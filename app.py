import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="🧠 Advanced BCI Emotion Decoder", layout="wide")

# Custom CSS for font enhancements
st.markdown("""
    <style>
    .css-1r6slb0 p {
        font-size: 22px !important;
        font-weight: 600;
        color: #444;
    }
    .big-text {
        font-size: 40px !important;
        color: green;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='font-size: 48px; color: #4A90E2;'>🧠 Advanced Simulated BCI Emotion Decoder</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**🧠 Alpha**")
    alpha = st.slider("", 0.0, 2.0, 1.0, 0.01, key="alpha")
with col2:
    st.markdown("**⚡ Beta**")
    beta = st.slider("", 0.0, 2.0, 1.0, 0.01, key="beta")
with col3:
    st.markdown("**🌙 Theta**")
    theta = st.slider("", 0.0, 2.0, 0.5, 0.01, key="theta")
with col4:
    st.markdown("**🚀 Gamma**")
    gamma = st.slider("", 0.0, 2.0, 0.5, 0.01, key="gamma")

# Simulated EEG data
t = np.arange(0, 30, 0.5)
df = pd.DataFrame({
    "Time (s)": t,
    "Alpha": alpha * np.sin(2 * np.pi * 0.5 * t) + np.random.randn(len(t)) * 0.1,
    "Beta": beta * np.sin(2 * np.pi * 1.0 * t) + np.random.randn(len(t)) * 0.1,
    "Theta": theta * np.sin(2 * np.pi * 0.2 * t) + np.random.randn(len(t)) * 0.1,
    "Gamma": gamma * np.sin(2 * np.pi * 5.0 * t) + np.random.randn(len(t)) * 0.1
})

# Enhanced EEG Chart with title
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Time (s)"], y=df["Alpha"], name="Alpha", line=dict(color='blue')))
fig.add_trace(go.Scatter(x=df["Time (s)"], y=df["Beta"], name="Beta", line=dict(color='red')))
fig.add_trace(go.Scatter(x=df["Time (s)"], y=df["Theta"], name="Theta", line=dict(color='green')))
fig.add_trace(go.Scatter(x=df["Time (s)"], y=df["Gamma"], name="Gamma", line=dict(color='purple')))

fig.update_layout(
    title="<b style='font-size:28px'>📊 Simulated EEG Band Powers</b>",
    xaxis_title="Time (s)",
    yaxis_title="Amplitude",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
    margin=dict(t=60, b=100)
)
st.plotly_chart(fig, use_container_width=True)

# Emotion decoder function
def decode_emotion(a, b, t, g):
    values = [a, b, t, g]
    labels = ["Alpha", "Beta", "Theta", "Gamma"]
    max_value = max(values)
    dominant = labels[values.index(max_value)]

    if max_value < 0.3:
        return "🤔 Neutral"
    if max_value < 0.5:
        return "😐 Bored"

    if a > 0.8 and b > 0.8 and g > 0.8:
        return "🤩 Euphoric"
    if b > 0.8 and t > 0.8 and g > 0.8:
        return "😵‍💫 Overwhelmed"
    if a > 0.8 and t > 0.8 and b > 0.8:
        return "😴 Drowsy-Alert"

    if a > 0.7 and b > 0.7:
        return "😊 Happy"
    if b > 0.7 and t > 0.7:
        return "😰 Anxious" if b > t else "😔 Feeling Low"
    if t > 0.7 and g > 0.7:
        return "😵 Confused"
    if a > 0.7 and t > 0.7:
        return "😌 Peaceful"
    if b > 0.7 and g > 0.7:
        return "😄 Excited" if g > b else "🤯 Stressed"
    if a > 0.7 and g > 0.7:
        return "🤗 Blissful"

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
    if b > 1.2 and g > 0.5 and a < 0.5:
        return "😱 Fearful"

    if dominant == "Alpha" and a > 0.5:
        return "🧘 Meditative" if a > 1.4 else "😌 Calm"
    if dominant == "Beta" and b > 0.5:
        return "🎯 Focused" if b > 1.4 else "⚡ Alert"
    if dominant == "Theta" and t > 0.5:
        return "💤 Deep Sleep" if t > 1.4 else "😴 Sleepy"
    if dominant == "Gamma" and g > 0.5:
        return "🤪 Hyperactive" if g > 1.4 else "🔥 Energetic"

    return "🤔 Neutral"

# Decode button
if st.button("🕵️ Decode Emotion"):
    emotion = decode_emotion(alpha, beta, theta, gamma)
    st.markdown(f"<div class='big-text'>AI guesses you are feeling {emotion}</div>", unsafe_allow_html=True)
