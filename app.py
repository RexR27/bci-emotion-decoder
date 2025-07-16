import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🧠 Advanced BCI Emotion Decoder", layout="wide")
st.title("🧠 Advanced Simulated BCI Emotion Decoder")

# 1. Sliders to simulate multiple brainwave band strengths
col1, col2, col3, col4 = st.columns(4)
with col1:
    alpha = st.slider("Alpha (Calm)", 0.0, 2.0, 1.0, 0.01)
with col2:
    beta = st.slider("Beta (Alert)", 0.0, 2.0, 1.0, 0.01)
with col3:
    theta = st.slider("Theta (Drowsy)", 0.0, 2.0, 0.5, 0.01)
with col4:
    gamma = st.slider("Gamma (Excited)", 0.0, 2.0, 0.5, 0.01)

# 2. Simulate 30s of multi-band data (for visualization)
t = np.arange(0, 30, 0.5)
data = {
    "Time (s)": t,
    "Alpha": alpha * np.sin(2 * np.pi * 0.5 * t) + np.random.randn(len(t))*0.1,
    "Beta": beta * np.sin(2 * np.pi * 1.0 * t) + np.random.randn(len(t))*0.1,
    "Theta": theta * np.sin(2 * np.pi * 0.2 * t) + np.random.randn(len(t))*0.1,
    "Gamma": gamma * np.sin(2 * np.pi * 5.0 * t) + np.random.randn(len(t))*0.1,
}
df = pd.DataFrame(data)

# 3. Plot multi-band chart
fig = px.line(df, x="Time (s)", y=["Alpha", "Beta", "Theta", "Gamma"],
              title="Simulated EEG Band Powers")
st.plotly_chart(fig, use_container_width=True)

# 4. Decode into an emotion
def decode_emotion(a, b, t, g):
    values = [a, b, t, g]
    labels = ["Alpha", "Beta", "Theta", "Gamma"]
    max_value = max(values)
    dominant = labels[values.index(max_value)]
    
    # If all signals are very low -> Neutral
    if max_value < 0.3:
        return "🤔 Neutral"
    # If all are low-to-moderate -> Bored
    if max_value < 0.5:
        return "😐 Bored"

    # Complex mixing patterns (3 bands high)
    if a > 0.8 and b > 0.8 and g > 0.8:
        return "🤩 Euphoric"
    if b > 0.8 and t > 0.8 and g > 0.8:
        return "😵‍💫 Overwhelmed"
    if a > 0.8 and t > 0.8 and b > 0.8:
        return "😴 Drowsy-Alert"

    # Two-band combinations
    if a > 0.7 and b > 0.7:
        return "😊 Happy"
    if b > 0.7 and t > 0.7:
        return "😰 Anxious" if b > t else "😔 Melancholy"
    if t > 0.7 and g > 0.7:
        return "😵 Confused"
    if a > 0.7 and t > 0.7:
        return "😌 Peaceful"
    if b > 0.7 and g > 0.7:
        return "😄 Excited" if g > b else "🤯 Stressed"
    if a > 0.7 and g > 0.7:
        return "🤗 Blissful"
    
    # High single band + moderate others
    if b > 1.2 and t > 0.5:
        return "😤 Frustrated"
    if t > 1.2 and b > 0.5:
        return "😢 Sad"
    if b > 1.2 and a < 0.4:
        return "😠 Angry"
    if g > 1.2 and a < 0.4:
        return "😡 Rage"
    if a > 1.2 and b < 0.4:
        return "😇 Calm"
    if t > 1.2 and a < 0.4:
        return "😴 Sleepy"
    # New: high arousal (beta+gamma) → Fear
    if b > 1.2 and g > 0.5 and a < 0.5:
        return "😱 Fearful"

    # Dominant single band patterns
    if dominant == "Alpha" and a > 0.5:
        return "🧘 Meditative" if a > 1.4 else "😌 Calm"
    if dominant == "Beta" and b > 0.5:
        return "🎯 Focused" if b > 1.4 else "⚡ Alert"
    if dominant == "Theta" and t > 0.5:
        return "💤 Deep Sleep" if t > 1.4 else "😴 Sleepy"
    if dominant == "Gamma" and g > 0.5:
        return "🤪 Hyperactive" if g > 1.4 else "🔥 Energetic"
    
    # Fallback
    return "🤔 Neutral"

if st.button("🕵️ Decode Emotion"):
    emotion = decode_emotion(alpha, beta, theta, gamma)
    st.success(f"AI guesses you are feeling **{emotion}**!")
