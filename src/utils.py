from urllib.parse import urlparse

BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def encode_base62(num: int) -> str:
    """Encode a positive integer into a Base62 string."""
    if num < 0:
        raise ValueError("num must be non-negative")
    if num == 0:
        return BASE62_ALPHABET[0]

    base = len(BASE62_ALPHABET)
    chars = []
    while num > 0:
        num, rem = divmod(num, base)
        chars.append(BASE62_ALPHABET[rem])
    return "".join(reversed(chars))


def decode_base62(code: str) -> int:
    """Decode a Base62 string into an integer."""
    if not code:
        raise ValueError("code must be non-empty")

    base = len(BASE62_ALPHABET)
    char_to_val = {ch: i for i, ch in enumerate(BASE62_ALPHABET)}

    num = 0
    for ch in code:
        if ch not in char_to_val:
            raise ValueError(f"Invalid Base62 character: {ch}")
        num = num * base + char_to_val[ch]
    return num


def is_valid_url(url: str) -> bool:
    """
    Minimal URL validation.
    Accepts only http/https URLs with a netloc.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)