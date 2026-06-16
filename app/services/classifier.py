from langchain_community.llms import Ollama

llm = Ollama(model="llama3.2:3b")

LABELS = [
    "politics","health","economy","sports",
    "technology","science","entertainment",
    "crime & safety","general"
]

def classify(text: str) -> str:
    prompt = f"""
Classify text into ONE category:

{", ".join(LABELS)}

Text:
{text}

Return only category name.
"""
    return llm.invoke(prompt).strip().lower()