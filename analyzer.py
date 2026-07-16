import zipfile

# used for determining the file tree
IGNORED_PATH_PARTS = {".git", "node_modules", "__pycache__", "target", "build", "dist", ".venv", ".vscode", ".idea", ".next", "cache"}

# used for determining the important files
INGORED_FILES = {".gitignore", ".gitattributes", "mvnw", "mvnw.cmd", "maven-wrapper.properties", "package-lock.json",  "yarn.lock",
"pnpm-lock.yaml", "poetry.lock", "Pipfile.lock", ".class", ".jar", ".war", ".exe", ".dll", ".so", ".o", ".obj", ".pyc", ".pyo", ".log", ".tmp", ".cache"
}

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

# counts the extensions
def count_extensions(fileTree):
    extensions = {}
    for file in fileTree:
        result = file.split("/")
        last = result[len(result) - 1]

        if "." in last:
            word = last[last.rfind("."):]
            if word not in extensions:
                extensions[word] = 1
            else:
                extensions[word] = extensions.get(word) + 1

    return extensions

# detects project type from a rule set (see notes.md)
def detect_project(fileTree):
    has_pom = False
    has_java = False
    has_app = False

    has_json = False
    has_src = False
    has_app = False
    has_config = False

    has_req = False
    has_py = False

    has_go = False

    has_make = False
    has_c = False
    has_cpp = False

    for file in fileTree:
        if file.endswith("pom.xml"):
            has_pom = True
        if file.endswith(".java"):
            has_java = True
        if file.endswith("application.properties"):
            has_app = True

        if file.endswith("package.json"):
            has_json = True
        if "src" in file:
            has_src = True
        if file.endswith("App.js"):
            has_app = True
        if file.endswith("next.config.js"):
            has_config = True

        if file.endswith("requirements.txt"):
            has_req = True
        if file.endswith(".py"):
            has_py = True
        
        if file.endswith("go.mod"):
            has_go = True
        if file.endswith("Makefile"):
            has_make = True
        if file.endswith(".c"):
            has_c = True
        if file.endswith(".cpp"):
            has_cpp = True

    if has_pom and has_java and has_app:
        return "Java Spring Boot"
    if has_pom:
        return "Java Maven"
    if has_json and has_app and has_src:
        return "React"
    if has_json and has_config:
        return "Next"
    if has_json:
        return "JavaScript"
    if has_req or has_py:
        return "Python"
    if has_go:
        return "Go"
    if has_make and has_c:
        return "C"
    if has_make and has_cpp:
        return "C++"
    
    return "Unknown"

# detects only important files and returns them
def detect_important(fileTree):
    importantFiles = []
    for file in fileTree:
        result = file.split("/")
        last = result[len(result) - 1]

        if "." in last and last not in INGORED_FILES:
            importantFiles.append(file)

    return importantFiles

# loads the content of important file into text (used for the chunker)
def load_file(file_obj, important_files):
    loaded_files = {}

    with zipfile.ZipFile(file_obj, 'r') as zf:
        for file_name in zf.namelist():
            if file_name in important_files:
                with zf.open(file_name, 'r') as r:
                    loaded_files[file_name] = r.read().decode("utf-8")

    return loaded_files