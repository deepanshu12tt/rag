from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = self.model.get_sentence_embedding_dimension()

    def embed(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)
