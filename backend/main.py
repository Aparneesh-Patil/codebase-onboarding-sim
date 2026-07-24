import chunk, analyzer, zipfile, embeddings, prompt
from fastapi import FastAPI, UploadFile 
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Since FastAPI is hosted on a different domain than the frontend is hosted (prevents CORS errors)
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

    fileTree = analyzer.get_file_tree(file_obj)

    extensions = analyzer.count_extensions(fileTree)

    projectType = analyzer.detect_project(fileTree)

    important_files = analyzer.detect_important(fileTree)

    loaded_files = analyzer.load_file(file_obj, important_files)

    chunked_data = chunk.chunking_type(loaded_files)

    chunk_list = []

    for document in chunked_data:
        for doc in document:
            chunk_list.append(doc)

    embeddings.store_embeddings(chunk_list)

    return {"isZip": True, "fileTree": fileTree, "extensions": extensions, "projectType": projectType, "importantFiles": important_files}

@app.post("/chatbot")
def reply_with_chatbot(chat : ChatRequest):

    result = embeddings.search_embeddings(chat.query)

    context = ""
    for i in range(5):
        context += str(result["documents"][0][i]) + str(result["metadatas"][0][i]) + "\n"

    response = prompt.ask_ai(context, chat.query)

    return {"response": response}





                    
        
    