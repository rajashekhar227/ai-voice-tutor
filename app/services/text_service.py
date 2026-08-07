import re


class TextService:

    def clean_text(self, text: str) -> str:

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove year markers
        text = re.sub(r"\b20\d{2}-\d{2}\b", "", text)

        # Remove common page headers
        text = re.sub(r"\nSCIENCE\n", "\n", text)

        # Remove standalone page numbers
        text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

        # Join words broken across lines
        # Example:
        # agri-
        # culture
        # ->
        # agriculture
        text = re.sub(r"-\n(\w)", r"-\1", text)

        # Replace newlines inside sentences with spaces
        text = re.sub(r"(?<![.!?:])\n(?!\n)", " ", text)

        # Normalize multiple spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize multiple blank lines
        text = re.sub(r"\n\s*\n+", "\n\n", text)

        return text.strip()