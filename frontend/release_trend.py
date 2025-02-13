import matplotlib.pyplot as plt
import streamlit as st

from filters import get_filters
from utils import fetch_data


def fetch_release_trend(category=None):
    params = {"category_name": category} if category else {}
    return fetch_data("apps/release_trend", params)


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
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(years, counts, marker="o", color="green")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Apps Released")
    st.pyplot(fig)
else:
    st.warning(f"No release trend data available for {category}.")
