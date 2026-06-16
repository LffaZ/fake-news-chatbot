from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
import os
import boto3

s3 = boto3.client("s3")

bucket = "fake-news-uas"
prefix = "faiss_index"
llm = Ollama(model="llama3.2:3b")
embedding = OllamaEmbeddings(model="llama3")

local_dir = "/home/ubuntu/fake-news-chatbot/faiss_index"
os.makedirs(local_dir, exist_ok=True)
s3.download_file(
    bucket,
    f"{prefix}/index.faiss",
    f"{local_dir}/index.faiss"
)

s3.download_file(
    bucket,
    f"{prefix}/index.pkl",
    f"{local_dir}/index.pkl"
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embedding,
    allow_dangerous_deserialization=True
)


def generate_answer(question, docs):
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a hoax news detection assistant.

Context:
{context}

Question:
{question}

Answer:
"""

    return llm.invoke(prompt)