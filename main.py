import chunk, analyzer, zipfile
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

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

    return {"isZip": True, "fileTree": fileTree, "extensions": extensions, "projectType": projectType, "importantFiles": important_files, "loaded_files": loaded_files, "chunked_data": chunked_data}





                    
        
    