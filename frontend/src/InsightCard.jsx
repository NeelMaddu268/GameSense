import React from "react";

function InsightCard({ player, score, anomaly }) {
  return (
    <div style={{
      padding: "1rem",
      border: "2px solid black",
      borderRadius: "12px",
      margin: "1rem",
      width: "250px"
    }}>
      <h2>{player}</h2>
      <p>Score: {score}</p>
      <p>{anomaly ? "⚠️ Anomaly detected!" : "Normal performance"}</p>
    </div>
  );
}

export default InsightCard;
