import hashlib
from pathlib import Path


def calculate_file_hash(filepath: Path, hash_type="sha1"):

    with open(filepath, "rb") as data:
        sha1_hash = hashlib.sha1(data.read()).hexdigest()

    return sha1_hash