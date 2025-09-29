import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    axios.get("/api/news").then((res) => {
      setArticles(res.data.articles || []);
    });
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>📰 Current Ohio News</h1>
      {articles.length === 0 ? (
        <p>Loading news...</p>
      ) : (
        <ul>
          {articles.map((a, i) => (
            <li key={i} style={{ margin: "1rem 0" }}>
              <a href={a.url} target="_blank" rel="noreferrer">
                <strong>{a.title}</strong>
              </a>
              <p>{a.description}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
