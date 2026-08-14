from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def create_embeddings(self, chunks):

        embeddings = self.model.encode(
            chunks,
            show_progress_bar=True
        )

        return embeddings