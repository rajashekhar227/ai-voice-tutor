import faiss
import numpy as np


class VectorService:

    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings):

        vectors = np.array(embeddings).astype("float32")

        self.index.add(vectors)

    def search(self, query_embedding, top_k=3):

        query_vector = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(
            query_vector,
            top_k
        )

        return distances[0], indices[0]

    def save_index(self, path):
        faiss.write_index(self.index, str(path))
    def load_index(self, path):
        self.index = faiss.read_index(str(path))