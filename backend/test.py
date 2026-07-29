import analyzer, zip_storage, chunk, embeddings, prompt
from pathlib import Path 

fileTree = analyzer.get_file_tree("./data/codebase-onboarding-sim.zip")

important_files = analyzer.detect_important(fileTree)

zip_id = zip_storage.hash_file("./data/codebase-onboarding-sim.zip")
dir_path = Path("temp_repo/" + zip_id)
dir_path.mkdir(parents=True, exist_ok=True)

dir_path = Path("temp_repo/" + zip_id + "/embeddings")
dir_path.mkdir(parents=True, exist_ok=True)

loaded_files = analyzer.load_file("./data/codebase-onboarding-sim.zip", important_files, zip_id)

chunked_data = chunk.chunking_type(loaded_files)

chunk_list = []

for document in chunked_data:
    for doc in document:
        chunk_list.append(doc)

embeddings.store_embeddings(chunk_list, zip_id)

query = input("What questions do you have about this repo?\n")
result = embeddings.search_embeddings(query, zip_id)

context = ""
for i in range(5):
    context += str(result["documents"][0][i]) + str(result["metadatas"][0][i]) + "\n"

print(prompt.ask_ai(context, query))


"""fileTree = analyzer.get_file_tree("data/Multithreaded-Web-Server.zip")

important_files = analyzer.detect_important(fileTree)

loaded_files = analyzer.load_file("data/Multithreaded-Web-Server.zip", important_files)

chunked_data = chunk.chunking_type(loaded_files)

chunk_list = []

for document in chunked_data:
    for doc in document:
        chunk_list.append(doc)

embeddings.store_embeddings(chunk_list)


query = input("What questions do you have about this repo?\n")
result = embeddings.search_embeddings(query)

context = ""
for i in range(5):
    context += str(result["documents"][0][i]) + str(result["metadatas"][0][i]) + "\n"

print(prompt.ask_ai(context, query))

"""
