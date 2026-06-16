from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

llm = Ollama(model="llama3.2:3b")

embedding = OllamaEmbeddings(model="llama3")

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