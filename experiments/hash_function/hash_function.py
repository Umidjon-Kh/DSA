from typing import Any

# ── Constants ─────────────────────────────────────────────────────────────────

_KNUTH_CONSTANT = 2654435761  # prime close to 2^32 / golden ratio
_GOLDEN_RATIO = 1.6180339887
_DJB2_INIT = 5381
_DJB2_MULT = 33
_FRAC_PRECISION = 10**10  # precision for float fractional part


# ── Internal helpers ──────────────────────────────────────────────────────────


def _hash_int(key: int) -> int:
    """
    Hashes an integer key using Knuth's multiplicative method.

    Multiplies by a large prime constant close to 2^32 / golden ratio.
    This "scrambles" the bits of the key — even keys that are multiples
    of capacity (like 10, 20, 30 with capacity=10) get spread evenly.

    Time complexity: O(1)
    """
    return (key * _KNUTH_CONSTANT + 0x9E3779B9) << 6


def _hash_float(key: float) -> int:
    """
    Hashes a float key without losing precision.

    First multiplies by golden ratio to guarantee a non-zero fractional
    part even for whole numbers like 10.0 or 100.0. Then splits into
    integer and fractional parts and hashes both separately.

    Time complexity: O(1)
    """
    if key.is_integer():
        return _hash_int(int(key))
    scrambled = key * _GOLDEN_RATIO
    int_part = int(scrambled)
    frac_part = scrambled - int_part
    frac_as_int = int(frac_part * _FRAC_PRECISION)
    combined = int_part * _KNUTH_CONSTANT + frac_as_int * _DJB2_MULT
    return (combined * _KNUTH_CONSTANT + 0x9E3779B9) << 6


def _hash_str(key: str) -> int:
    """
    Hashes a string key using the djb2 algorithm.

    Each character accumulates into the running hash via:
        hash = hash * 33 + ord(char)
    The multiplication on the running total means character order matters —
    "name" and "mane" produce different results.

    Time complexity: O(k) where k is the length of the string
    """
    hash_val = _DJB2_INIT
    for char in key:
        hash_val = hash_val * _DJB2_MULT + ord(char)
    return ((hash_val % 1_000_003) * _KNUTH_CONSTANT + 0x9E3779B9) << 6


def _hash_tuple(key: tuple) -> int:
    """
    Hashes a tuple key by applying hash_key to each element recursively.

    Uses djb2 accumulation across all element hashes.
    Raises TypeError if any element inside the tuple is mutable
    (list, dict, set) — matching Python's own behaviour.

    Time complexity: O(n) where n is total number of elements recursively
    """
    hash_val = _DJB2_INIT
    for element in key:
        if isinstance(element, (list, dict, set)):
            raise TypeError(f"Unhashable type inside tuple: {type(element).__name__!r}")
        element_hash = _hash_raw(element) % 1_000_003
        hash_val ^= element_hash + 0x9E3779B9 + (hash_val << 6) + (hash_val >> 2)
    return hash_val


# ── Public interface ──────────────────────────────────────────────────────────


def _hash_raw(key: Any) -> int:
    """
    Main hash router — dispatches to the correct hash function by type.

    Supported key types:
        int, bool → _hash_int   (bool is subclass of int in Python)
        float     → _hash_float
        str       → _hash_str
        tuple     → _hash_tuple (recursive — all elements must be hashable)

    All results are guaranteed to be in range [0, capacity).

    Time complexity: O(k) where k is the size/length of the key

    Raises:
        TypeError: If key type is not hashable (list, dict, set, or
                   any unsupported type).
    """
    if isinstance(key, bool):
        return _hash_int(int(key))
    if isinstance(key, int):
        return _hash_int(key)
    if isinstance(key, float):
        return _hash_float(key)
    if isinstance(key, str):
        return _hash_str(key)
    if isinstance(key, tuple):
        return _hash_tuple(key)
    else:
        raise TypeError(f"Unhashable type: {type(key).__name__!r}")


def hash_key(key: Any, capacity: int) -> int:
    return _hash_raw(key) % capacity


def next_prime(n: int) -> int:
    """
    Returns the smallest prime number greater than n.

    Used by resize() to find the next capacity — hash tables perform
    better when capacity is prime because it reduces clustering after
    the modulo operation.

    Time complexity: O(n * sqrt(n)) — fast enough for table sizes
    """
    candidate = n + 1
    while True:
        if _is_prime(candidate):
            return candidate
        candidate += 1


def _is_prime(n: int) -> bool:
    """
    Returns True if n is a prime number.

    Checks divisibility up to sqrt(n) — any factor larger than sqrt(n)
    would have a corresponding factor smaller than sqrt(n).

    Time complexity: O(sqrt(n))
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True
