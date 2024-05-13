import streamlit as st

from dotenv import load_dotenv
import sys

from util import read_doc, get_response, add_to_history, add_doc, get_all_docnames

sys.path.append("../..")

history = []
env_key = ["OPENAI_API_KEY"]
load_dotenv()
model = None
default_doc="Select a document/context"
def render():
    libinfo = None
    with st.container():
        st.header("💬 Chat with Virtual Friend")
        if not "doclist" in st.session_state:
            st.session_state['doclist'] = get_all_docnames()
        col1,col2=st.columns([1,2],  gap="small")
        useDataRetrieval=False
        formatwithOpenAI = col1.checkbox("format with OpenAI",key="format_withOpenAI", value=True,  help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

        selected_doc = col2.selectbox("Context", key="selected_context", options=[default_doc]+st.session_state.doclist, index=None,   help=None, on_change=None, args=None, kwargs=None,   placeholder="Choose a document/context", disabled=False, label_visibility="hidden")
        query = st.text_input("x", key="user_query", label_visibility="hidden", placeholder="Ask questions about your Document:")
        current_history = history[::-1]
        #if not query:
            #query = "What is this document about?"
        if query:
            response = get_response( query , formatwithOpenAI,"" if selected_doc==default_doc else selected_doc)
            if response:
                add_to_history(query, response, history)
                st.write(response)
        if current_history:
            st.markdown("""---""")
            for h in current_history:
                st.markdown(f"###### :blue[{h[0]}]")
                st.markdown(f"{h[1]}")

    #
    # :high_brightness:{response}h)
