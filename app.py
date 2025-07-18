import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="🧠 BCI Live Decoder", layout="wide")

# CSS: Adjust spacing, font, layout
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .slider-label {
        font-size: 24px !important;
        font-weight: bold !important;
        display: flex;
        align-items: center;
    }
    .stSlider {
        margin-bottom: -20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("## 🧠 Brainwave Decoder - Live Signal Focus")

# Slider container
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='slider-label'>🧠 Alpha</div>", unsafe_allow_html=True)
    alpha = st.slider("", 0.0, 2.0, 1.0, 0.01, key="alpha", on_change=lambda: st.session_state.update(last="Alpha"))
with col2:
    st.markdown("<div class='slider-label'>⚡ Beta</div>", unsafe_allow_html=True)
    beta = st.slider("", 0.0, 2.0, 1.0, 0.01, key="beta", on_change=lambda: st.session_state.update(last="Beta"))
with col3:
    st.markdown("<div class='slider-label'>🌙 Theta</div>", unsafe_allow_html=True)
    theta = st.slider("", 0.0, 2.0, 0.5, 0.01, key="theta", on_change=lambda: st.session_state.update(last="Theta"))
with col4:
    st.markdown("<div class='slider-label'>🚀 Gamma</div>", unsafe_allow_html=True)
    gamma = st.slider("", 0.0, 2.0, 0.5, 0.01, key="gamma", on_change=lambda: st.session_state.update(last="Gamma"))

# Initialize last changed if not present
if "last" not in st.session_state:
    st.session_state["last"] = "Alpha"

# Simulate signal data
t = np.arange(0, 30, 0.5)
signal_map = {
    "Alpha": alpha * np.sin(2 * np.pi * 0.5 * t) + np.random.randn(len(t)) * 0.1,
    "Beta": beta * np.sin(2 * np.pi * 1.0 * t) + np.random.randn(len(t)) * 0.1,
    "Theta": theta * np.sin(2 * np.pi * 0.2 * t) + np.random.randn(len(t)) * 0.1,
    "Gamma": gamma * np.sin(2 * np.pi * 5.0 * t) + np.random.randn(len(t)) * 0.1,
}
selected = st.session_state["last"]

# Plot the last-touched signal
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=signal_map[selected], name=selected, line=dict(width=3)))
fig.update_layout(
    title=f"📊 Showing Live Signal: {selected}",
    xaxis_title="Time (s)",
    yaxis_title="Amplitude",
    height=400,
    template="plotly_dark",
    margin=dict(t=60, b=60)
)
st.plotly_chart(fig, use_container_width=True)
