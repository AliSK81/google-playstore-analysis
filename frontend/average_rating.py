import streamlit as st

from filters import get_filters
from utils import fetch_data


def fetch_average_rating(category):
    params = {"category_name": category} if category else {}
    return fetch_data("apps/average_rating", params).get("average_rating")


st.subheader("Average Rating per Category")

with st.sidebar:
    filters = get_filters(
        show_category=True
    )

category = filters["category"]
avg_rating = fetch_average_rating(category)

if avg_rating is not None:
    rounded_rating = round(avg_rating, 1)
    st.markdown(f"### 🌟 **{round(avg_rating, 1)}** out of 5")
else:
    st.warning("No average rating data available.")
