from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

LABELS = [
    "politics",
    "health",
    "economy",
    "sports",
    "technology",
    "science",
    "entertainment",
    "crime & safety",
    "general"
]


def classify(text: str) -> str:
    result = classifier(text, LABELS)
    return result["labels"][0]