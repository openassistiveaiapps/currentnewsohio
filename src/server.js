import express from "express";
import axios from "axios";
import 'dotenv/config';

const app = express();
const PORT = process.env.PORT || 5000;

// Helper: Summarize text with Hugging Face
// Read API keys and model from environment variables. Do NOT hardcode secrets.
const HUGGINGFACE_API_KEY = process.env.HUGGINGFACE_API_KEY;
const HF_MODEL = process.env.HF_MODEL || "sshleifer/distilbart-cnn-12-6";

const summaryCache = new Map(); // simple in-memory cache

async function summarizeText(text) {
  // quick guards
  if (!text) return text;
  if (text.length < 40) return text; // skip very short text

  // cache key: use a truncated version of the text to keep map small
  const cacheKey = text.slice(0, 400);
  if (summaryCache.has(cacheKey)) {
    console.log("summarizeText: cache hit");
    return summaryCache.get(cacheKey);
  }

  console.log("summarizeText: calling HF for text length", text.length);

  try {
    const hfUrl = `https://api-inference.huggingface.co/models/${HF_MODEL}`;
    const resp = await axios.post(
      hfUrl,
      { inputs: text },
      {
        headers: {
          Authorization: `Bearer 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`,
          "Content-Type": "application/json",
        },
        timeout: 60000,
      }
    );

    // HF returns different shapes; handle common ones
    let summary = "";
    if (Array.isArray(resp.data) && resp.data[0] && resp.data[0].summary_text) {
      summary = resp.data[0].summary_text;
    } else if (resp.data && resp.data.summary_text) {
      summary = resp.data.summary_text;
    } else if (typeof resp.data === "string") {
      summary = resp.data;
    } else if (Array.isArray(resp.data) && typeof resp.data[0] === "string") {
      summary = resp.data[0];
    } else {
      summary = JSON.stringify(resp.data).slice(0, 1000);
    }

    // cache but keep cache size reasonable
    try {
      if (summaryCache.size > 200) {
        // simple eviction: clear when too big (you can implement LRU)
        summaryCache.clear();
      }
      summaryCache.set(cacheKey, summary);
    } catch (e) {
      console.warn("cache set failed", e.message);
    }

    return summary;
  } catch (err) {
    console.error("summarizeText: HuggingFace error:", err?.response?.status, err?.message);
    // If HF returns 503 (model loading), you might want to surface that to the caller
    // For now fallback to original or description
    return text;
  }
}

// Lightweight keyword-based categorizer
function categorizeArticle(article) {
  const text = ((article.title || "") + " " + (article.description || "") + " " + (article.content || "")).toLowerCase();

  const categories = {
    politics: /\b(president|senate|congress|election|governor|mayor|policy|law|senator|representative|house|vote|campaign)\b/,
    sports: /\b(game|score|win|season|goal|nba|mlb|nfl|nhl|soccer|football|basketball|baseball|coach|tournament|match)\b/,
    entertainment: /\b(movie|film|actor|actress|celebrity|concert|music|album|tv|series|hollywood|netflix|award|oscars)\b/,
    events: /\b(festival|rally|conference|exhibition|parade|event|ceremony|fair|summit)\b/,
    technology: /\b(tech|software|hardware|ai|machine learning|startup|google|apple|microsoft|facebook|meta|intel)\b/,
    business: /\b(market|stocks|stock|shares|economy|company|business|profit|revenue|ipo|bank)\b/,
    health: /\b(health|covid|vaccine|hospital|doctor|medical|disease|pandemic)\b/,
  };

  for (const [cat, rx] of Object.entries(categories)) {
    if (rx.test(text)) return cat;
  }

  // fallback
  return 'general';
}

// Endpoint: Get Ohio News
app.get("/api/news", async (req, res) => {
  try {
    // Validate required environment variables
    // if (!process.env.NEWSAPI_KEY) {
    //  console.error('Missing NEWSAPI_KEY in environment');
    //  return res.status(400).json({ ok: false, error: 'NEWSAPI_KEY not configured on server' });
    // }
    const q = "Ohio OR Columbus OR Cleveland OR Cincinnati OR Dayton OR Akron OR Toledo";
    const response = await axios.get("https://newsapi.org/v2/everything", {
      params: {
        q,
        language: "en",
        pageSize: 15,
        sortBy: "publishedAt",
        apiKey: "93e0ea8e915a487e90d2736a52b45028" // process.env.NEWSAPI_KEY,
      },
    });

  const raw = response.data.articles || [];
    const doSummaries = req.query.summary === "1" || req.query.summary === "true";
  const doGroup = req.query.group === "1" || req.query.group === "true";

    // if (doSummaries) {
    //  console.error('Summaries requested but HUGGINGFACE_API_KEY missing');
    //  return res.status(400).json({ ok: false, error: 'HUGGINGFACE_API_KEY not configured on server' });
    // }

    //console.log(`/api/news: fetched ${raw.length} articles. Summaries: ${doSummaries}`);
    if (!doSummaries) {
      // attach categories quickly
      const categorized = raw.map(a => ({ ...a, category: categorizeArticle(a) }));
      if (doGroup) {
        const grouped = categorized.reduce((acc, cur) => {
          acc[cur.category] = acc[cur.category] || [];
          acc[cur.category].push(cur);
          return acc;
        }, {});
        return res.json({ ok: true, count: categorized.length, grouped });
      }
      // return raw articles for speed
      return res.json({ ok: true, count: categorized.length, articles: categorized });
    }

    // Sequential summarization (safer for rate limits and easier to confirm calls)
    const articles = [];
    for (const a of raw) {
      const textToSummarize = a.description || a.content || a.title || "";
      //console.log("Summarizing article:", a.title, "text length:", textToSummarize.length);
      const summary = await summarizeText(textToSummarize);
      articles.push({ ...a, summary, category: categorizeArticle(a) });
    }

    if (doGroup) {
      const grouped = articles.reduce((acc, cur) => {
        acc[cur.category] = acc[cur.category] || [];
        acc[cur.category].push(cur);
        return acc;
      }, {});
      return res.json({ ok: true, count: articles.length, grouped });
    }

    return res.json({ ok: true, count: articles.length, articles });
  } catch (err) {
    console.error("/api/news error:", err?.response?.status, err?.message);
    return res.status(500).json({ ok: false, error: err?.message || "unknown" });
  }
});


app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
