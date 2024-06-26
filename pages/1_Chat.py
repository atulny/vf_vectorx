import sys
# from time import sleep
from typing import Optional

#from pydantic import BaseModel
from streamlit_float import *
from streamlit_option_menu import option_menu
import streamlit as st

from chat_util import init_messages,  get_friend_list, load_friend_messages, get_messages, get_response, \
    chat_page_init, get_friend_profile, create_friend, refresh_user_data
from form_util import   render_fields
from util import auth_decorator
#from typing import Annotated
#from streamlit_pydantic_form import st_auto_form, widget

sys.path.append("../../..")

st.set_page_config(layout="wide", page_title="Chat")

chat_page_init()  # lots of magic happens here
 
Friend_profile = [
    {"name":"name", "type":str},
    {"name": "dob_ts", "type": str},
    {"name": "gender", "type": str},
    {"name": "description", "type": str},
    {"name": "interests", "type": str},
    {"name": "location", "type": str}

]
 

@st.experimental_dialog("Friend Profile")
def show_friend_profile(friend_id):
    data = get_friend_profile(friend_id)
    form_key="friend_profile"
    with st.form(form_key):
        render_fields(Friend_profile, data,form_key)

        if st.form_submit_button("Submit"):
            ## collect dtata and save
            st.rerun()

@st.experimental_dialog("Friend Profile")
def new_friend_profile():
    data = {}
    if st.button("Surprise Me"):
        create_friend({"surprise_me":True})
        refresh_user_data()
        st.rerun()

    form_key = "new_friend_profile"
    with st.form(form_key):
        render_fields(Friend_profile, data, form_key)
        if st.form_submit_button("Submit"):
            ## collect data and save
            st.rerun()


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
        st.markdown(
            f"<div class='header-wrap'><div>%nbsp;.</div><div class='header-right'><img src='{st.session_state.usersession.get('imageUrl')}'/><span>{st.session_state.usersession.get('fullName', '&nbsp;')}</span></div></div>",
            unsafe_allow_html=True)

        init_messages()
        if not st.session_state.user:
            refresh_user_data()


        with st.container():
            st.header("💬 Chat with Virtual Friend")
            border = True
            col1, col2 = st.columns([1, 3], )
            with col1:
                st.markdown("<div class='p__h friend-list-inner'>&nbsp;</div>", unsafe_allow_html=True)
                st.markdown("<div class='p__h full-length shaded'></div>", unsafe_allow_html=True)
                name_clicked = st.button("[+] Add a Friend")
                if name_clicked:
                    new_friend_profile( )
                    #new_friend_modal1.open()
                friends = get_friend_list()
                if friends:
                    icons = ["file-earmark-person"] * len(friends)
                    selected = option_menu("My Friends", options=[f.get("name") for f in friends], icons=icons,
                                           menu_icon="person-hearts",
                                           default_index=0)
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
                            show_friend_profile(st.session_state.selectedfriend)
                            pass
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
