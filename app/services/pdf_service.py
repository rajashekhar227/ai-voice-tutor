from pathlib import Path
import fitz
class PDFService:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
    def discover_pdfs(self):
        subjects = {}
        if not self.base_path.exists():
            raise FileNotFoundError(f"{self.base_path} not found")

        for subject_folder in self.base_path.iterdir():

            if subject_folder.is_dir():
                pdfs = sorted(subject_folder.glob("*.pdf"))
                subjects[subject_folder.name] = pdfs
        return subjects
    def extract_text(self, pdf_path):
        document = fitz.open(pdf_path)
        text = ""
        for page in document:
            text += page.get_text()
        document.close()
        return text