import base64
import os
from time import sleep

import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_js_eval import streamlit_js_eval

from util import page_init

st.set_page_config(layout="wide",page_title = "Junctions: Virtual Friends")
query_params = st.query_params
print(query_params.get("noreload"))
from clerkjs import clerkjs
from streamlit_elements import elements, mui, html


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
                opacity:.6;

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
        data:dict = clerkjs({"clerkPubKey": os.environ.get("CLERKPUBKEY")})
        if data:
            current_status = st.session_state.usersession.get("status")
            if data.get("status") != current_status:
                st.session_state.usersession = data.copy()
                try:
                    if current_status == "active" or current_status == "No session":
                        ## HACK ALERT
                        streamlit_js_eval(js_expressions="top.location.reload()")
                except:
                    pass

            st.subheader("MISSION")
            st.markdown("""Chat app for people to communicate with a virtual friend when they are feeling lonely or just 
             need someone to talk to. Virtual friend demographics can be random or personalized. 
                      Your virtual friend gets to know you and remembers to check-in on occasion. Powered by LLM.""")

            ## HACK ALERT
            # reload the page if the main is loaded in the iframe after redirect
            # for deployment in streamlit( coz it runs in an iframe
            #streamlit_js_eval(js_expressions="(self.parent.parent.parent != self.parent.parent  ) && top.location.reload()")

            # otherwise
            streamlit_js_eval(js_expressions="(self.parent.parent != self.parent  ) && top.location.reload()")




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
