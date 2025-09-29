import express from "express";
import axios from "axios";
import 'dotenv/config';

const app = express();
const PORT = process.env.PORT || 5000;

// Endpoint: Get Ohio News
app.get("/api/news", async (req, res) => {
  try {
    const response = await axios.get("https://newsapi.org/v2/everything", {
      params: {
        q: "Ohio",
        sortBy: "publishedAt",
        apiKey: process.env.NEWSAPI_KEY,
      },
    });
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
