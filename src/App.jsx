import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    // Request summaries from the backend by passing summary=1
    axios.get("/api/news?summary=1").then((res) => {
      setArticles(res.data.articles || []);
    });
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>📰 Ohio News (AI Summarized)</h1>
      {articles.length === 0 ? (
        <p>Loading AI-powered news...</p>
      ) : (
        <ul>
          {articles.map((a, i) => (
            <li key={i} style={{ margin: "1rem 0", padding: "1rem", border: "1px solid #ccc", borderRadius: "8px" }}>
              <a href={a.url} target="_blank" rel="noreferrer">
                <strong>{a.title}</strong>
              </a>
              <p><em>{a.source.name}</em> — {new Date(a.publishedAt).toLocaleString()}</p>
              <p>{a.summary}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
