import matplotlib.pyplot as plt
import streamlit as st

from data_fetcher import fetch_update_trend
from filters import get_filters

st.subheader("App Update Trend")

with st.sidebar:
    filters = get_filters(
        show_category=True
    )

category = filters["category"]

update_trend = fetch_update_trend(category)

if update_trend:
    years = [entry["year"] for entry in update_trend]
    counts = [entry["count"] for entry in update_trend]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(years, counts, marker="o", color="purple")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Apps Updated")
    st.pyplot(fig)
else:
    st.warning(f"No update trend data available for {category}.")
