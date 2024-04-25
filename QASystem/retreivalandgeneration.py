from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
from QASystem.ingestion import get_vector_store
from langchain_community.embeddings import BedrockEmbeddings
import boto3

bedrock = boto3.client(service_name='bedrock-runtime')
bedrock_embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",client=bedrock)


prompt_template = """

Human: Use the following pieces of context to provide a 
concise answer to the question at the end but usse atleast summarize with 
250 words with detailed explaantions. If you don't know the answer, 
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context

Question: {question}

Assistant:"""

PROMPT=PromptTemplate(
    template=prompt_template,
    input_variables=["context","question"]
)

def get_llama2_llm():
    llm=Bedrock(model_id='meta.llama2-70b-chat-v1', client=bedrock)
    return llm


def get_llm_response(llm, vectorstore_faiss, query):
    qa = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = 'stuff',
        retriever = vectorstore_faiss.as_retriever(
            search_type = 'similarity',
            search_kwargs = {"k":3}
        ),
        return_source_documents = True,
        chain_type_kwargs = {"prompt": PROMPT}
    )

    answer = qa({"query": query})

    return answer['result']


if __name__ == '__main__':
    llm = get_llama2_llm()
    query = 'What is RAG token?'
    faiss_index=FAISS.load_local("faiss_index",bedrock_embeddings,allow_dangerous_deserialization=True)
    query="What is RAG token?"

    print(get_llm_response(llm, faiss_index, query))