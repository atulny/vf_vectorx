import functools
import traceback

import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.switch_page_button import switch_page


def page_init():

    hide_streamlit_style = """
    <style>
    *, html {scroll-behavior: smooth !important;}
        #MainMenu {visibility: hidden;}
    
    #stDecoration  {visibility: hidden;}
    
    .stDeployButton{visibility: hidden;}
    
    header{display:none !important}
    
    [data-testid="stSidebarUserContent"]{padding-top:.8em;}
    
    [data-testid="block-container"]{padding-top:1em;}
    
    footer {visibility: hidden;}
    .block-container {padding:.5rem 4rem !important}
    
    .header-wrap{border-bottom:1px solid #ccc;background-color:#efefef;
        font-size:150%;padding:0 10px;position:fixed;top:1px;left:1px;width:100%;
        height:3rem;display:flex;
       flex-direction:row;justify-content:space-between;
    }
       
    .header-wrap .header-right img {height:28px;margin-right:5px;}
    
    [data-testid="stSidebarNav"] {
        background-size: 240px auto;
        background-repeat: no-repeat;
        background-position:center center !important;
        padding-top:370px !important;
        box-sizing:border;
        margin-top:-150px !important;
    }
    
    [data-testid='column']:has(.full-length){height:75vh !important}
    
    [data-testid='column']:has(.shaded){background-color:#f0f2f6;}
    
    .block-container:has(.header-wrap) > [data-testid='stVerticalBlockBorderWrapper'] >div > [data-testid='stVerticalBlock']{
      margin-top:-200px
    } 
      
    .element-container > .stMarkdown > [data-testid='stMarkdownContainer'] > .p__h{
        overflow;hidden;height:0  !important;max-height:0  !important;margin:0  !important;padding:0 !important;
    }
    
    .block-container  .block-container{
        padding:0 !important
    }
    
    [data-testid="stSidebarNavLink"]{
       font-size:150%;
     }
    .main-wrap{
        background-color:#f0f2f6;
        padding:1rem 2rem .5rem 2rem;
    }
    .main-wrap .main-wrap-header{
             font-size:180%;
    }
    .main-wrap .main-wrap-header span{
         color:#aaa;
         text-transform: capitalize;
    }
    .main-wrap .main-wrap-tips{
        font-size90%;
        color:#666;
        font-style: italic;
    }
    .main-wrap .main-wrap-sub-header{
             font-size:110%;
    }
     .element-container:has(.main-wrap) + .element-container{
       background-image:url("./asset/hero-1-5.png")
     }
    </style>

    """
    if not "usersession" in st.session_state:
        st.session_state.usersession = {"status": 'Unknown'}
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    logo_url = './asset/icon3.png'
    add_logo(logo_url)

def auth_decorator(fn):

    @functools.wraps(fn)
    def check_if_logged_in(*a,**kw):
        if st.session_state.usersession.get("status") != "active":
            switch_page("Home")
        else:
            return fn(*a,**kw)
    return check_if_logged_in
def error_decorator(fn):
    @functools.wraps(fn)
    def error_wrapped(*a,**kw):
        try:
            return fn(*a,**kw)
        except Exception as e:
            error = str(traceback.format_exc())

            print(error)
            st.error(f"An Error Occurred  {str(e)}")
    return error_wrapped
def isLoggedIn():
    return True if st.session_state.usersession.get("status") == "active" else False
def get_auth():
    token = st.session_state.usersession.get("token")
    return   f"Bearer {token}" if token else None
# import openai
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.llms import OpenAI
#import os
# from langchain.callbacks import get_openai_callback
# from langchain.chains.question_answering import load_qa_chain
# from openai.types.chat import ChatCompletionMessageParam
# from pypdf import PdfReader
# from docx2txt import docx2txt
# import chromadb
# from chromadb.config import Settings

# client = [None]
# model_name = "gpt-4"
# def get_db():
#     if client[0] is None:
#         client[0] = chromadb.PersistentClient(settings=Settings(allow_reset=True, anonymized_telemetry=False))
#
#     return client[0]
#
#
# DBNAME = "myvectors"
# COLLECTIONS={}
# def get_collection(name=None):
#     if not name:
#         name = DBNAME
#
#     collection = COLLECTIONS.get(name)
#     if collection is None:
#         client = get_db()
#
#         collection = client.get_or_create_collection( name=name)
#         COLLECTIONS[name] = collection
#     return collection
#
# def build_prompt(query: str, context: List[str],formatwithOpenAI:bool) -> List[ChatCompletionMessageParam]:
#     """
#     Builds a prompt for the LLM. #
#
#     """
#     content="Break your answer up into nicely readable paragraphs."
#     if formatwithOpenAI and context:
#         content2 = """
#     Pretend you are a virtual friend whose name is Stephanie,
#     remember you are not a virtual assistant,
#     you are a friend. Use the document as a context,
#     write a response to continue the conversation.
#     Do not mention context. Keep the response short and ask probing questions:
#         """
#         content="""
# Pretend you are a virtual friend whose name is Stephanie,
# remember you are not a virtual assistant, you are a friend.
# Your goal is to help the user improve their mental health.
# Write a response to continue this conversation,
# introduce yourself if not already discussed,
# do not ask more than one question,
# make sure to answer any question the user has asked, use the document to help come up with answer:
#
# Break your answer up into nicely readable paragraphs.
#         """
#
#     system: ChatCompletionMessageParam = {
#         "role": "system",
#         "content": content
#     }
#     user: ChatCompletionMessageParam = {
#         "role": "user",
#         "content": f"The question is {query}. Here is all the context you have:"
#         f'{(" ").join(context)}',
#     }
#
#     return [system, user]
#
#
# def get_chatGPT_response(query: str, context: List[str], model_name: str,formatwithOpenAI:bool) -> str:
#     """
#     Queries the GPT API to get a response to the question.
#     """
#     response = openai.chat.completions.create(
#         model=model_name,
#         messages=build_prompt(query, context,formatwithOpenAI),
#     )
#
#     return response.choices[0].message.content  # type: ignore
#
# def get_response(  query , formatwithOpenAI=False, docname=None):
#     """
#     returns  response to the query
#     """
#     docs = []
#
#     if docname:
#         print("loading DB")
#         collection = get_collection()
#         where_criteria = {"doc": docname}
#         print("searching")
#         result = collection.query(query_texts=[query], n_results=1, include=["documents", 'distances', ],where=where_criteria)
#         docs = result.get("documents")
#         if not formatwithOpenAI:
#             return "\n".join((docs[0] if docs else []))
#
#     print("formatting with Model")
#     response = get_chatGPT_response(query, docs[0] if docs  else [], model_name, formatwithOpenAI)
#     print("done")
#     return response
# def add_doc(doc, chunks):
#     store_name = doc  #.name[:-4]
#     collection = get_collection()
#     if type(chunks) is not list:
#         chunks=[chunks]
#     try:
#         collection.upsert(documents=chunks, metadatas=[{"doc":store_name}]*len(chunks),ids=list(map(lambda tup: f"{store_name}_{tup[0]}", enumerate(chunks))))
#     except Exception as e:
#         print(e)
#
#
# def get_all_docnames():
#     collection = get_collection()
#
#     all_metadatas = collection.get(include=["metadatas"]).get('metadatas')
#     distinct_keys = set([x.get('doc') for x in all_metadatas])
#     return list(distinct_keys)
# def read_doc(doc, gettext=False):
#     text = ""
#     if not doc:
#         return
#     if doc.name.endswith("pdf"):
#         pdf_reader = PdfReader(doc)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     else:
#         text = docx2txt.process(doc)
#     if gettext:
#        return text
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200,
#         length_function=len
#     )
#     chunks = text_splitter.split_text(text=text)
#     return chunks
#
#
# def add_to_history(query, response, context,history):
#     # tolog = f"""
#     # :question:{query}
#     #
#     # :high_brightness:{response}
#     # _________________
#     # """
#     #if not tolog in history:
#     history.append((context,query,response))
#
#
# def get_sources(answer, doc_index):
#     """Retrieves the docs that were used to answer the question the generated answer."""
#
#     source_keys = [s for s in answer.split("SOURCES: ")[-1].split(", ")]
#
#     source_docs = []
#     for doc in doc_index:
#         if doc.metadata["source"] in source_keys:
#             source_docs.append(doc)
#     return source_docs
