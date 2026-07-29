// uses a fetch to get the response given that the Request body is the zipped file
export async function analyzeRepo(file){
    const formData = new FormData()

    formData.append("file", file)

    // POST request with the Request body being the zipped file
    const response = await fetch("http://127.0.0.1:8000/analyze/", {
        method: "POST",
        body: formData,
    })

    
    if (!response.ok) {
        throw new Error("Repository analysis failed")
    }

    // return response
    return response.json()
}

export async function sendChatMessage(query, repoId){
    const response = await fetch("http://127.0.0.1:8000/chatbot", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            query: query,
            repo_id: repoId
        })
    })

    if (!response.ok) {
        throw new Error("Chatbot request failed")
    }

    // return response
    return response.json()
}

export async function getRepoFile(repoId, path){
    // converts the path string to query strings
    const query = new URLSearchParams({path: path})

    const response = await fetch(`http://127.0.0.1:8000/repos/${repoId}/files?path=${encodeURIComponent(path)}`, {
        method: "GET"
    })

    if (!response.ok) {
        throw new Error("Failed to retrieve files")
    }

    return response.json()

}