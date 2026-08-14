from app.services.pdf_service import PDFService
from app.services.embedding_service import EmbeddingService


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

print("Embeddings created")
print("Number of embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))
print("\nFIRST CHUNK")
print("=" * 60)
print(chunks[0])
print()
print()
print()
print("\nFIRST CHUNK EMBEDDING")
print("=" * 60)
print(embeddings[0])

print("\nEMBEDDING LENGTH:")
print(len(embeddings[0]))