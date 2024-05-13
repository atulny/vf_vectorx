from time import sleep

import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_js_eval import streamlit_js_eval

from util import page_init

st.set_page_config(layout="wide",page_title = "Junctions: Virtual Friends")
#query_params = st.query_params
#print(query_params)
from clerkjs import clerkjs

page_init()
with st.container():
    st.header("Junctions: Virtual Friends")
    with st.container():
        st.subheader(f"{st.session_state.usersession.get('fullName','User')} : {st.session_state.usersession['status']}")

        data:dict = clerkjs("Junctions")
        if data:
            current_status = st.session_state.usersession.get("status")
            if data.get("status") != current_status:
                print(f"session_data before {data.get('status')} {current_status}")

                st.session_state.usersession = data.copy()
                try:
                    if current_status == "active" or current_status == "No session":
                        print(f"refresing {st.session_state.usersession.get('status')}")
                        ## HACK ALERT
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
                    #sleep(2)
                    #st.rerun()
                except:
                    pass
            #print(st.session_state.usersession)
            ## HACK ALERT
            # reload the page if the main is loaded in the iframe after redirect
            streamlit_js_eval(js_expressions="self.parent != top && top.location.reload()")

    st.markdown("<br/><a href='/Chat' target='_self'>Start Chatting</a>", unsafe_allow_html=True)