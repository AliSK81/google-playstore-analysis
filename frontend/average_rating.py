import streamlit as st

from filters import get_filter_values
from utils import fetch_data


def fetch_average_rating(category):
    params = {"category_name": category} if category and category != 'All' else {}
    return fetch_data("apps/average_rating", params).get("average_rating")


st.subheader("Average Rating per Category")

(categories, content_ratings, min_rating, max_rating, min_price, max_price, min_installs,
 max_installs) = get_filter_values()

with st.sidebar:
    category = st.selectbox("📂 Select Category", ["All"] + categories)

avg_rating = fetch_average_rating(category)

if avg_rating is not None:
    rounded_rating = round(avg_rating, 1)
    st.markdown(f"### 🌟 **{round(avg_rating, 1)}** out of 5")
else:
    st.warning("No average rating data available.")
