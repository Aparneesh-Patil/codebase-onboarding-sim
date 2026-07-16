from astchunk import ASTChunkBuilder

# Your source code
code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
"""

# Initialize the chunk builder
configs = {
    "max_chunk_size": 100,             # Maximum non-whitespace characters per chunk
    "language": "python",              # Supported: python, java, csharp, typescript
    "metadata_template": "default"     # Metadata format for output
}
chunk_builder = ASTChunkBuilder(**configs)

# Create chunks
chunks = chunk_builder.chunkify(code)

# Each chunk contains content and metadata
for i, chunk in enumerate(chunks):
    print(f"[Chunk {i+1}]")
    print(f"{chunk['content']}")
    print(f"Metadata: {chunk['metadata']}")
    print("-" * 50)