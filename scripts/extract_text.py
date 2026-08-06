from app.services.pdf_service import PDFService
service = PDFService("data/textbooks/class_8")
subjects = service.discover_pdfs()
science_pdf = subjects["hesc1dd"][0]
print("Reading:", science_pdf.name)
print("-" * 50)
text = service.extract_text(science_pdf)
print(len(text))
print(text[:2000])   