import sys
from streamlit_float import *
from streamlit_option_menu import option_menu
import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components

from chat_util import init_messages, get_user, get_friend_list, load_friend_messages, get_messages, get_response, \
    chat_page_init
from util import auth_decorator

sys.path.append("../../..")

st.set_page_config(layout="wide",page_title = "Chat")

chat_page_init()  # lots of magic happens here

friend_modal = Modal(
    "Friend Details",
    key="chat-modal",
    # Optional
    padding=20,  # default value
    max_width=744,  # default value
)
if friend_modal.is_open():
    with friend_modal.container():
        st.write("Text goes here")
        st.write("Some  text")
        st.button("close",on_click=lambda *a:friend_modal.close(rerun_condition=False))

def on_user_submit():
    query = st.session_state.user_query
    friend_id = st.session_state.selectedfriend
    if query and friend_id:
        st.session_state.waiting_response = True
        try:
            get_response(friend_id, query)
        except:
            pass
        st.session_state.waiting_response = False

@auth_decorator
def render():
    st.markdown(f"<div class='header-wrap'><div>%nbsp;.</div><div class='header-right'><img src='{st.session_state.usersession.get('imageUrl')}'/><span>{st.session_state.usersession.get('fullName', '&nbsp;')}</span></div></div>",unsafe_allow_html=True)

    init_messages()
    if not st.session_state.user:
        data = get_user()
        st.session_state.user = data

    with st.container():
        st.header("💬 Chat with Virtual Friend")
        border = True
        col1, col2 = st.columns([1, 3], )
        with col1:
            st.markdown("<div class='friend-list-inner'>&nbsp;</div>", unsafe_allow_html=True)
            st.markdown("<div class='full-length shaded'></div>", unsafe_allow_html=True)

            friends = get_friend_list()
            selected = option_menu("My Friends", [f.get("name") for f in friends],
                                   menu_icon="person-hearts", default_index=0)
            if selected:
                friend = [f for f in friends if f.get("name") == selected]
                if friend:
                    load_friend_messages(friend[0].get("id"))
        with col2:
            with st.container(border=border):
                friend = [f for f in get_friend_list() if f.get("id") == st.session_state.selectedfriend]
                if friend:
                    st.markdown(f"<div class='friend-label'></div>", unsafe_allow_html=True)
                    name_clicked = st.button(friend[0].get('name'))
                    if name_clicked:
                        friend_modal.open()
                with st.container():
                    st.chat_input(key='user_query', on_submit=on_user_submit)
                    button_b_pos = "1rem"
                    button_css = float_css_helper(width="2.2rem", bottom=button_b_pos, transition=0)
                    float_parent(css=button_css)

                if content := get_messages():
                    for c in content:
                        if c["from"] == "user":
                            with st.chat_message(name='user'):
                                st.markdown(c["message"])
                        else:
                            with st.chat_message(name=c["from"]):
                                st.markdown(c["message"])


render()