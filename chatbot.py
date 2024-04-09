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

        doc = st.file_uploader("Upload a Document (pdf or doc)", type=['pdf', 'doc', 'docx'])

        if doc:
            chunks = read_doc(doc)
            if not chunks:
                st.markdown(f"""
                :red[Unable to extract content from `{doc.name}`]
                Please try again with a different document.
                """)
                return
            add_doc(doc, chunks)
        docs=get_all_docnames()
        print(docs)
        #col1,col2=st.columns([1,2],  gap="small")
        useDataRetrieval=False
        #useDataRetrieval = col1.checkbox("Use Data Retrieval", value=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

        selected_doc = st.selectbox("Context", options=[default_doc]+docs, index=None,  key=None, help=None, on_change=None, args=None, kwargs=None,   placeholder="Choose a document/context", disabled=False, label_visibility="hidden")
        query = st.text_input("x", label_visibility="hidden", placeholder="Ask questions about your Document:")
        current_history = history[::-1]
        #if not query:
            #query = "What is this document about?"
        if query:
            response = get_response( query , useDataRetrieval,"" if selected_doc==default_doc else selected_doc)
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
