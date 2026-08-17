import json
from pathlib import Path

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


knowledge_path = Path("data/knowledge/class_8/science")

index_path = knowledge_path / "science.index"
chunks_path = knowledge_path / "chunks.json"


# Load chunks
with open(chunks_path, "r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Chunks loaded:", len(chunks))


# Load FAISS index
vector_service = VectorService(dimension=384)

vector_service.load_index(index_path)

print("FAISS index loaded")


# Create embedding service
embedding_service = EmbeddingService()


# Test search
question = "What are Kharif crops?"

question_embedding = embedding_service.create_embeddings(
    [question]
)[0]


distances, indices = vector_service.search(
    question_embedding,
    top_k=3
)


print("\nQuestion:")
print(question)

print("\nFAISS results:")
print("Distances:", distances)
print("Indices:", indices)

print("\nRelevant chunks:")

for index in indices:

    print("\nChunk", index)
    print(chunks[index])