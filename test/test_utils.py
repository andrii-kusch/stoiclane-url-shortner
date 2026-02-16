import pytest
from src.utils import encode_base62, decode_base62, is_valid_url


def test_base62_roundtrip_small_numbers():
    for n in range(0, 1000):
        code = encode_base62(n)
        assert decode_base62(code) == n


def test_encode_negative_raises():
    with pytest.raises(ValueError):
        encode_base62(-1)


def test_decode_invalid_char_raises():
    with pytest.raises(ValueError):
        decode_base62("abc$")


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://example.com", True),
        ("http://example.com/path", True),
        ("ftp://example.com", False),
        ("example.com", False),
        ("", False),
    ],
)
def test_is_valid_url(url, expected):
    assert is_valid_url(url) is expected