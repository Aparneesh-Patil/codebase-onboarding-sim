import zipfile
from fastapi import FastAPI, File, UploadFile
app = FastAPI()


IGNORED_PATH_PARTS = {".git", "node_modules", "__pycache__", "target", "build", "dist", ".venv", ".vscode", ".idea", ".next", "cache"}

@app.get('/')
def read_root():
    return {"Hello": "World"}

# create the endpoint for analyzing zip files
@app.post("/analyze/")
async def create_upload_file(file: UploadFile):
    file_obj = file.file
    
    # check if file is zip or not
    if(zipfile.is_zipfile(file_obj) == False):
        return {"isZip": False, "fileTree": None, "extensions": None, "projectType": None}  
    
    # resets the cursor back to the start incase reading the file has caused the cursor to move
    file_obj.seek(0)

    # gets the file tree of the zip, ignoring files if needed
    fileTree = get_file_tree(file_obj)

    extensions = count_extensions(fileTree)
    return {"isZip": True, "fileTree": fileTree, "extensions": None, "projectType": None}


# gets the file tree from the zip file, ignoring folders/files in the ignored path
def get_file_tree(file):
    with zipfile.ZipFile(file, 'r') as archive:
        skip = False
        fileTree = []
        for file_name in archive.namelist():
            result = file_name.split("/")
            for word in result:
                if word in IGNORED_PATH_PARTS:
                    skip = True
                    break
            if skip == False:
                fileTree.append(file_name)
            skip = False
    return fileTree

def count_extensions(fileTree):
    extensions = {}
    
            


                    
        
    