import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from filters import get_filters
from utils import fetch_data


def fetch_apps(filters):
    data = fetch_data("apps", filters)
    return pd.DataFrame(data) if data else pd.DataFrame()


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

filtered_df = fetch_apps(filters)

if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(8, 3))
    filtered_df["rating"].hist(bins=20, ax=ax, color="blue", alpha=0.7)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    st.pyplot(fig)
else:
    st.warning("No data available for rating distribution.")
