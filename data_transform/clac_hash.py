import hashlib
from tqdm.auto import tqdm
from pathlib import Path


def calculate_file_hash(filepath: Path, hash_type="sha1"):
    file_size = filepath.stat().st_size
    hash_obj = hashlib.new(hash_type)

    with open(filepath, "rb") as f, tqdm(
        total=file_size, unit="B", unit_scale=True
    ) as pbar:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
            pbar.update(len(chunk))

    return hash_obj.hexdigest()
