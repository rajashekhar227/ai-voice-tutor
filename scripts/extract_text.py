from app.services.pdf_service import PDFService


pdf_service = PDFService("data/textbooks/class_8")

subjects = pdf_service.discover_pdfs()

science_pdf = subjects["hesc1dd"][0]

print("Reading:", science_pdf.name)

pages = pdf_service.extract_pages(science_pdf)

print("Total pages extracted:", len(pages))

for page in pages[:3]:

    print(f"\n\nPAGE {page['page']}")
    print("=" * 60)

    text = pdf_service.reconstruct_page(page["blocks"])

    cleaned_text = pdf_service.clean_text(text)

    print(cleaned_text)