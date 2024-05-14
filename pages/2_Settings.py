import datetime
from dataclasses import Field
from typing import Optional
from pydantic import BaseModel
from streamlit_option_menu import option_menu
import streamlit as st
import streamlit_pydantic as sp

from chat_util import get_user
from util import page_init, auth_decorator

st.set_page_config(layout="wide",page_title = "Settings")

class Location(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "USA"
class UserProfile(BaseModel):
    #user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob_ts: Optional[int] = None
    gender: Optional[str] = None
    location : Optional[Location]=None

page_init()
@auth_decorator
def render():
    if "selected_setting" not in st.session_state:
        st.session_state.selected_setting = ""
    col1,col2 = st.columns([1,4],)
    with col1:
        st.markdown("<div class='full-length shaded'></div>", unsafe_allow_html=True)
        selected = option_menu("Settings", ["My Profile","Privacy Message"],
                               menu_icon="gear",icons=["credit-card-2-front"], default_index=0)
        if selected:
            st.session_state.selected_setting = selected

    with col2:
            st.subheader("Privacy Message")
            if selected == "Privacy Message":
                st.markdown("""
                Your privacy is our priority. You can be sure that your information and conversations stay between you 
                and your virtual friends.
                
                You get to choose what you share, how you show up online, or who you talk to.
                
                We add additional layers of protection to all of your conversations
                 and ensure that the data is stored in our secure databases.
                """)
            elif selected == "My Profile":
                with st.form(key="pydantic_form1"):
                    # Render input model -> input data is accesible via st.session_state["input_data"]
                    data = {}
                    if "user" not in st.session_state:
                        data = get_user()
                        st.session_state.user = data
                    else:
                        data = st.session_state.get("user",{})
                    userprofile=UserProfile(**data)
                    sp.pydantic_input(model=userprofile, key="user")
                    submit_button = st.form_submit_button(label="Submit")
                pass

render()