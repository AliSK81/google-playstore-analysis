import streamlit as st

from utils import fetch_data


def fetch_filters():
    filters_data = fetch_data("filters")
    return filters_data if filters_data else {}


def load_filters():
    if "filters_data" not in st.session_state:
        st.session_state.filters_data = fetch_filters()


def get_filter_values():
    filters_data = st.session_state.filters_data
    categories = filters_data.get("categories", [])
    content_ratings = filters_data.get("content_ratings", [])
    min_rating = filters_data.get("min_rating", 0.0)
    max_rating = filters_data.get("max_rating", 5.0)
    min_price = filters_data.get("min_price", 0.0)
    max_price = filters_data.get("max_price", 100.0)
    min_installs = filters_data.get("min_installs", 0)
    max_installs = filters_data.get("max_installs", 10000000)
    return categories, content_ratings, min_rating, max_rating, min_price, max_price, min_installs, max_installs
