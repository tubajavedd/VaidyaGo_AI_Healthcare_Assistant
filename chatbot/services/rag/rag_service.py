from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RAGService:

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Example medical knowledge
        self.docs = [
            "Fever is usually caused by infection.",
            "Drink fluids and rest for viral fever.",
            "Headache can be due to stress or dehydration."
        ]

        self.index = self.build_index()

    def build_index(self):
        embeddings = self.model.encode(self.docs)
        index = faiss.IndexFlatL2(len(embeddings[0]))
        index.add(np.array(embeddings))
        return index

    def search(self, query):
        q_emb = self.model.encode([query])
        _, I = self.index.search(np.array(q_emb), k=1)
        return self.docs[I[0][0]]
