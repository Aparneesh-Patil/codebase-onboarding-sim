# Codebase Onboarding Simulator

A local web application that helps developers understand unfamiliar codebases. Users upload a zipped repository, explore its file structure, open source files, and ask questions about the project through a repository-aware chatbot. This is a demo of how this project works: [youtube_link]

## Overview

Understanding a new codebase can take a significant amount of time. Developers, like me, often need to manually inspect folders, locate important files, identify the technologies being used, and determine where the main application logic begins. The Codebase Onboarding Simulator simplifies this process by analyzing an uploaded repository and presenting useful onboarding information in one workspace.

The application can:

* Display the repository's file tree
* Display source code when files are selected
* Split source files into code chunks
* Generate embeddings for repository content
* Retrieve relevant code for a user's question
* Answer questions using only the uploaded repository
* Show which files were used to generate an answer

Note that this project is currently designed to only run locally.

## What I Learned

This project taught me how different parts of a full-stack application work together, from uploading and analyzing repositories to displaying files in a React interface. I also gained hands-on experience with source-code parsing, embeddings, vector databases, and retrieval-augmented generation. One of the biggest things I learned was how important it is to give an AI model only the most relevant code instead of the entire repository. I also became more comfortable debugging issues across both the frontend and backend. Overall, this project helped me better understand how AI tools can be built to solve practical developer problems.


## Features

### Repository Upload

Users can upload a repository as a `.zip` file.

The backend validates the upload before analyzing its contents.

### Repository Analysis

The analyzer scans the uploaded project and returns:

* File tree
* File-extension counts
* Detected project type
* Important files
* Parsed and chunked source code

Folders that usually contain unnecessary files are ignored, for example:

```text
.git
node_modules
__pycache__
target
build
dist
.venv
.vscode
.idea
.next
cache
```

### Interactive File Tree

The frontend displays the repository as an expandable file tree.

Users can select a file to retrieve and display its contents without leaving the main workspace.

### Code Chunking

Source files are divided into smaller chunks so that relevant sections can be retrieved more accurately.

The project uses tree-sitter to detect structures such as:

* Functions
* Classes
* Methods
* Other language-specific declarations

### Repository-Aware Chatbot

Users can ask personalized questions about the repository to a chatbot. The chatbot retrieves the most relevant code chunks and uses them as context when generating its answer.

## Tech Stack

### Frontend

* React
* JavaScript
* CSS
* Vite

### Backend

* Python
* FastAPI

### Code Analysis

* Tree-sitter
* Language-specific Tree-sitter parsers

### Retrieval and Embeddings

* Sentence Transformers
* `all-MiniLM-L6-v2` from Hugging Face
* ChromaDB
* Langchain
* `qwen2.5-coder:7b` from ollama

## How It Works

### 1. Upload

The user uploads a zipped repository through the React frontend.

### 2. Analyze

The FastAPI backend:

1. Validates that the uploaded file is a ZIP archive
2. Extracts the repository into a temporary directory
3. Ignores unnecessary folders and generated files
4. Creates the file tree
5. Counts file extensions
6. Detects the project type
7. Identifies important files
8. Loads supported source files

### 3. Chunk

Supported files are parsed and divided into smaller logical sections, such as functions and classes.

### 4. Embed

Each chunk is converted into a vector embedding and stored in ChromaDB.

### 5. Retrieve

When the user submits a question, the question is embedded and compared with the stored repository chunks. The most relevant chunks are selected.

### 6. Generate an Answer

The retrieved code and file metadata are passed to the chatbot, which generates a repository-specific response.

## API Endpoints

### Analyze a Repository

```http
POST /analyze/
```

Uploads and analyzes a zipped repository.


### Retrieve a Repository File

```http
GET /repos/{repo_id}/files?path={file_path}
```

Returns the contents of a selected repository file.


### Ask the Chatbot

```http
POST /chatbot
```


## Running the Project Locally

## Prerequisites

Install the following before starting:

* Python 3.12 or newer
* Node.js
* npm
* Ollama
* qwen2.5-coder:7b model from ollama


## Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### macOS or Linux

```bash
source .venv/bin/activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The backend should run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local URL shown by Vite, usually:

```text
http://localhost:5173
```

## Supported Languages

Current languages that can be chunked are:

* Markdown
* Python
* JavaScript
* Java
* C
* C++
* Go
* HTML
* CSS

## Future Improvements

* Improve language-specific code chunking
* Improve repository cleanup and temporary-file handling
* Improve source references in chatbot responses
* Add response streaming or typing animation
* Add a return button to go back to upload site

## Project Goals

This project is intended to demonstrate experience with:

* Full-stack application development
* REST API design
* React state management
* Repository and filesystem analysis
* Secure file handling
* Source-code parsing
* Retrieval-augmented generation
* Embeddings and vector databases
* AI-assisted developer tools
* Codebase onboarding and documentation

## Limitations

* The project currently runs locally
* Large repositories may take longer to analyze
* Some programming languages may not yet have specialized chunking
* Retrieval quality depends on chunk size and embedding quality
* The chatbot may not always retrieve every file needed for a complete answer
* Uploaded code is analyzed but should never be executed
* Repository sessions may not persist after the backend stops
