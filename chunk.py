from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from tree_sitter import Language, Parser, Node
import tree_sitter_python as tspython
from uuid import uuid4


# Tries to figure which chunking method is the best for each "important" file
def chunking_type(file_map):
    final = []
    for key, value in file_map.items():
        if ".md" in key:
            result = chunk_markdown(value, key)
            final.append(result)
        elif ".py" in key:
            source_code = value.encode('utf-8')
            result = chunk_language(source_code, "python", key)
            final.append(result)
    
    return final 


def chunk_markdown(markdown_text, file_path) -> list[Document]:
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]   
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    documents = splitter.split_text(markdown_text)

    for doc in documents:
        doc.metadata["file_path"] = file_path
        doc.metadata["language"] = "markdown"

    return documents


def chunk_language(source_code: bytes, lang_type, file_path) -> list:
    if lang_type == "python":
        parser = Parser(Language(tspython.language()))
        tree = parser.parse(source_code)
        root = tree.root_node
        
        nodes = collect_nodes(root)
        chunks = []

        for node in nodes:
            string = source_code[node.start_byte:node.end_byte].decode('utf-8') 
            chunk = Document(
                id=str(uuid4()),
                page_content= string,
                metadata={"start_line": node.start_point[0], "end_line": node.end_point[0], "file_path": file_path, "language": lang_type}
            )
            chunks.append(chunk)

        return chunks
    
def collect_nodes(node: Node) -> list[Node]:
    target_types = ['function_definition', 'class_definition']
    result: list[Node] = []

    if node.type in target_types:
        result.append(node)
    else:
        for child in node.children:
            result.extend(collect_nodes(child))

    return result
    




