# import datetime
# from dataclasses import Field
# from typing import Optional
#from pydantic import BaseModel
from streamlit_option_menu import option_menu
import streamlit as st

from chat_util import get_user, refresh_user_data
from form_util import render_fields
from util import page_init, auth_decorator

st.set_page_config(layout="wide",page_title = "Settings")
 

User_Profile=[
    {"name":"first_name","type": str},
    {"name": "last_name", "type": str},
    {"name": "dob_ts", "type": str},
    {"name": "gender", "type": str},
    {"name": "location", "type": str}

]
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
                form_key = "my_profile"
                with st.form(key=form_key):
                    # import streamlit_pydantic as sp
                    # Render input model -> input data is accesible via st.session_state["input_data"]
                    data = {}
                    if "user" not in st.session_state:
                        refresh_user_data()
                    else:
                        data = st.session_state.get("user",{})
                    # userprofile=UserProfile(**data)
                    render_fields(User_Profile, data, form_key)
                    if st.form_submit_button("Submit"):
                        pass
                    # sp.pydantic_input(model=userprofile, key="user")
                    #submit_button = st.form_submit_button(label="Submit")
                pass

render()
