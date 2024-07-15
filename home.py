import streamlit as st
from streamlit_option_menu import option_menu
import contact_center.app as contact_center_app
import text_to_sql


# global config
st.set_page_config(page_title="FSI Gen AI 데모", layout='wide')

# sidebar
st.sidebar.title("FSI Gen AI 데모")
with st.sidebar:
    # https://icons.getbootstrap.com/
    choose = option_menu(
        menu_title=None,
        options=["1. AI 고객 센터", "2. Text to SQL"],
        icons=['kanban', 'magic'],
        default_index=0,
    )

if choose == "1. AI 고객 센터":
    contact_center_app.app()
elif choose == "2. Text to SQL":
    contact_center_app.app()