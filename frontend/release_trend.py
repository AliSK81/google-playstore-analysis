import matplotlib.pyplot as plt
import streamlit as st

from filters import get_filter_values
from utils import fetch_data


def fetch_release_trend(category=None):
    params = {"category_name": category} if category and category != 'All' else {}
    return fetch_data("apps/release_trend", params)


st.subheader("App Release Trend")

(categories, content_ratings, min_rating, max_rating, min_price, max_price, min_installs,
 max_installs) = get_filter_values()

with st.sidebar:
    category = st.selectbox("📂 Select Category", ["All"] + categories)

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
