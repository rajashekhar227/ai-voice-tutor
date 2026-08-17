from pathlib import Path
import json

from app.services.pdf_service import PDFService
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


# -----------------------------
# Paths
# -----------------------------

TEXTBOOK_PATH = "data/textbooks/class_8"
KNOWLEDGE_PATH = Path("data/knowledge/class_8")


# -----------------------------
# Services
# -----------------------------

pdf_service = PDFService(TEXTBOOK_PATH)
embedding_service = EmbeddingService()


# Discover all subjects
subjects = pdf_service.discover_pdfs()

print("\nSubjects found:")

for subject, pdfs in subjects.items():
    print(f"{subject}: {len(pdfs)} PDFs")


# -----------------------------
# Process every subject
# -----------------------------

for subject, pdfs in subjects.items():

    print("\n" + "=" * 60)
    print("SUBJECT:", subject)
    print("=" * 60)
    if not pdfs:
        print("No PDFs found. Skipping subject.")
        continue
    subject_path = KNOWLEDGE_PATH / subject
    subject_path.mkdir(parents=True, exist_ok=True)

    all_chunks = []
    metadata = []

    # Process every PDF
    for pdf_path in pdfs:

        print("\nProcessing:", pdf_path.name)

        pages = pdf_service.extract_pages(pdf_path)

        all_text_parts = []

        for page in pages:

            text = pdf_service.reconstruct_page(page["blocks"])
            text = pdf_service.clean_text(text)

            all_text_parts.append(text)

        all_text = "\n\n".join(all_text_parts)

        chunks = pdf_service.create_chunks(all_text)

        print("Chunks:", len(chunks))

        # Store chunks
        for chunk_id, chunk in enumerate(chunks):

            all_chunks.append(chunk)

            metadata.append({
                "subject": subject,
                "pdf": pdf_path.name,
                "chunk_id": chunk_id
            })

    # -----------------------------
    # Create embeddings
    # -----------------------------

    print("\nCreating embeddings...")

    embeddings = embedding_service.create_embeddings(all_chunks)

    print("Total chunks:", len(all_chunks))
    print("Embedding size:", len(embeddings[0]))

    # -----------------------------
    # Create FAISS index
    # -----------------------------

    vector_service = VectorService(dimension=384)

    vector_service.add_embeddings(embeddings)

    # -----------------------------
    # Save FAISS index
    # -----------------------------

    index_path = subject_path / f"{subject}.index"

    vector_service.save_index(index_path)

    # -----------------------------
    # Save chunks
    # -----------------------------

    chunks_path = subject_path / "chunks.json"

    with open(chunks_path, "w", encoding="utf-8") as file:
        json.dump(
            all_chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    # -----------------------------
    # Save metadata
    # -----------------------------

    metadata_path = subject_path / "metadata.json"

    with open(metadata_path, "w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\nSaved:")
    print(index_path)
    print(chunks_path)
    print(metadata_path)


print("\n" + "=" * 60)
print("KNOWLEDGE BASE BUILD COMPLETE")
print("=" * 60)