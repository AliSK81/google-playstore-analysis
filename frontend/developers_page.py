import time

import pandas as pd
import streamlit as st

from data_fetcher import fetch_developers, create_developer, update_developer, delete_developer


def create_developer_page():
    st.subheader("Create New Developer")
    name = st.text_input("Developer Name")
    email = st.text_input("Developer Email")
    if st.button("Create Developer"):
        data = create_developer(name, email)
        if data:
            st.success(f"Developer '{name}' created successfully!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Failed to create developer.")


def list_developers_page():
    st.subheader("Manage Developers")

    if "dev_page" not in st.session_state:
        st.session_state.dev_page = 1

    per_page = 10  # Number of developers per page
    response = fetch_developers(filters={'page': st.session_state.dev_page, 'per_page': per_page})

    if not response or "developers" not in response:
        st.warning("No developers found.")
        return

    developers = response["developers"]
    total_pages = response["total_pages"]

    if not developers:
        st.warning("No developers available.")
        return

    developer_df = pd.DataFrame(developers)

    col1, col2 = st.columns([6, 1])

    with col1:
        st.write("**Existing Developers**")

    with col2:
        st.write("**Actions**")

    for index, row in developer_df.iterrows():
        col1, col2, col3 = st.columns([9, 1, 1])

        with col1:
            st.write(f"👨‍💻 {row['name']} ({row['email']})")

        with col2:
            edit_button = st.button("✏️", key=f"edit_{row['id']}")
        with col3:
            delete_button = st.button("❌", key=f"delete_{row['id']}")

        if edit_button:
            st.session_state['edit_mode'] = True
            st.session_state['edit_id'] = row['id']
            st.session_state['edit_name'] = row['name']
            st.session_state['edit_email'] = row['email']
            st.rerun()

        if delete_button:
            delete_developer_page(row['id'])

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.dev_page > 1:
            if st.button("⬅️ Previous", key="prev_page"):
                st.session_state.dev_page -= 1
                st.rerun()
    with col3:
        if st.session_state.dev_page < total_pages:
            if st.button("Next ➡️", key="next_page"):
                st.session_state.dev_page += 1
                st.rerun()

    st.write(f"Page {st.session_state.dev_page} of {total_pages}")


def edit_developer_page():
    if "edit_mode" in st.session_state and st.session_state["edit_mode"]:
        st.subheader(f"Edit Developer: {st.session_state['edit_name']}")
        new_name = st.text_input("New Developer Name", value=st.session_state['edit_name'])
        new_email = st.text_input("New Developer Email", value=st.session_state['edit_email'])
        if st.button("Update Developer"):
            data = update_developer(st.session_state['edit_id'], new_name, new_email)
            if data:
                st.success(f"Developer '{st.session_state['edit_name']}' updated successfully!")
                time.sleep(1)
                del st.session_state['edit_mode']
                del st.session_state['edit_id']
                del st.session_state['edit_name']
                del st.session_state['edit_email']
                st.rerun()
            else:
                st.error("Failed to update developer.")


def delete_developer_page(developer_id):
    if delete_developer(developer_id):
        st.success("Developer deleted successfully!")
        time.sleep(1)
        st.rerun()
    else:
        st.error("Failed to delete developer.")


def developers_page():
    st.title("Developers Management")

    tab1, tab2 = st.tabs(["Create Developer", "Manage Developers"])

    with tab1:
        create_developer_page()

    with tab2:
        if "edit_mode" in st.session_state and st.session_state["edit_mode"]:
            edit_developer_page()
        else:
            list_developers_page()


developers_page()
