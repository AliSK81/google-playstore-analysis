import streamlit as st

from data_fetcher import fetch_apps
from filters import get_filters

st.subheader("Search Apps")

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
        show_editors_choice=True,
        show_limits=True
    )

filtered_df = fetch_apps(filters)
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.warning("No apps found with the current filters.")
