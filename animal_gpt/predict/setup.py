import faiss
import numpy as np

class PredictionSetup:

    def __init__(self, model, sentences) -> None:
        self.model = model
        self.sentences = sentences

    # Generate embeddings for sentences and store in Faiss index
    def create_embedding_index(self):
        embeddings = self.model.encode(self.sentences)
        
        # Normalize embeddings before adding to the index
        embeddings = np.array(embeddings)
        embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)

        # Create Faiss index
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings.astype(np.float32))
        
        return index
    
    # Perform sentence similarity search using Faiss
    def find_similar_sentences(self, query, index, top_k=5):
        query_embedding = self.model.encode(query)
        query_embedding /= np.linalg.norm(query_embedding)

        # Perform similarity search using Faiss
        i, similar_indices = index.search(np.array([query_embedding]).astype(np.float32), top_k)
        # Retrieve and return similar sentences
        similar_sentences = [self.sentences[i] for i in similar_indices[0]]
        probabilities = i[0]
        return similar_sentences,probabilities