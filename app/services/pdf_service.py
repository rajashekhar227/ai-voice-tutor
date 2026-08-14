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
    def reconstruct_page(self, blocks):

        filtered_blocks = []

        for block in blocks:

            text = block["text"].strip()

            if text == "2024-25":
                continue

            filtered_blocks.append(block)

        # Separate left and right columns
        left_blocks = []
        right_blocks = []

        for block in filtered_blocks:

            if block["x0"] < 310:
                left_blocks.append(block)
            else:
                right_blocks.append(block)

        # Sort each column from top to bottom
        left_blocks.sort(key=lambda block: block["y0"])
        right_blocks.sort(key=lambda block: block["y0"])

        # Combine columns
        ordered_blocks = left_blocks + right_blocks

        text_parts = []

        for block in ordered_blocks:
            text_parts.append(block["text"])

        return "\n\n".join(text_parts)
    def clean_text(self, text):
        text = " ".join(text.split())
        title = "CROP PRODUCTION AND MANAGEMENT"
        if text.startswith(title + " " + title):
            text = text.replace(title + " " + title,title,1)
        text = text.replace("P aheli", "Paheli")
        return text.strip()
    def create_chunks(self, text, chunk_size=700, overlap=100):
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks