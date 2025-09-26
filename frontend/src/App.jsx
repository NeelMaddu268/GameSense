import React, { useState, useEffect } from "react";
import InsightCard from "./InsightCard";

function App() {
  const [insights, setInsights] = useState([]);

  const fetchInsights = () => {
    fetch("http://127.0.0.1:8000/insights")
      .then(res => res.json())
      .then(data => setInsights(data));
  };

  // Fetch every 3 seconds
  useEffect(() => {
    fetchInsights(); // initial fetch
    const interval = setInterval(fetchInsights, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ display: "flex", justifyContent: "center", flexWrap: "wrap", marginTop: "2rem" }}>
      {insights.map((insight) => (
        <InsightCard
          key={insight.player}
          player={insight.player}
          score={insight.score}
          anomaly={insight.anomaly}
        />
      ))}
    </div>
  );
}

export default App;
