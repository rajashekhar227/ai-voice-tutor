from app.services.pdf_service import PDFService


pdf_service = PDFService("data/textbooks/class_8")

subjects = pdf_service.discover_pdfs()

science_pdf = subjects["hesc1dd"][0]

print("Reading:", science_pdf.name)

pdf_service.extract_pages(science_pdf)