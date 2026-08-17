from app.services.pdf_service import PDFService
pdf_service = PDFService("data/textbooks/class_8")
subjects = pdf_service.discover_pdfs()
science_pdf = subjects["hesc1dd"][0]
print("Reading:", science_pdf.name)
pages = pdf_service.extract_pages(science_pdf)
print("Total pages extracted:", len(pages))
all_text = ""
all_text_parts = []

for page in pages:

    text = pdf_service.reconstruct_page(page["blocks"])

    text = pdf_service.clean_text(text)

    all_text_parts.append(text)


all_text = "\n\n".join(all_text_parts)
chunks = pdf_service.create_chunks(all_text)
print("Total chunks:", len(chunks))
for i, chunk in enumerate(chunks[:3]):
    print(f"\n\nCHUNK {i + 1}")
    print("=" * 60)
    print(chunk)