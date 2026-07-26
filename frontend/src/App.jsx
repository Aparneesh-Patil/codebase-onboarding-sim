import { useState } from 'react'
import FileDrop from './components/FileDrop'
import FileTree from './components/FileTree'
import './styles/workspace.css'
import ChatPanel from './components/ChatPanel'


function App() {
  const [analysis, setAnalysis] = useState(null)

  // if analysis doesn't exist, we call FileDrop to get the analyzed zipped file, else we send the analyzed zipped file to FileTree (to print out the FileTree)
  return (
    <div className="parent">

      {!analysis ? (
        <FileDrop onAnalysisComplete={setAnalysis} />
      ) : (
        <div className="workspace">
          <aside className="file-panel">
            <FileTree files={analysis.fileTree} />
          </aside>

          <ChatPanel/>
        </div>
      )}
    </div>
  );
    
}

export default App
