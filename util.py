#import pickle
from typing import List

import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
#import os
from langchain.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
from openai.types.chat import ChatCompletionMessageParam
from pypdf import PdfReader
from docx2txt import docx2txt
import chromadb
from chromadb.config import Settings

client = [None]
model_name = "gpt-4"
def get_db():
    if client[0] is None:
        client[0] = chromadb.PersistentClient(settings=Settings(allow_reset=True, anonymized_telemetry=False))

    return client[0]


DBNAME = "myvectors"
COLLECTIONS={}
def get_collection(name=None):
    if not name:
        name = DBNAME

    collection = COLLECTIONS.get(name)
    if collection is None:
        client = get_db()

        collection = client.get_or_create_collection( name=name)
        COLLECTIONS[name] = collection
    return collection

def build_prompt(query: str, context: List[str],useDataRetrieval:bool) -> List[ChatCompletionMessageParam]:
    """
    Builds a prompt for the LLM. #

    """
    content="Break your answer up into nicely readable paragraphs."
    if useDataRetrieval:
        content="""
I am going to ask you a question, which I would like you to answer
based only on the provided context, and not any other information.
Refer to speaker as You.
If there is not enough information in the context to answer the question,
say "I am not sure", then try to make a guess.
Break your answer up into nicely readable paragraphs.
        """

    system: ChatCompletionMessageParam = {
        "role": "system",
        "content": content,
    }
    user: ChatCompletionMessageParam = {
        "role": "user",
        "content": f"The question is {query}. Here is all the context you have:"
        f'{(" ").join(context)}',
    }

    return [system, user]


def get_chatGPT_response(query: str, context: List[str], model_name: str,useDataRetrieval:bool) -> str:
    """
    Queries the GPT API to get a response to the question.
    """
    response = openai.chat.completions.create(
        model=model_name,
        messages=build_prompt(query, context,useDataRetrieval),
    )

    return response.choices[0].message.content  # type: ignore

def get_response(  query , useDataRetrieval=False, docname=None):
    """
    returns  response to the query
    """
    docs = []
    if docname:
        useDataRetrieval = True
    if useDataRetrieval:
        collection = get_collection()
        wherecriteria={}
        if docname:
            wherecriteria = {"doc": docname}
        result = collection.query(query_texts=[query], n_results=1, include=["documents", 'distances', ],where=wherecriteria)
        docs = result.get("documents")
        #return "\n".join((docs[0] if docs else []))
    response = get_chatGPT_response(query, docs[0] if docs  else [], model_name,useDataRetrieval)
    return response
def add_doc(doc, chunks):
    store_name = doc.name[:-4]
    collection = get_collection()
    if type(chunks) is not list:
        chunks=[chunks]
    try:
        collection.upsert(documents=chunks, metadatas=[{"doc":store_name}]*len(chunks),ids=list(map(lambda tup: f"{store_name}_{tup[0]}", enumerate(chunks))))
    except Exception as e:
        print(e)


def get_all_docnames():
    collection = get_collection()

    all_metadatas = collection.get(include=["metadatas"]).get('metadatas')
    distinct_keys = set([x.get('doc') for x in all_metadatas])
    return list(distinct_keys)
def read_doc(doc, gettext=False):
    text = ""
    if not doc:
        return
    if doc.name.endswith("pdf"):
        pdf_reader = PdfReader(doc)
        for page in pdf_reader.pages:
            text += page.extract_text()
    else:
        text = docx2txt.process(doc)
    if gettext:
       return text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text=text)
    return chunks


def add_to_history(query, response, history):
    # tolog = f"""
    # :question:{query}
    #
    # :high_brightness:{response}
    # _________________
    # """
    #if not tolog in history:
    history.append((query,response))


def get_sources(answer, doc_index):
    """Retrieves the docs that were used to answer the question the generated answer."""

    source_keys = [s for s in answer.split("SOURCES: ")[-1].split(", ")]

    source_docs = []
    for doc in doc_index:
        if doc.metadata["source"] in source_keys:
            source_docs.append(doc)
    return source_docs
