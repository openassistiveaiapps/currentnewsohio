#!/usr/bin/env python3
import time
import logging
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

URL = "https://cricclubs.com/FortyPlusLeague/viewPointsTable.do?league=19&clubId=24301"
DEBUG_HTML = "page_debug.html"

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
DEFAULT_VIEWPORT = {"width": 1280, "height": 800}
DEFAULT_TIMEOUT_MS = 120000

# Convert string to number
def text_to_number(s):
    try:
        return float(s)
    except:
        return None

# Parse a table and compute ranking
def parse_and_rank_table(table, table_index):
    headers = []
    thead = table.find("thead")
    if thead:
        headers = [th.get_text(strip=True).lower() for th in thead.find_all("th")]
    else:
        first_row = table.find("tr")
        if first_row:
            headers = [td.get_text(strip=True).lower() for td in first_row.find_all("td")]

    rows_data = []
    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cells) < len(headers):
            continue
        row = dict(zip(headers, cells))
        rows_data.append(row)

    if not rows_data:
        return pd.DataFrame()

    df = pd.DataFrame(rows_data)

    # Heuristic: find columns
    col_team = next((c for c in df.columns if "team" in c or "club" in c), df.columns[0])
    col_points = next((c for c in df.columns if "point" in c or c in ("p", "pt")), None)
    col_won = next((c for c in df.columns if "won" in c), None)
    col_nrr = next((c for c in df.columns if "nrr" in c), None)

    # Coerce numeric
    if col_points:
        df["_points"] = df[col_points].apply(text_to_number)
    else:
        df["_points"] = 0
    if col_won:
        df["_won"] = df[col_won].apply(text_to_number)
    else:
        df["_won"] = 0
    if col_nrr:
        df["_nrr"] = df[col_nrr].apply(text_to_number)
    else:
        df["_nrr"] = 0

    df["_team"] = df[col_team].astype(str)

    # Rank
    df = df.sort_values(by=["_points", "_nrr", "_won"], ascending=[False, False, False]).reset_index(drop=True)
    df["rank"] = df.index + 1

    # Add table identifier
    df["table_index"] = table_index

    return df[["table_index", "rank", "_team", "_points", "_nrr", "_won"]].rename(
        columns={"_team": "team", "_points": "points", "_nrr": "nrr", "_won": "won"}
    )

# Main scraping
def scrape_multiple_tables(url, headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(user_agent=DEFAULT_USER_AGENT, viewport=DEFAULT_VIEWPORT)
        page = context.new_page()

        logging.info("Loading page...")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT_MS)
        except PWTimeoutError:
            logging.warning("Timeout during page load, proceeding anyway.")

        time.sleep(5)  # extra wait for JS tables
        html = page.content()
        with open(DEBUG_HTML, "w", encoding="utf-8") as f:
            f.write(html)
        logging.info("Saved debug HTML to %s", DEBUG_HTML)
        browser.close()

        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        all_dfs = []

        for idx, table in enumerate(tables):
            df_table = parse_and_rank_table(table, idx)
            if not df_table.empty:
                all_dfs.append(df_table)

        if not all_dfs:
            logging.error("No tables parsed successfully.")
            return pd.DataFrame()
        combined_df = pd.concat(all_dfs, ignore_index=True)
        return combined_df

# Run
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df_all = scrape_multiple_tables(URL, headless=False)  # set headless=True if Cloudflare solved
    if not df_all.empty:
        print(df_all.to_string(index=False))
        df_all.to_csv("all_tables_ranked.csv", index=False)
        logging.info("Saved CSV all_tables_ranked.csv")
    else:
        logging.error("No ranking data extracted.")
