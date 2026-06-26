# Sprint 1: Find a way to analyze the Repo
The goal is to build a backend so that we accept only zipped repo, scan the folder structure and return basic codebase information.


## First Tasks
    [X] Set up FastAPI project
    [X] Create upload endpoint
    [X] Validate zip file
    [X] Extract zip safely
    [X] Ignore unnecessary folders
    [X] Generate file tree
    [X] Count file extensions
    [X] Detect project type
    [X] Identify important files
    [X] Return JSON response

## Current rule set to determine the project type:
    pom.xml
    -> Java Maven

    pom.xml + .java + application.properties
    -> Java Spring Boot

    package.json
    -> Node.js / JavaScript

    package.json + src + App.js
    -> React

    package.json + next.config.js
    -> Next.js

    requirements.txt or .py
    -> Python

    go.mod
    -> Go

    MakeFile + .c
    -> C

    MakeFile + .cpp
    -> C++

This is just a base for Sprint 1. For future, I could introduce confidence scores and judge the project types based on that.

# Sprint 2: Add Repo Chatbot

The goal is to connect the analyzer results to a basic chatbot so users can ask questions about the uploaded repo and understand where to start.

## First Tasks
    [ ] Read important code files from the repo
    [ ] Ignore files that are too large or not useful for analysis
    [ ] Create temporary repo context from file paths and contents
    [ ] Create a chat endpoint
    [ ] Pass the user question and repo context into the chatbot
    [ ] Make answers based only on the uploaded repo
    [ ] Show which files were used in the answer
    [ ] Add a simple chat box on the frontend
    [ ] Add starter onboarding questions
    [ ] Test with personal repo