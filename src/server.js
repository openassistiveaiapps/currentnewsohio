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
          Authorization: `Bearer ${HUGGINGFACE_API_KEY}`,
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

// Endpoint: Get Ohio News
app.get("/api/news", async (req, res) => {
  try {
    const q = "Ohio OR Columbus OR Cleveland OR Cincinnati OR Dayton OR Akron OR Toledo";
    const response = await axios.get("https://newsapi.org/v2/everything", {
      params: {
        q,
        language: "en",
        pageSize: 15,
        sortBy: "publishedAt",
        apiKey: process.env.NEWSAPI_KEY,
      },
    });

    const raw = response.data.articles || [];
    const doSummaries = req.query.summary === "1" || req.query.summary === "true";

    //console.log(`/api/news: fetched ${raw.length} articles. Summaries: ${doSummaries}`);
    if (!doSummaries) {
      // return raw articles for speed
      return res.json({ ok: true, count: raw.length, articles: raw });
    }

    // Sequential summarization (safer for rate limits and easier to confirm calls)
    const articles = [];
    for (const a of raw) {
      const textToSummarize = a.description || a.content || a.title || "";
      //console.log("Summarizing article:", a.title, "text length:", textToSummarize.length);
      const summary = await summarizeText(textToSummarize);
      articles.push({ ...a, summary });
    }

    return res.json({ ok: true, count: articles.length, articles });
  } catch (err) {
    console.error("/api/news error:", err?.response?.status, err?.message);
    return res.status(500).json({ ok: false, error: err?.message || "unknown" });
  }
});


app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
