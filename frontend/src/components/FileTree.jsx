export default function FileTree({ files }) {
  return (
    <div className="file-tree">
      <h2>Repository Files</h2>

      <ul>
        {files.map((filePath) => (
          <li key={filePath}>{filePath}</li>
        ))}
      </ul>
    </div>
  );
}