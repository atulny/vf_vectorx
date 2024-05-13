import streamlit as st

import sys

from util import read_doc, add_doc, get_all_docnames

sys.path.append("../..")



def render():
    with st.container():
        st.header("Context Documents")
        col1,col2=st.columns([1,2],  gap="small")
        if not "doclist" in st.session_state:
            st.session_state['doclist'] = get_all_docnames()
        do_chunking = col1.checkbox("Chunk document", key="do_chunking", value=True,  help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

        context = col2.text_input("Context", key="doc_context",label_visibility="visible", placeholder="Specify a context for this document")

        doc = st.file_uploader("Upload a Document (pdf or doc)", type=['pdf', 'doc', 'docx'])

        if doc:
            chunks = read_doc(doc, gettext=not do_chunking)
            if not chunks:
                st.markdown(f"""
                :red[Unable to extract content from `{doc.name}`]
                Please try again with a different document.
                """)
                return
            context_name = context
            if not context_name:
                context_name = doc.name[:-4]
            add_doc(context_name, chunks)
        st.session_state['doclist'] = get_all_docnames()
        st.subheader("Contexts")
        for d in st.session_state.doclist:
            st.markdown("- " + d)


