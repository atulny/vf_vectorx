import base64
from time import sleep

import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_js_eval import streamlit_js_eval

from util import page_init

st.set_page_config(layout="wide",page_title = "Junctions: Virtual Friends")
#query_params = st.query_params
#print(query_params)
from clerkjs import clerkjs


def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.

    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"

    st.markdown(
        f"""
         <style>
         .element-container:has(.main-wrap) + .element-container {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
              background-position: left 60px;
              background-size:contain;
                background-repeat: no-repeat;

         }}
         </style>
         """,
        unsafe_allow_html=True
    )
page_init()
with st.container():
    st.header("Junctions: Virtual Friends")
    with st.container():
        st.markdown(f"""
                    <div class='main-wrap'>
                    <div class='main-wrap-header'>WELCOME, {st.session_state.usersession.get('fullName','User')} <span>{st.session_state.usersession['status']}</span></div>
                    <div class='main-wrap-sub-header'>Friendship, on your terms, with a virtual friend</div>
                    <div class='main-wrap-tips'>Click on the icon below for Login status</div>
                    </div>
                    """,unsafe_allow_html=True)
        data:dict = clerkjs({"clerkPubKey": "pk_test_cHJpbWUtc2hyaW1wLTQwLmNsZXJrLmFjY291bnRzLmRldiQ"})
        if data:
            current_status = st.session_state.usersession.get("status")
            if data.get("status") != current_status:
                st.session_state.usersession = data.copy()
                try:
                    if current_status == "active" or current_status == "No session":
                        ## HACK ALERT
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
                except:
                    pass
            #print(st.session_state.usersession)
            ## HACK ALERT
            # reload the page if the main is loaded in the iframe after redirect
            st.subheader("MISSION")
            st.markdown("""Chat app for people to communicate with a virtual friend when they are feeling lonely or just need someone to talk to. Virtual friend demographics can be random or personalized. Y"
                            our virtual friend gets to know you and remembers to check-in on occasion. Powered by LLM.""")
            streamlit_js_eval(js_expressions="self.parent.parent != top && top.location.reload()")
            set_bg_hack("./asset/hero-1-5.png")
            streamlit_js_eval(js_expressions=f"""
                let fn = ()=>{{         
                    let doc = top.document.querySelector('.element-container:has(.main-wrap) + .element-container iframe')
                    if(doc && doc.contentDocument && doc.contentDocument.body){{
                        doc.contentDocument.body.style.backgroundColor = 'transparent';
                    }}  else {{
                        setTimeout(fn, 500)
                    }}
                }};
                setTimeout(fn, 500);
            """)
