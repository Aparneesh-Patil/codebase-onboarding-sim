import chunk, analyzer, zipfile, embeddings, prompt, zip_storage
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI()

# Since FastAPI is hosted on a different domain than the frontend is hosted, we enable this to prevent CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# defines the POST's request body for the chatbot endpoint 
class ChatRequest(BaseModel):
    query: str
    repo_id: str

@app.get('/')
def read_root():
    return {"Hello": "World"}

# create the endpoint for analyzing zip files
@app.post("/analyze/")
def create_upload_file(file: UploadFile):
    file_obj = file.file

    # check if file is zip or not
    if(zipfile.is_zipfile(file_obj) == False):
        return {"isZip": False, "fileTree": None, "extensions": None, "projectType": None, "importantFiles": None}  
    
    # resets the cursor back to the start incase reading the file has caused the cursor to move
    file_obj.seek(0)

    repo_id = zip_storage.hash_file(file_obj)

    # creates a storage for vector_embeddings and file_storage
    dir_path = Path("temp_repo/" + repo_id)
    dir_path.mkdir(parents=True, exist_ok=True)

    fileTree = analyzer.get_file_tree(file_obj)

    extensions = analyzer.count_extensions(fileTree)

    projectType = analyzer.detect_project(fileTree)

    important_files = analyzer.detect_important(fileTree)

    loaded_files = analyzer.load_file(file_obj, important_files, repo_id)

    chunked_data = chunk.chunking_type(loaded_files)

    chunk_list = []

    for document in chunked_data:
        for doc in document:
            chunk_list.append(doc)

    embeddings.store_embeddings(chunk_list, repo_id)

    return {"repoId": repo_id, "isZip": True, "fileTree": fileTree, "extensions": extensions, "projectType": projectType, "importantFiles": important_files}

@app.post("/chatbot")
def reply_with_chatbot(chat : ChatRequest):

    result = embeddings.search_embeddings(chat.query, chat.repo_id)

    context = ""
    for i in range(5):
        context += str(result["documents"][0][i]) + str(result["metadatas"][0][i]) + "\n"

    response = prompt.ask_ai(context, chat.query)

    return {"response": response}

# GET request for getting each specfic file
@app.get("/repos/{repo_id}/files")
def get_files(repo_id: str, path: str):
    repo_directory = Path("temp_repo/" + repo_id).resolve()
    requested_file = Path("temp_repo/" + repo_id + "/" + path).resolve()

    if repo_directory not in requested_file.parents:
        raise HTTPException(status_code=400, detail="Invalid file path")

    if not requested_file.exists() or not requested_file.is_file():
        raise HTTPException(status_code=404, detail="File not found") 


    content = requested_file.read_text(
        encoding="utf-8",
        errors="replace"
    )

    return {"path": path, "content": content}
    





                    
        
    