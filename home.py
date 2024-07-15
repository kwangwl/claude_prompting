import streamlit as st
from streamlit_option_menu import option_menu
import contact_center
import text_to_sql


# app
app_info = {
    "1. AI 고객 센터": contact_center,
    "2. Text to SQL": text_to_sql,
}
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

app = app_info[choose]
app.app()
