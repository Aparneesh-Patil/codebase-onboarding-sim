import '../styles/FileDrop.css'
import {useRef, useState} from "react"

export default function FileDrop(){

    const uploadRef = useRef(null)
    const [file, setFile] = useState(null)

    // sets current file to the uploaded file (intilized as null)
    const handleChange = (e) =>{
        setFile(uploadRef.current.files[0])
    }

    // called when user hits the Analyze Repo button
    const handleAnalyze = (e) => {
        // separates the button click to the div click
        e.stopPropagation()

        if (!file) return

        console.log("Analyze repository")
    }

    const handleUploadBoxClick = () => {
        if (uploadRef.current !== null) {
            uploadRef.current.click()
        }
    }

    return(
        <div className="upload-page">
            <div className="upload-card">
                <div className="upload-header">
                    <span className="upload-label">Repository Upload</span>

                    <h1>Upload your codebase</h1>

                    <p>
                        Upload a ZIP file to analyze the project structure and explore the
                        repository.
                    </p>
                </div>

                <div className="upload-box" onClick={handleUploadBoxClick}>
                    {/* The screen changes depending on whether a file has been uploaded or not */}
                    {file ? (
                        // File exists
                        <>
                            <div className="upload-icon uploaded">
                                <svg
                                    viewBox="0 0 24 24"
                                    width="42"
                                    height="42"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    >
                                    <path d="M20 6 9 17l-5-5" />
                                </svg>
                            </div>

                            <div className="upload-text">
                                <h2>{file.name}</h2>
                                <p>{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                            </div>

                            <div className="upload-info">
                                <button className= "analyze-button" onClick={handleAnalyze} type="button">Analyze Repo</button>
                            </div>
                        </>
                    ) : (
                        // file doesn't exist
                        <>
                            <div className="upload-icon">
                                <svg
                                    viewBox="0 0 24 24"
                                    width="42"
                                    height="42"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="1.8"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    >
                                    <path d="M12 16V4" />
                                    <path d="m7 9 5-5 5 5" />
                                    <path d="M20 15v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-4" />
                                </svg>
                            </div>

                            <div className="upload-text">
                                <h2>Select your repository</h2>
                                <p>Choose a ZIP file from your computer</p>
                            </div>

                            <div className="upload-info">
                                <span>ZIP files only</span>
                                <span>Maximum 50 MB</span>
                            </div>
                        </>
                    )}

                    <input ref={uploadRef} className="file-input" type="file" accept=".zip" onChange={handleChange} onClick={(e) => e.stopPropagation()}/>
                </div>

                <p className="privacy-text">
                Your repository will only be used for analysis.
                </p>
            </div>
        </div>
        
    );
}