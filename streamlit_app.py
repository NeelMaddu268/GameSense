# streamlit_app.py
import streamlit as st
import numpy as np
from sklearn.ensemble import IsolationForest
import random
import openai
import os
import time

# --- OpenAI Setup (optional) ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Title ---
st.title("PrizePicks AI Insight Demo")

# --- Players ---
players = ["LeBron James", "Stephen Curry", "Kevin Durant", "Giannis Antetokounmpo"]

# --- Historical scores ---
history = {
    player: np.array([random.randint(18, 25) for _ in range(10)]).reshape(-1,1)
    for player in players
}

# --- Train anomaly detectors ---
models = {
    player: IsolationForest(contamination=0.1, random_state=42).fit(scores)
    for player, scores in history.items()
}

# --- Function for AI commentary ---
def get_ai_commentary(player, score, anomaly):
    if not anomaly:
        return ""
    prompt = f"""
    You are a sports analyst. Player {player} just scored {score} points, which is unusually high for them.
    Explain in 1-2 sentences why this anomaly might have occurred in a clear and casual way.
    """
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return "AI explanation unavailable"

# --- Simulate live insights ---
def generate_insights():
    results = []
    for player in players:
        score = random.randint(15, 35)
        anomaly = True if models[player].predict(np.array([[score]]))[0] == -1 else False
        commentary = get_ai_commentary(player, score, anomaly)
        results.append({
            "player": player,
            "score": score,
            "anomaly": anomaly,
            "commentary": commentary
        })
    return results

# --- Streamlit UI ---
refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 1, 10, 3)

placeholder = st.empty()

while True:
    insights = generate_insights()
    with placeholder.container():
        for insight in insights:
            st.subheader(insight["player"])
            st.write(f"Score: {insight['score']}")
            st.write(f"Anomaly: {'⚠️' if insight['anomaly'] else 'Normal'}")
            if insight.get("commentary"):
                st.write(f"*{insight['commentary']}*")
            st.markdown("---")
    time.sleep(refresh_interval)
