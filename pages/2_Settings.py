from streamlit_option_menu import option_menu
import streamlit as st

from util import page_init, auth_decorator

st.set_page_config(layout="wide",page_title = "Settings")

page_init()
@auth_decorator
def render():
    if "selected_setting" not in st.session_state:
        st.session_state.selected_setting = ""
    col1,col2 = st.columns([1,4],)
    with col1:
        st.markdown("<div class='full-length shaded'></div>", unsafe_allow_html=True)
        selected = option_menu("Settings", ["My Profile","Privacy Message","Logout"],
                               menu_icon="gear",icons=["credit-card-2-front"], default_index=0)
        if selected:
            st.session_state.selected_setting = selected

    with col2:
        st.title(st.session_state.selected_setting )




render()