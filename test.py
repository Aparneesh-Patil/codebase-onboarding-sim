import analyzer, chunk, embeddings, prompt

fileTree = analyzer.get_file_tree("data/Multithreaded-Web-Server.zip")

important_files = analyzer.detect_important(fileTree)

loaded_files = analyzer.load_file("data/Multithreaded-Web-Server.zip", important_files)

chunked_data = chunk.chunking_type(loaded_files)

chunk_list = []

for document in chunked_data:
    for doc in document:
        chunk_list.append(doc)

query = "What does route do?"

embeddings.store_embeddings(chunk_list)
result = embeddings.search_embeddings(query)

context = ""
for i in range(5):
    context += str(result["documents"][0][i]) + str(result["metadatas"][0][i]) + "\n"

prompt.ask_ai(context, query)


