import analyzer, chunk, embeddings

fileTree = analyzer.get_file_tree("data/Multithreaded-Web-Server.zip")

important_files = analyzer.detect_important(fileTree)

loaded_files = analyzer.load_file("data/Multithreaded-Web-Server.zip", important_files)

chunked_data = chunk.chunking_type(loaded_files)

chunk_list = []

for document in chunked_data:
    for doc in document:
        chunk_list.append(doc.page_content)

query = "What does Router do?"

embeddings.create_embeddings(chunk_list, query)

