"""
Module that handles the hashing of files.

Useful functions:
    compare_hash
"""

import base64
from pathlib import Path

import xxhash


def get_hasher(file_path: Path) -> xxhash.xxh64:
    """
    Get the hasher of a file.

    Args:
        file_path: The path to the file
    """

    chunk_size: int = 256 * 1024    # no particular reason for this size
    hasher: xxhash.xxh64 = xxhash.xxh64()
    with file_path.open('rb') as file:
        while chunk := file.read(chunk_size):
            hasher.update(chunk)
    return hasher

def compare_hash(target: Path|xxhash.xxh64, hash_code: str) -> bool:
    """
    Compare the hash of the target with the given hash code.

    Args:
        target: The file path or hasher to compare
        hash_code: The hash code to compare against
    """

    # Get the hasher object
    hasher: xxhash.xxh64
    if isinstance(target, Path):
        hasher = get_hasher(target)
    else:
        hasher = target

    # Get the hash code in little endian base64 format
    big_endian_hash: bytes = hasher.digest()
    big_endian_int: int = int.from_bytes(big_endian_hash, byteorder = 'big')
    little_endian_hash: bytes = big_endian_int.to_bytes(len(big_endian_hash), 'little')
    base64_little_endian: str = base64.b64encode(little_endian_hash).decode('utf-8')

    return base64_little_endian == hash_code
