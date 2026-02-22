import streamlit as st
import requests
import pandas as pd
from collections import Counter
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="TicketPilot Monitor", layout="wide")

st_autorefresh(interval=2000, key="datarefresh")

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/queue"
SIMULATE_URL = f"{BASE_URL}/simulate"
EXPORT_URL = f"{BASE_URL}/export"

st.title("TicketPilot Monitor")

with st.sidebar:
    st.header("System Controls")
    if st.button(" Simulate", use_container_width=True):
        try:
            res = requests.post(SIMULATE_URL, timeout=2)
            if res.status_code == 200:
                st.success("Simulation sequence started.")
        except Exception:
            st.error("Engine Connection Error")

    st.divider()
    st.write("### Data Audit")
    if st.button("Exportt", use_container_width=True):
        st.info("Exporting CSV from server storage...")
        st.markdown(
            f"[Click here to Download CSV]({EXPORT_URL})", unsafe_allow_html=True
        )

# 5. Data Fetching Logic
try:
    response = requests.get(API_URL, timeout=1)
    if response.status_code == 200:
        payload = response.json()
        tickets = payload.get("queue", [])
        total_count = payload.get("total", 0)

        m1, m2, m3 = st.columns(3)
        m1.metric("Backlog Size", total_count)

        high_prio = sum(1 for t in tickets if float(t.get("priority", 0)) >= 1.0)
        m2.metric("High Priority (1)", high_prio)
        m3.metric("Sync Status", f"Last: {datetime.now().strftime('%H:%M:%S')}")

        st.divider()

        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.subheader("📊 Category Distribution")
            categories = [t.get("category", "Unknown") for t in tickets]
            if categories:
                cat_data = pd.DataFrame.from_dict(
                    Counter(categories), orient="index", columns=["Count"]
                )
                st.bar_chart(cat_data, color="#007bff")

        with col_right:
            st.subheader("⚖️ Priority Split (High vs Low)")
            if tickets:
                prio_df = pd.DataFrame(
                    {
                        "Level": ["High", "Low"],
                        "Total": [high_prio, total_count - high_prio],
                    }
                )
                st.vega_lite_chart(
                    prio_df,
                    {
                        "mark": {"type": "arc", "innerRadius": 50},
                        "encoding": {
                            "theta": {"field": "Total", "type": "quantitative"},
                            "color": {
                                "field": "Level",
                                "type": "nominal",
                                "scale": {"range": ["#ff4b4b", "#1f77b4"]},
                            },
                        },
                    },
                    use_container_width=True,
                )

        st.subheader(" Priority Queue Feed")
        for idx, t in enumerate(tickets):
            icon = "🔴" if float(t.get("priority", 0)) >= 1.0 else "🔵"
            with st.expander(
                f"#{idx+1} {icon} {t['ticket_id']} | {t['subject'][:50]}..."
            ):
                st.json(t)
    else:
        st.error("Engine Offline: Could not reach FastAPI.")

except Exception:
    st.warning("Connecting to TicketPilot Engine...")
