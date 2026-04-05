from typing import Any

# ── Constants ─────────────────────────────────────────────────────────────────

_KNUTH_CONSTANT = 2654435761  # prime close to 2^32 / golden ratio
_GOLDEN_RATIO = 1.6180339887
_DJB2_INIT = 5381
_DJB2_MULT = 33
_FRAC_PRECISION = 10**10  # precision for float fractional part
_BOOST_CONSTANT = 0x9E3779B9  # 2^32 / golden ratio in hex — used in boost::hash_combine
_STR_NORMALIZER = 1_000_003  # prime used to normalize str hash before final mix
_TUP_NORMALIZER = 1_000_003  # prime used to normalize each tuple element hash


# ── Internal helpers ──────────────────────────────────────────────────────────


def _hash_int(key: int) -> int:
    """
    Hashes an integer key using Knuth's multiplicative method
    combined with a bit shift for extra scrambling.

    Multiplies by a large prime constant close to 2^32 / golden ratio,
    adds the boost constant to avoid zero-clustering, then shifts left
    by 6 bits (multiplies by 64) to widen the output range.

    This ensures that keys which are multiples of capacity
    (e.g. 10, 20, 30 with capacity=10) do not all land in bucket 0.

    Time complexity: O(1)
    """
    return (key * _KNUTH_CONSTANT + _BOOST_CONSTANT) << 6


def _hash_float(key: float) -> int:
    """
    Hashes a float key without losing precision.

    Whole floats (1.0, 2.0) delegate to _hash_int to match Python's
    own behaviour where hash(1) == hash(1.0).

    For fractional floats: multiplies by golden ratio first to guarantee
    a non-zero fractional part, then splits into integer and fractional
    components and hashes both. Final result goes through the same
    Knuth + boost + shift mix as _hash_int.

    Time complexity: O(1)
    """
    if key.is_integer():
        return _hash_int(int(key))
    scrambled = key * _GOLDEN_RATIO
    int_part = int(scrambled)
    frac_part = scrambled - int_part
    frac_as_int = int(frac_part * _FRAC_PRECISION)
    combined = int_part * _KNUTH_CONSTANT + frac_as_int * _DJB2_MULT
    return (combined * _KNUTH_CONSTANT + _BOOST_CONSTANT) << 6


def _hash_str(key: str) -> int:
    """
    Hashes a string key using the djb2 algorithm followed by a
    Knuth multiplicative mix.

    djb2 accumulates each character via:
        hash = hash * 33 + ord(char)
    Multiplication on the running total means character order matters —
    "name" and "mane" always produce different values.

    After djb2 the result is normalized by a prime (_STR_NORMALIZER)
    to reduce the magnitude before the final Knuth + boost + shift mix.
    This keeps max_chain low even for large tables.

    Time complexity: O(k) where k is the length of the string
    """
    hash_val = _DJB2_INIT
    for char in key:
        hash_val = hash_val * _DJB2_MULT + ord(char)
    return ((hash_val % _STR_NORMALIZER) * _KNUTH_CONSTANT + _BOOST_CONSTANT) << 6


def _hash_tuple(key: tuple) -> int:
    """
    Hashes a tuple key using boost::hash_combine style XOR accumulation.

    Each element is hashed via _hash_raw and normalized by _TUP_NORMALIZER
    before being folded into the running hash with:
        hash ^= element_hash + BOOST + (hash << 6) + (hash >> 2)

    This pattern (from C++ boost library) produces excellent avalanche
    behaviour — a single bit change in any element changes roughly half
    the bits of the final hash. It also handles element order correctly:
    (1, 2) and (2, 1) always produce different results.

    Raises TypeError if any element is mutable (list, dict, set).

    Time complexity: O(n) where n is total number of elements recursively
    """
    hash_val = _DJB2_INIT
    for element in key:
        if isinstance(element, (list, dict, set)):
            raise TypeError(f"Unhashable type inside tuple: {type(element).__name__!r}")
        element_hash = _hash_raw(element) % _TUP_NORMALIZER
        hash_val ^= element_hash + _BOOST_CONSTANT + (hash_val << 6) + (hash_val >> 2)
    return hash_val


def _is_prime(n: int) -> bool:
    """
    Returns True if n is a prime number.

    Checks divisibility only up to sqrt(n) — any composite number n
    must have a factor <= sqrt(n), so checking beyond that is redundant.
    Even numbers are eliminated first, then only odd divisors are checked.

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


# ── Public interface ──────────────────────────────────────────────────────────


def hash_key(key: Any, capacity: int) -> int:
    """
    Computes the bucket index for given key and capacity.

    Routes to the correct internal hash function based on key type,
    then applies % capacity to produce an index in [0, capacity).

    Supported key types:
        bool  → treated as int (False=0, True=1)
        int   → Knuth multiplicative hash
        float → golden ratio split hash (whole floats delegate to int)
        str   → djb2 + Knuth mix
        tuple → boost::hash_combine style (all elements must be hashable)

    Time complexity: O(k) where k is the size or length of the key

    Raises:
        TypeError: If key is not hashable (list, dict, set, or unknown type).
        TypeError: If a tuple contains a mutable element.
    """
    return _hash_raw(key) % capacity


def next_prime(n: int) -> int:
    """
    Returns the smallest prime number strictly greater than n.

    Used by _resize() to find the next table capacity — hash tables
    perform better with prime capacities because it reduces clustering
    after the modulo operation.

    Examples:
        next_prime(10)  → 11
        next_prime(20)  → 23
        next_prime(100) → 101

    Time complexity: O(n * sqrt(n)) — acceptable for table sizes
    """
    candidate = n + 1
    while True:
        if _is_prime(candidate):
            return candidate
        candidate += 1


def _hash_raw(key: Any) -> int:
    """
    Internal router — returns raw hash value without % capacity.

    Called by hash_key (which applies % capacity once at the end)
    and by _hash_tuple (which needs raw values for accumulation).
    Keeping % capacity out of internal calls prevents range compression
    that would cause clustering in composite types like tuple.

    Time complexity: O(k) where k is the size or length of the key
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
    raise TypeError(f"Unhashable type: {type(key).__name__!r}")
