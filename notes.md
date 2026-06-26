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