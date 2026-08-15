from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


# Test chunks
chunks = [
    "Kharif crops are sown in the rainy season.",
    "Rabi crops are grown in the winter season.",
    "The preparation of soil is the first step before growing a crop.",
    "Irrigation is the supply of water to crops at regular intervals."
]


# Create embeddings
embedding_service = EmbeddingService()
embeddings = embedding_service.create_embeddings(chunks)

print("Embeddings created")
print("Number of embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))


# Create FAISS index
vector_service = VectorService(dimension=384)

# Add embeddings to FAISS
vector_service.add_embeddings(embeddings)

print("\nEmbeddings added to FAISS")


# Question
question = "What crops are grown during the rainy season?"


# Convert question into embedding
question_embedding = embedding_service.create_embeddings([question])[0]


# Search FAISS
distances, indices = vector_service.search(
    question_embedding,
    top_k=2
)


print("\nQuestion:")
print(question)

print("\nFAISS results:")
print("Distances:", distances)
print("Indices:", indices)


# Show the actual chunks
print("\nRelevant chunks:")

for index in indices:
    print("\nChunk", index)
    print(chunks[index])