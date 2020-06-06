import uuid
import hashlib
from typing import Optional

import hashids


# IMPORTANT: read it from environment variables instead!..
DEFAULT_SALT = 'This is my horse, my horse is amazing!'


def encode(identifier: int, salt: Optional[str] = DEFAULT_SALT) -> str:
    """Hashes the given text into a unique (collision free), short, and reproducible hash-code..."""
    hashids_processor = hashids.Hashids(salt=salt)
    hashed_value = hashids_processor.encode(identifier)
    return hashed_value


def decode(hash_id: str, salt: Optional[str] = DEFAULT_SALT) -> int:
    """Returns full URL (if exists) by the given short URL..."""
    hashids_processor = hashids.Hashids(salt=salt)
    identifier = hashids_processor.decode(hash_id)[0]
    return identifier
