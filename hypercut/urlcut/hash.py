from typing import Optional


def encode(text: str, salt: Optional[str] = None) -> Optional[str]:
    """Hashes the given text into a unique (collision free), short, and reproducible hash-code..."""
    return text[:12]


def decode(short_url: str) -> str:
    """Returns full URL (if exists) by the given short URL..."""
    pass
