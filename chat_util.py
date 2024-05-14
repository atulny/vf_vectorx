import requests
import json
import streamlit as st
from streamlit_float import *

from util import page_init, get_auth, error_decorator

BASE_URL="https://api.junctions.com"
def chat_page_init():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user" not in st.session_state:
        st.session_state.user = None
    if "selectedfriend" not in st.session_state:
        st.session_state.selectedfriend = ""
    if "waiting_response" not in st.session_state:
        st.session_state.waiting_response = False

    page_init()
    hide_streamlit_style = """
    <style>
    [data-testid="stHorizontalBlock"]     {
        position: relative !important;height: 100% !important;
    }
    
    .stChatMessage {
            max-width:85%;
            min-width:85%;

    }
    .stChatMessage:has([data-testid="chatAvatarIcon-user"]){
        flex-direction: row-reverse !important;
        max-width:80%;
        align-self: flex-end;
    }
    
    .stChatMessage:has([data-testid="chatAvatarIcon-user"]) p{
        text-align: right !important;
    }
    
    [data-testid="column"] > [data-testid="stVerticalBlockBorderWrapper"] > div >[data-testid="stVerticalBlock"]>[data-testid="stVerticalBlockBorderWrapper"] 
    {
        max-height: 85vh!important;height: calc(100vh - 200px) !important;
        position:relative;overflow:auto;border:1px solid #ccc;
    }
        
    .element-container:has(.friend-label) + .element-container:has(button) button{
        text-align:left;
        margin:0;border:0 !important;
        border:none;
        padding:0;
        margin-top: -30px;
        min-width: 50vw;
        font-size:20px !important;
        border-bottom:1px solid #666 !important;
        position:fixed;
        display:block !important;
        background-color:white;
        z-index:5;
        opacity:.7;
     }
     .element-container:has(.friend-label) + .element-container:has(button) button p{
         font-size:200% !important;padding:0;
                 font-weight:bold !important;
                         background-color:white;
    }
    
    
    [data-testid="column"]:has(.friend-list-inner){
        padding:.5rem;
        max-height: 85vh!important;height: calc(100vh - 200px) !important;
    }
    
    </style>

    """
    js = f"""
    <script>
        function scroll(messagecount){{
            var els = parent.document.querySelectorAll('.stChatMessage')
            var last = els[els.length - 1]
            if (last){{
                last.scrollIntoViewIfNeeded()
            }}
            }}

        scroll({len(st.session_state.messages)} )
        setTimeout(scroll,500)
        setTimeout(scroll,1000)

    </script>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.components.v1.html(js)
    float_init(theme=True, include_unstable_primary=False)

def get_messages():
    return st.session_state.messages

def init_messages():
 return
@error_decorator
def get_response(friend_id,message):
    auth = get_auth()
    data = {"friend_id": friend_id,"query":message}
    response = requests.post(f"{BASE_URL}/generate",
                             headers={"Content-Type": "application/json", "Accept": "application/json","Authorization":auth},
                             data=json.dumps(data))
    result = response.json()
    conversation = result.get("conversation")
    st.session_state['messages'] = conversation

@error_decorator
def load_friend_messages(friend_id):
    auth = get_auth()
    st.session_state.selectedfriend = friend_id
    data = {"friend_id":friend_id}
    response = requests.post(f"{BASE_URL}/generate",
            headers={"Content-Type":"application/json", "Accept": "application/json","Authorization":auth},
                data=json.dumps(data) )
    result =  response.json()
    conversation = result.get("conversation")
    st.session_state['messages'] = conversation

    return conversation

@error_decorator
def get_friend_list():
    user = st.session_state.user
    friends = user.get("friend_ids")  if user else []
    return friends
@error_decorator
def get_user():
    auth = get_auth()
    print(f"############################ {auth} ############################")
    result = requests.get(f"{BASE_URL}/user_profile",headers={"Authorization":auth,"Accept": "application/json"})
    result = result.json()
    user =  result.get("data")
    return user