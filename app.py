import json
import os
import sys
import boto3
import streamlit as st

from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS

from QASystem.ingestion import data_ingestion, get_vector_store
from QASystem.retreivalandgeneration import get_llama2_llm, get_llm_response

bedrock = boto3.client(service_name='bedrock-runtime')
bedrock_embeddings = BedrockEmbeddings(model_id='amazon.titan-embed-text-v1', client=bedrock)


def main():
    st.set_page_config('QA with Document')
    st.header('QA with Document using Langchain and AWS Bedrock')

    user_question = st.text_input('Ask Question from PDF File.')

    with st.sidebar:
        st.title('Update or create vector store')
        if st.button('vector update'):
            with st.spinner('processing...'):
                docs = data_ingestion()
                get_vector_store(docs)
        
        if st.button('llama model'):
            with st.spinner('processing...'):
                faiss_index=FAISS.load_local("faiss_index",bedrock_embeddings,allow_dangerous_deserialization=True)
                llm = get_llama2_llm()

                st.write(get_llm_response(llm, faiss_index, user_question))
                st.success('Done')

if __name__=="__main__":
    main()
