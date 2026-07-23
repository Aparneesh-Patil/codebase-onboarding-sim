from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from tree_sitter import Language, Parser, Node
import tree_sitter_python as tspython
import tree_sitter_cpp as tscpp
import tree_sitter_javascript as tsjs
import tree_sitter_html as tshtml
import tree_sitter_css as tscss
import tree_sitter_java as tsjava
import tree_sitter_go as tsgo
from uuid import uuid4


# Tries to figure which chunking method is the best for each "important" file
def chunking_type(file_map):
    final = []
    for key, value in file_map.items():
        if key.lower().endswith(".js"):
            source_code = value.encode('utf-8')
            result = chunk_language(source_code, "javascript", key)
            final.append(result)
        elif key.lower().endswith(".md"):
            result = chunk_markdown(value, key)
            final.append(result)
        elif key.lower().endswith(".py"):
            source_code = value.encode('utf-8')
            result = chunk_language(source_code, "python", key)
            final.append(result)
        elif key.lower().endswith(".cpp") or key.lower().endswith(".h"):
            source_code = value.encode('utf-8')
            result = chunk_language(source_code, "C++", key)
            final.append(result)
        elif key.lower().endswith(".html"):
            source_code = value.encode('utf-8')
            result = chunk_language(source_code, "html", key)
            final.append(result)
        elif key.lower().endswith(".css"):
            source_code = value.encode('utf-8')
            result = chunk_language(source_code, "css", key)
            final.append(result)
        elif key.lower().endswith(".java"):
            source_code = value.encode('utf-8')
            result = chunk_language(source_code, "java", key)
            final.append(result)
        elif key.lower().endswith(".go"):
            source_code = value.encode('utf-8')
            result = chunk_language(source_code, "go", key)
            final.append(result)
    
    return final 

# function for chunking markdown files (the method to do this is chunk based on Headers)
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

# function for chunking coding files using AST (Abstract Syntax Trees) to parse the language into functions and classes and chuncking them that way
def chunk_language(source_code: bytes, lang_type, file_path) -> list:
    if lang_type == "python":
        parser = Parser(Language(tspython.language()))
        target_types = ['function_definition', 'class_definition']
    elif lang_type == "C++":
        parser = Parser(Language(tscpp.language()))
        target_types = ['function_definition', 'class_definition', 'class_specifier']
    elif lang_type == "javascript":
        parser = Parser(Language(tsjs.language()))
        target_types = ["function_declaration", "class_declaration", "method_definition", "arrow_function"]
    elif lang_type == "html":
        parser = Parser(Language(tshtml.language()))
        target_types = ["element", "script_element", "style_element"]
    elif lang_type == "css":
        parser = Parser(Language(tscss.language()))
        target_types = ["rule_set", "media_statement", "supports_statement", "keyframes_statement"]
    elif lang_type == "java":
        parser = Parser(Language(tsjava.language()))
        target_types = ["class_declaration", "interface_declaration", "enum_declaration", "record_declaration", "method_declaration", "constructor_declaration"]
    elif lang_type == "go":
        parser = parser = Parser(Language(tsgo.language()))
        target_types = ["function_declaration", "method_declaration", "type_declaration"]

    tree = parser.parse(source_code)
    root = tree.root_node
    nodes = collect_nodes(root, target_types)
    chunks = []

    # for each node or chunk, we get it's id, content and metadata and add to our list to return
    for node in nodes:
        content = source_code[node.start_byte:node.end_byte].decode('utf-8') 
        chunk = Document(
            id=str(uuid4()),
            page_content= content,
            metadata={"start_line": node.start_point[0], "end_line": node.end_point[0], "file_path": file_path, "language": lang_type}
        )
        chunks.append(chunk)

    return chunks

# Add all nodes with the type of function and class to the list, so that their content (which is printed later) are chunked as functions and classes
def collect_nodes(node: Node, target_types: list) -> list[Node]:
    result: list[Node] = []

    if node.type in target_types:
        result.append(node)
    else:
        for child in node.children:
            result.extend(collect_nodes(child, target_types))

    return result