from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        print(f"\n📦 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("✓ Embedding model ready")

    def encode(self, texts):
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )
