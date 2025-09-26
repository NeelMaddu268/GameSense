from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sklearn.ensemble import IsolationForest
import random

app = FastAPI()

# Allow Vite frontend
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example players
players = ["LeBron James", "Stephen Curry", "Kevin Durant", "Giannis Antetokounmpo"]

# Historical scores (simple simulated history for each player)
history = {
    player: np.array([random.randint(18, 25) for _ in range(10)]).reshape(-1,1)
    for player in players
}

# Train anomaly detector for each player
models = {}
for player, scores in history.items():
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(scores)
    models[player] = model

@app.get("/insights")
def get_insights():
    results = []

    for player in players:
        # Simulate live score
        new_score = random.randint(15, 35)
        prediction = models[player].predict(np.array([[new_score]]))[0]  # -1 = anomaly

        results.append({
            "player": player,
            "score": new_score,
            "anomaly": True if prediction == -1 else False
        })

    return results
