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

    def extract_pages(self, pdf_path):
        document = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(document, start=1):

            blocks = page.get_text("blocks")

            page_blocks = []

            for block in blocks:

                x0, y0, x1, y1, text, block_no, block_type = block

                text = text.strip()

                if not text:
                    continue

                page_blocks.append({
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "text": text,
                    "block_no": block_no,
                    "block_type": block_type
                })

            pages.append({
                "page": page_number,
                "blocks": page_blocks
            })

        document.close()

        return pages