import matplotlib.pyplot as plt
import streamlit as st

from client_api import fetch_release_trend
from filters import get_filters

st.subheader("App Release Trend")

with st.sidebar:
    filters = get_filters(
        show_category=True
    )

category = filters["category"]

release_trend = fetch_release_trend(category)

if release_trend:
    years = [entry["year"] for entry in release_trend]
    counts = [entry["count"] for entry in release_trend]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(years, counts, marker="o", color="green")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Apps Released")
    st.pyplot(fig)
else:
    st.warning(f"No release trend data available for {category}.")
