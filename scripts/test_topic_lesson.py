import json
from pathlib import Path

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.llm_service import LLMService


# --------------------------------
# Settings
# --------------------------------

SUBJECT = "hesc1dd"
TOPIC = "Kharif Crops"
TOP_K = 3

knowledge_path = Path("data/knowledge/class_8") / SUBJECT


# --------------------------------
# Load chunks
# --------------------------------

with open(
    knowledge_path / "chunks.json",
    "r",
    encoding="utf-8"
) as file:

    chunks = json.load(file)


# --------------------------------
# Load FAISS
# --------------------------------

embedding_service = EmbeddingService()

vector_service = VectorService(dimension=384)

vector_service.load_index(
    knowledge_path / f"{SUBJECT}.index"
)


# --------------------------------
# Search textbook
# --------------------------------

print("\nSearching textbook...")
print("=" * 60)

query_embedding = embedding_service.create_embeddings(
    [TOPIC]
)[0]

distances, indices = vector_service.search(
    query_embedding,
    top_k=TOP_K
)


print("\nFAISS results:")

for distance, index in zip(distances, indices):

    print(
        f"Index: {index} | Distance: {distance:.4f}"
    )


# --------------------------------
# Get relevant chunks
# --------------------------------

relevant_chunks = []

for index in indices:

    if index == -1:
        continue

    relevant_chunks.append(chunks[index])


print("\nRelevant textbook content:")
print("=" * 60)

for i, chunk in enumerate(relevant_chunks):

    print(f"\nChunk {i + 1}")
    print("-" * 40)
    print(chunk[:500])


# --------------------------------
# Generate teacher lesson
# --------------------------------

content = "\n\n".join(relevant_chunks)

llm_service = LLMService()

lesson = llm_service.generate_lesson(
    topic=TOPIC,
    content=content
)


# --------------------------------
# Final lesson
# --------------------------------

print("\n\nGENERATED LESSON")
print("=" * 60)

print(lesson)