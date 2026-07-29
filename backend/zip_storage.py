import hashlib, zipfile
from pathlib import Path

# hashing contents of our file - inspired by https://www.youtube.com/watch?v=cMdgDTgxx6o
def hash_file(file_obj, algorithm: str='sha256', chunk_size: int = 8192) -> str:
    hasher = hashlib.new(algorithm)

    with zipfile.ZipFile(file_obj, 'r') as zf:
        for file_name in zf.namelist():
            if file_name.endswith('/'):
                continue

            with zf.open(file_name, 'r') as f:
                # reads the chunks of the file (with our defined chunk size) until it finds an empty bytes object
                for chunk in iter(lambda: f.read(chunk_size), b''):
                    hasher.update(chunk)

    hash_output = hasher.hexdigest()

    return hash_output


