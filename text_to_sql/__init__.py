import streamlit as st
# from . import summary

# menu info
menu_info = {
#     "요약": summary,
}


def app():
    menu = st.sidebar.selectbox("Menu", list(menu_info.keys()))
    menu_app = menu_info[menu]
    menu_app.app()
