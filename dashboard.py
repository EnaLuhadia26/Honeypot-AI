import json
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import altair as alt

LOG_PATH = "logs/honeypot.json"

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

st.set_page_config(page_title="Honeypot Dashboard", layout="wide")
st.title("🕵️ Honeypot Monitoring Dashboard")

# Load logs
def load_logs(path=LOG_PATH):
    events = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        st.warning("⚠️ No log file found yet.")
    return events

events = load_logs()

if not events:
    st.info("No events yet. Waiting for honeypot logs...")
else:
    df = pd.DataFrame(events)

    # Convert timestamp
    df["ts"] = pd.to_datetime(df["ts"], errors="coerce")

    # ----------------- Top Metrics -----------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Events", len(df))
    col2.metric("Unique IPs", df["ip"].nunique())
    col3.metric("Suspicious Events", df["suspicious"].sum())

    st.markdown("---")

    # ----------------- Charts Row -----------------
    chart_col1, chart_col2, chart_col3 = st.columns(3)

    # Pie Chart: Suspicious vs Normal
    with chart_col1:
        st.subheader("⚠️ Suspicious vs Normal")
        pie_data = df["suspicious"].value_counts().reset_index()
        pie_data.columns = ["suspicious", "count"]
        pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
            theta="count:Q",
            color=alt.Color("suspicious:N", scale=alt.Scale(domain=[False, True], range=["#4caf50", "#f44336"])),
            tooltip=["suspicious", "count"]
        )
        st.altair_chart(pie_chart, use_container_width=True)

    # Bar Chart: Requests by Method
    with chart_col2:
        st.subheader("⚡ Requests by Method")
        chart_methods = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x="method:N",
                y="count():Q",
                color="method:N",
                tooltip=["method", "count()"]
            )
        )
        st.altair_chart(chart_methods, use_container_width=True)

    # Bar Chart: Top Attacking IPs
    with chart_col3:
        st.subheader("🌍 Top Attacking IPs")
        ip_counts = df["ip"].value_counts().reset_index()
        ip_counts.columns = ["ip", "count"]
        chart_ips = (
            alt.Chart(ip_counts.head(10))
            .mark_bar()
            .encode(
                x="count:Q",
                y=alt.Y("ip:N", sort="-x"),
                tooltip=["ip", "count"]
            )
        )
        st.altair_chart(chart_ips, use_container_width=True)

    st.markdown("---")

    # ----------------- Raw Logs -----------------
    with st.expander("📜 View Raw Logs"):
        st.dataframe(df)





