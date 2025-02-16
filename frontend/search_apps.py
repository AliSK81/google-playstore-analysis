import pandas as pd
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
        show_editors_choice=True
    )

col1, col2 = st.columns(2)
with col1:
    page = st.number_input("Page", min_value=1, step=1, value=1)
with col2:
    per_page = st.number_input("Results per Page", min_value=1, max_value=100, value=10)

filters["page"] = page
filters["per_page"] = per_page

response = fetch_apps(filters)

if "apps" in response:
    apps = pd.DataFrame(response["apps"])
    total_apps = response["total_apps"]
    total_pages = response["total_pages"]

    if not apps.empty:
        st.dataframe(apps)

        st.write(f"Showing page {page} of {total_pages} (Total results: {total_apps})")


else:
    st.warning("No apps found with the current filters.")
