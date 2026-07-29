import { FaFolder, FaFile } from "react-icons/fa"
import '../styles/FileTree.css'

// converts the file paths to javascript objects
function buildTree(paths) {
  const root = {}

  paths.forEach((path) => {
    const parts = path.split("/").filter(Boolean)
    let current = root

    parts.forEach((part) => {
      // if the folder/file doesn't exist, then we create a new object for that folder
      if (!current[part]) {
        current[part] = {}
      }

      // move into the that folder/file path
      current = current[part]
    })
  })

  return root
}

// A recursive function that determine whether the current item has children (folder) or doesn't (file)
function TreeNode({ tree, currentPath = '',  onFileClick }) {
  return (
    <ul className="tree-list">
      {Object.entries(tree).map(([name, children]) => {
        // checks for whether we have a folder or file (folder = 1 or more children)
        const isFolder = Object.keys(children).length > 0

        const fullPath = currentPath ? `${currentPath}/${name}` : name

        return (
          <li key={name} className="tree-item">
            <div className={isFolder ? "folder-row" : "file-row"} onClick={() => {
              if(!isFolder){
                onFileClick(fullPath)
              }
            }}>
              
              <span className="tree-icon">
                {isFolder ? <FaFolder /> : <FaFile />}
              </span>

              <span className="tree-name">{name}</span>
            </div>

            {isFolder && (<TreeNode tree={children} currentPath={fullPath} onFileClick={onFileClick}/>)}
          </li>
        )
      })}
    </ul>
  )
}


export default function FileTree({ files, onFileClick }) {
  const tree = buildTree(files)

  return (
    <section className="file-tree">
      <h2>Repo Files</h2>
      <TreeNode tree={tree} onFileClick={onFileClick}/>
    </section>
  );

}