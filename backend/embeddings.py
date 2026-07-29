from sentence_transformers import SentenceTransformer
import chromadb

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# stores vector database here
client = chromadb.PersistentClient(path="data/chroma")

collection = client.get_or_create_collection(name="zipfile_embeddings")

def store_embeddings(chunks, repo_id):
    # checks for whether the repo_id exists and returns if it does
    existing = collection.get(where={"repo_id": repo_id},limit=1)

    if len(existing["ids"]) > 0:
        return
  
    # The chunks page content is converted into embeddings
    document = []

    for chunk in chunks:
        document.append(chunk.page_content + chunk.metadata["file_path"])
    
    embedding = embedder.encode_document(document, convert_to_numpy=True, normalize_embeddings=True)

    collection.add(
        embeddings=embedding.tolist(),
        ids=[f"{repo_id}:{i}" for i in range(len(chunks))],
        documents= [chunk.page_content for chunk in chunks],
        metadatas = [{"source": chunk.metadata["file_path"], "repo_id": repo_id} for chunk in chunks]
    )

def search_embeddings(query, repo_id):
    query_embedding = embedder.encode_query(query, convert_to_numpy=True, normalize_embeddings=True)

    result = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results= 5,
        where={"repo_id": repo_id}
    )

    return result
