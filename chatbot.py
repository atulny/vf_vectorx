import streamlit as st

from dotenv import load_dotenv
import sys

from util import read_doc, get_response, add_to_history, add_doc

sys.path.append("../..")

history = []
env_key = ["OPENAI_API_KEY"]
load_dotenv()
model = None

def render():
    libinfo = None
    with st.container():
        st.header("💬 Chat with a document")

        doc = st.file_uploader("Upload a Document (pdf or doc)", type=['pdf', 'doc', 'docx'])

        if doc:
            chunks = read_doc(doc )
            if not chunks:
                st.markdown(f"""
                :red[Unable to extract content from `{doc.name}`]
                Please try again with a different document.
                """)
                return
            add_doc(doc, chunks)
        useDataRetrieval = st.checkbox("Use Data Retrieval", value=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
        query = st.text_input("x", label_visibility="hidden", placeholder="Ask questions about your Document:")
        current_history = history[::-1]
        if not query:
            query = "What is this document about?"
        if query:
            response = get_response( query)
            if response:
                add_to_history(query, response, history)
                st.write(response)
                if current_history:
                    st.markdown("""---""")
                    st.markdown("".join(current_history))
