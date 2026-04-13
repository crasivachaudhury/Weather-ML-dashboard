import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# -----------------------------
# DUMMY DATA (NO ML USED)
# -----------------------------
def fetch_realtime_kolkata(city):
    return {
        "Temp_C": round(random.uniform(25, 35), 2),
        "RH_pct": random.randint(50, 90)
    }

# ✅ DATE-BASED FORECAST
def predict_next_24h(selected_date):
    times, temps, rain_probs = [], [], []

    base_time = datetime.combine(selected_date, datetime.min.time())

    for i in range(0, 24, 3):
        t = base_time + timedelta(hours=i)
        times.append(t.strftime("%d %b %Y %H:%M"))
        temps.append(round(random.uniform(22, 35), 1))
        rain_probs.append(round(random.uniform(0, 100), 1))

    return {
        "time": times,
        "temp": temps,
        "rain_prob": rain_probs
    }

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Weather Prediction", layout="wide")
st.title("🌦️ Weather Prediction Dashboard")

# Sidebar
st.sidebar.header("User Input")
city = st.sidebar.text_input("City", "Kolkata")
date = st.sidebar.date_input("Select Date", datetime.now())

# Data
api_vals = fetch_realtime_kolkata(city)
forecast = predict_next_24h(date)

# -----------------------------
# TOP SECTION
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Weather Data")
    st.metric("Temperature (°C)", api_vals["Temp_C"])
    st.metric("Humidity (%)", api_vals["RH_pct"])

with col2:
    st.subheader("📡 Sensor Data")
    s1, s2 = st.columns(2)
    with s1:
        st.metric("Sensor Temp (°C)", "EMPTY")
    with s2:
        st.metric("Sensor Humidity (%)", "EMPTY")

st.divider()

# -----------------------------
# GRAPHS
# -----------------------------
g1, g2 = st.columns(2)

with g1:
    st.subheader("📈 Temperature vs Time")
    fig_t = go.Figure()
    fig_t.add_trace(go.Scatter(
        x=forecast["time"],
        y=forecast["temp"],
        mode='lines+markers'
    ))
    st.plotly_chart(fig_t, use_container_width=True, key="temp_graph")

with g2:
    st.subheader("🌧️ Rainfall Probability")
    fig_r = go.Figure()
    fig_r.add_trace(go.Bar(
        x=forecast["time"],
        y=forecast["rain_prob"]
    ))
    st.plotly_chart(fig_r, use_container_width=True, key="rain_graph")

st.divider()

# -----------------------------
# SENSOR EMPTY GRAPHS
# -----------------------------
sg1, sg2 = st.columns(2)

with sg1:
    st.subheader("📊 Sensor Temperature (Live)")
    fig_empty1 = go.Figure()
    fig_empty1.update_layout(
        annotations=[dict(text="No Sensor Data", x=0.5, y=0.5, showarrow=False)]
    )
    st.plotly_chart(fig_empty1, use_container_width=True, key="sensor_temp")

with sg2:
    st.subheader("📊 Sensor Rainfall Probability (Live)")
    fig_empty2 = go.Figure()
    fig_empty2.update_layout(
        annotations=[dict(text="No Sensor Data", x=0.5, y=0.5, showarrow=False)]
    )
    st.plotly_chart(fig_empty2, use_container_width=True, key="sensor_rain")

st.divider()

# -----------------------------
# FINAL CARDS UI
# -----------------------------
st.subheader("📋 Model Prediction (Next 24 Hours)")

if forecast:
    num_cols = 4

    for i in range(0, len(forecast["time"]), num_cols):
        cols = st.columns(num_cols)

        for j in range(num_cols):
            if i + j < len(forecast["time"]):
                idx = i + j

                temp = forecast["temp"][idx]
                rain = forecast["rain_prob"][idx]
                rain_mm = round(rain / 100, 3)
                rain_status = "YES" if rain > 50 else "NO"

                with cols[j]:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #1e2a38, #2c3e50);
                        padding:15px;
                        border-radius:15px;
                        color:white;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                        margin-bottom:15px;
                    ">
                        <div style="font-size:13px;">🕒 {forecast['time'][idx]}</div>
                        <hr style="margin:5px 0; border:0.5px solid #555;">
                        <div>🌡 Temp: {temp} °C</div>
                        <div>🌧 Rain Prob: {rain}%</div>
                        <div>☁️ Rain: {rain_status}</div>
                        <div>💧 {rain_mm} mm/hr</div>
                    </div>
                    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Built using Streamlit | Weather ML Project 🚀")