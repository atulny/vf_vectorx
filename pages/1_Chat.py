import sys
from time import sleep
from typing import Optional

from pydantic import BaseModel
from streamlit_float import *
from streamlit_option_menu import option_menu
import streamlit as st

from chat_util import init_messages, get_user, get_friend_list, load_friend_messages, get_messages, get_response, \
    chat_page_init, get_friend_profile
from util import auth_decorator
from typing import Annotated
from streamlit_pydantic_form import st_auto_form, widget

sys.path.append("../../..")

st.set_page_config(layout="wide", page_title="Chat")

chat_page_init()  # lots of magic happens here

class Location(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "USA"
class FriendProfile(BaseModel):
    #id: Optional[str] = None
    name: Optional[str] = None
    dob_ts: Optional[int] = None
    gender: Optional[str] = None
    description: Optional[str] = None

    #preferred_pronoun: Optional[str] = None
    #living_situation: Optional[str] = None
    #get_friend_profileinteraction_frequency: Optional[str] = None
    interests: Optional[list[str]] = []
    #hobbies: Optional[list[str]] = []
    #reminders_preference: Optional[bool] = False
    #created_by: Optional[str] = None
    #created_on: Optional[datetime.datetime] = None
    location: Optional[Location] = None
    #created_by_system: Optional[bool] = None
    #is_public: Optional[bool] = False

# new_friend_modal1 = Modal(
#     "Create Friend",
#     key="new-friend-modal",
#     # Optional
#     padding=10,  # default value
#     max_width=744,  # default value
# )
# if new_friend_modal1.is_open():
#     with new_friend_modal1.container():
#         data = {}
#         friendprofile = FriendProfile(**data)
#         sp.pydantic_input(model=friendprofile, key="newfriend")
#         submit_button = st.form_submit_button(label="Submit")
#         st.button("close", on_click=lambda *a: new_friend_modal1.close(rerun_condition=False))
#
# friend_modal = Modal(
#     "Friend Details",
#     key="friend-modal",
#     # Optional
#     padding=10,  # default value
#     max_width=744,  # default value
# )
# if friend_modal.is_open():
#     with friend_modal.container():
#         st.write("Friend Profile")
#         data = get_friend_profile(st.session_state.selectedfriend)
#         if data.get("interests"):
#             data["interests"] = data["interests"].split(",")
#         friendprofile = FriendProfile(**data)
#         sp.pydantic_input(model=friendprofile, key="friend")
#         submit_button = st.form_submit_button(label="Submit")
#         st.button("close", on_click=lambda *a: friend_modal.close(rerun_condition=False))

@st.experimental_dialog("Friend Profile")
def show_friend_profile(friend_id):
    #import streamlit_pydantic as sp

    data = get_friend_profile(friend_id)
    if data.get("interests"):
        data["interests"] = data["interests"].split(",")
    friendprofile = FriendProfile(**data)
    with st_auto_form("form_4", model=FriendProfile) as  form2:
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.rerun()

    #sp.pydantic_input(model=friendprofile, key="friend")
    # if st.form_submit_button(label="Submit"):
    #     #st.button("close", on_click=lambda *a: new_friend_modal1.close(rerun_condition=False))
    #     st.rerun()
@st.experimental_dialog("Friend Profile")
def new_friend_profile():
    import streamlit_pydantic as sp

    data = {}
    friendprofile = FriendProfile(**data)
    sp.pydantic_input(model=friendprofile, key="newfriend")
    if st.form_submit_button(label="Submit"):
        #st.button("close", on_click=lambda *a: new_friend_modal1.close(rerun_condition=False))
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
            data = get_user()
            st.session_state.user = data


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