import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

RETRIEVE_K = 15   # retrieve more
FINAL_K = 5       # return fewer

class VectorIndex:
    def __init__(self):
        self.chunks = []
        self.embeddings = None

    def build(self, chunks, embedder):
        self.chunks = chunks
        texts = [c["text"] for c in chunks]
        self.embeddings = embedder.encode(texts)
        print(f"✓ Vector index built with {len(chunks)} chunks")

    