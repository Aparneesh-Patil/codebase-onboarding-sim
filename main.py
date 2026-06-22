import zipfile
from fastapi import FastAPI, File, UploadFile
app = FastAPI()

fileTree = None
extensions = None
projectType = None


@app.get('/')
def read_root():
    return {"Hello": "World"}

# create the endpoint for analyzing zip files
@app.post("/analyze/")
async def create_upload_file(file: UploadFile):
    file_obj = file.file
    
    # check if file is zip or not
    if(zipfile.is_zipfile(file_obj) == False):
        return {"isZip": False, "fileTree": fileTree, "extensions": extensions, "projectType": projectType}  
    
    # resets the cursor back to the start incase reading the file has caused the cursor to move
    file_obj.seek(0)

    # gets the file tree of the zip
    get_file_tree(file_obj)
    return {"isZip": True, "fileTree": fileTree, "extensions": extensions, "projectType": projectType}


def get_file_tree(file):
    with zipfile.ZipFile(file, 'r') as archive:
        global fileTree
        fileTree = archive.namelist()
        
    