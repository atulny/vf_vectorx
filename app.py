import streamlit as st
from PIL import Image
#from dotenv import load_dotenv

from chatbot import render
from doc_upload import render as render_upload

#from config import init

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
#stDecoration  {visibility: hidden;}
.stDeployButton{visibility: hidden;}
.stTextInput label[aria-hidden="true" {display:none !important}
.stSelectbox label[aria-hidden="true"] {display:none !important}
.block-container{padding-top:1rem !important}
[data-testid="stSidebarUserContent"]{padding-top:.8em;}
[data-testid="block-container"]{padding-top:1em;}
footer {visibility: hidden;}
</style>

"""

st.set_page_config(layout="wide")
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
tab1,tab2 = st.tabs(["❊ Ask me", "Documents"])
#load_dotenv()
#init()


with tab1:
    render()
with tab2:
    render_upload()