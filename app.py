import logging
import os
import time

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings

from utils import get_video_id, get_video_transcript, join_transcript

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename="execution.log",
    encoding="utf-8",
    filemode="a",
)

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")


def get_text_chunks(text: str):
    text_splitter = CharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]

    return docs


def vector_embedding(url):
    """ Create vector database """
    if "vectors" not in st.session_state:
        st.session_state.embeddings = NVIDIAEmbeddings(truncate="END")

        video_id = get_video_id(url)
        transcript = get_video_transcript(video_id)

        text = join_transcript(transcript)
        logging.debug(f"FULL TRANSCRIPT:\n{text}")

        st.session_state.final_documents = get_text_chunks(text)

        st.session_state.vectors = FAISS.from_documents(
            st.session_state.final_documents,
            st.session_state.embeddings
        )


st.title("NVIDIA NIM DEMO")

prompt = ChatPromptTemplate.from_template(
    """
    Produce a summary of the input.
    {context}
    Input:{input}
    """
)


llm = ChatNVIDIA(model="meta/llama3-70b-instruct")

url = st.text_input("Enter the url of a Youtube video")

if url:
    vector_embedding(url)

    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    start_time = time.process_time()
    response = retrieval_chain.invoke({"input": url})
    logging.info(f"Response time: {time.process_time() - start_time}")
    st.write(response["answer"])

    # With a streamlit expander
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("-------------------------------")
