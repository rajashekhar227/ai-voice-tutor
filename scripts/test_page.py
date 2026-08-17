from app.services.pdf_service import PDFService


pdf_service = PDFService("data/textbooks/class_8")

subjects = pdf_service.discover_pdfs()

science_pdf = subjects["hesc1dd"][0]

pages = pdf_service.extract_pages(science_pdf)

for page in pages[:3]:

    print("\n")
    print("=" * 80)
    print("PAGE:", page["page"])
    print("=" * 80)

    text = pdf_service.reconstruct_page(page["blocks"])

    print(text)