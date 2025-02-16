import matplotlib.pyplot as plt
import streamlit as st

from client_api import fetch_rating_distribution
from filters import get_filters

st.subheader("Rating Distribution")

with st.sidebar:
    filters = get_filters(
        show_category=True,
        show_rating=True,
        show_price=True,
        show_installs=True,
        show_content_rating=True,
        show_free_only=True,
        show_ads=True,
        show_in_app=True,
        show_editors_choice=True)

filtered_data = fetch_rating_distribution(filters)

if filtered_data:
    ratings = [entry['rating'] for entry in filtered_data]
    counts = [entry['count'] for entry in filtered_data]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(ratings, counts, color="blue", alpha=0.9, width=0.09)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    st.pyplot(fig)
else:
    st.warning("No data available for rating distribution.")
