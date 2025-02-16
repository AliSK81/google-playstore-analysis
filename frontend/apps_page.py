import time

import pandas as pd
import streamlit as st

from data_fetcher import fetch_apps, create_app, update_app, delete_app


def create_app_page():
    st.subheader("Create New App")
    app_name = st.text_input("App Name")
    app_id = st.text_input("App ID")
    category_id = st.number_input("Category ID", min_value=1, max_value=100)
    developer_id = st.number_input("Developer ID", min_value=1, max_value=100)
    rating = st.number_input("Rating", min_value=0.0, max_value=5.0, step=0.1)
    free = st.checkbox("Free")
    if st.button("Create App"):
        data = create_app(app_id, app_name, category_id, developer_id, rating, free)
        if data:
            st.success(f"App '{app_name}' created successfully!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Failed to create app.")


def list_apps_page():
    st.subheader("Manage Apps")

    if "app_page" not in st.session_state:
        st.session_state.app_page = 1

    per_page = 10  # Number of apps per page
    response = fetch_apps(filters={'page': st.session_state.app_page, 'per_page': per_page})

    if not response or "apps" not in response:
        st.warning("No apps found.")
        return

    apps = response["apps"]
    total_pages = response["total_pages"]

    if not apps:
        st.warning("No apps available.")
        return

    app_df = pd.DataFrame(apps)

    col1, col2 = st.columns([6, 1])

    with col1:
        st.write("**Existing Apps**")

    with col2:
        st.write("**Actions**")

    for index, row in app_df.iterrows():
        col1, col2, col3 = st.columns([9, 1, 1])

        with col1:
            st.write(f"📱 {row['app_name']} ({row['app_id']})")

        with col2:
            edit_button = st.button("✏️", key=f"edit_{row['id']}")
        with col3:
            delete_button = st.button("❌", key=f"delete_{row['id']}")

        if edit_button:
            st.session_state['edit_mode'] = True
            st.session_state['edit_id'] = row['id']
            st.session_state['edit_name'] = row['app_name']
            st.session_state['edit_app_id'] = row['app_id']
            st.rerun()

        if delete_button:
            delete_app_page(row['id'])

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.app_page > 1:
            if st.button("⬅️ Previous", key="prev_page"):
                st.session_state.app_page -= 1
                st.rerun()
    with col3:
        if st.session_state.app_page < total_pages:
            if st.button("Next ➡️", key="next_page"):
                st.session_state.app_page += 1
                st.rerun()

    st.write(f"📄 Page {st.session_state.app_page} of {total_pages}")


def edit_app_page():
    if "edit_mode" in st.session_state and st.session_state["edit_mode"]:
        st.subheader(f"Edit App: {st.session_state['edit_name']}")
        new_name = st.text_input("New App Name", value=st.session_state['edit_name'])
        new_app_id = st.text_input("New App ID", value=st.session_state['edit_app_id'])
        if st.button("Update App"):
            data = update_app(st.session_state['edit_id'], new_name, new_app_id)
            if data:
                st.success(f"App '{st.session_state['edit_name']}' updated successfully!")
                time.sleep(1)
                del st.session_state['edit_mode']
                del st.session_state['edit_id']
                del st.session_state['edit_name']
                del st.session_state['edit_app_id']
                st.rerun()
            else:
                st.error("Failed to update app.")


def delete_app_page(app_id):
    if delete_app(app_id):
        st.success("App deleted successfully!")
        time.sleep(1)
        st.rerun()
    else:
        st.error("Failed to delete app.")


def apps_page():
    st.title("Apps Management")

    tab1, tab2 = st.tabs(["Create App", "Manage Apps"])

    with tab1:
        create_app_page()

    with tab2:
        if "edit_mode" in st.session_state and st.session_state["edit_mode"]:
            edit_app_page()
        else:
            list_apps_page()


apps_page()
