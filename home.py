import streamlit as st
from streamlit_option_menu import option_menu
from app import contact_center, text_to_sql, image_analyzer


# global config
st.set_page_config(page_title="FSI Gen AI 데모", layout='wide')

# sidebar
st.sidebar.title("FSI Gen AI 데모")
with st.sidebar:
    # https://icons.getbootstrap.com/
    choose = option_menu(
        menu_title=None,
        options=["1. AI 고객 센터", "2. Text to SQL", "3. Image Analyzer"],
        icons=['kanban', 'magic', 'image'],
        default_index=0,
    )

if choose == "1. AI 고객 센터":
    contact_center.app()
elif choose == "2. Text to SQL":
    text_to_sql.app()
elif choose == "3. Image Analyzer":
    image_analyzer.app()
