import streamlit as st

from data_fetcher import fetch_average_rating
from filters import get_filters

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
