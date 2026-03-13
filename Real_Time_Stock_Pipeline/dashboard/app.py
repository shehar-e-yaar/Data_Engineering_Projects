import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Real-Time Stock Dashboard", layout="wide")
st.title("Real-Time Stock Market Dashboard")

engine = create_engine("postgresql+psycopg2://stock_user:stock_pass@127.0.0.1:55432/stock_db")

query = """
SELECT symbol, price, volume, event_time
FROM stock_prices
ORDER BY event_time DESC
LIMIT 200
"""

df = pd.read_sql(query, engine)

if df.empty:
    st.warning("No data available yet. Start producer and Spark job.")
else:
    st.subheader("Latest Stock Records")
    st.dataframe(df, use_container_width=True)

    st.subheader("Latest Record Per Symbol")
    latest_df = df.sort_values("event_time").groupby("symbol").tail(1)
    st.dataframe(latest_df[["symbol", "price", "volume", "event_time"]], use_container_width=True)

    st.subheader("Price Trend")
    chart_df = df.sort_values("event_time")
    st.line_chart(chart_df.set_index("event_time")["price"])