from sentence_transformers import SentenceTransformer
import torch 


def create_embeddings(chunks, query):
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    embeddings = embedder.encode_document(chunks) 

    query_embedding = embedder.encode_query(query)

    similarity_scores = embedder.similarity(query_embedding, embeddings)[0]
    scores, indices = torch.topk(similarity_scores, k=5)

    print("\nQuery:", query)
    print("Top 5 most similar sentences in chunks:")

    for score, idx in zip(scores, indices):
        print(f"(Score: {score:.4f})", chunks[idx])