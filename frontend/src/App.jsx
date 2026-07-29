import { useState } from 'react'
import FileDrop from './components/FileDrop'
import FileTree from './components/FileTree'
import './styles/workspace.css'
import ChatPanel from './components/ChatPanel'
import { getRepoFile } from './service/api'


function App() {
  const [analysis, setAnalysis] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [isFileLoading, setIsFileLoading] = useState(false)
  const [fileError, setFileError] = useState('')

  // fetches the
  async function handleFileClick(path) {
    if (!analysis || !analysis.repoId) {
      return
    }

    setIsFileLoading(true)
    setFileError('')

    // we try get the get request, if not throw an error
    try {
      const fileData = await getRepoFile(analysis.repoId, path)
      setSelectedFile(fileData)
    } catch (error) {
      console.error(error)
      setFileError(error.message)
      setSelectedFile(null)
    } finally {
      setIsFileLoading(false)
    }

  }

  // if analysis doesn't exist, we call FileDrop to get the analyzed zipped file, else we send the analyzed zipped file to FileTree (to print out the FileTree)
  return (
    <div className="parent">
      {!analysis ? (
        <FileDrop onAnalysisComplete={setAnalysis} />
      ) : (
        <div className="workspace">
          <aside className="file-panel">
            <FileTree
              files={analysis.fileTree}
              onFileClick={handleFileClick}
            />
          </aside>

          <section className="main-panel">
            {isFileLoading && (
              <div className="file-status">
                Loading file...
              </div>
            )}

            {fileError && (
              <div className="file-error">
                {fileError}
              </div>
            )}

            <div className={`chat-view ${selectedFile ? 'hidden' : ''}`}>
              <ChatPanel repoId={analysis.repoId} />
            </div>

            {selectedFile && (
              <div className="file-viewer">
                <header className="file-viewer-header">
                  <h2>{selectedFile.path}</h2>

                  <button
                    type="button"
                    onClick={() => setSelectedFile(null)}
                  >
                    Close
                  </button>
                </header>

                <pre>
                  <code>{selectedFile.content}</code>
                </pre>
              </div>
            )}
          </section>
        </div>
      )}
    </div>
  )
}

export default App
