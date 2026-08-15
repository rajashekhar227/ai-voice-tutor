from app.services.pdf_service import PDFService
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from pathlib import Path
import json

pdf_service = PDFService("data/textbooks/class_8")

subjects = pdf_service.discover_pdfs()

science_pdf = subjects["hesc1dd"][0]

print("Reading:", science_pdf.name)

pages = pdf_service.extract_pages(science_pdf)

all_text = ""

for page in pages:

    text = pdf_service.reconstruct_page(page["blocks"])

    text = pdf_service.clean_text(text)

    all_text += text + "\n"


chunks = pdf_service.create_chunks(all_text)

print("Total chunks:", len(chunks))


embedding_service = EmbeddingService()

embeddings = embedding_service.create_embeddings(chunks)
vector_service = VectorService(dimension=384)
vector_service.add_embeddings(embeddings)
print("\nEmbeddings added to FAISS")
knowledge_path = Path("data/knowledge/class_8/science")

knowledge_path.mkdir(parents=True, exist_ok=True)

# Save FAISS index
vector_service.save_index(
    knowledge_path / "science.index"
)

# Save chunks
with open(knowledge_path / "chunks.json", "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)

print("\nKnowledge base saved")


print("Embeddings created")
print("Number of embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))

question = "What are Kharif crops?"

question_embedding = embedding_service.create_embeddings([question])[0]

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