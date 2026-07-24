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