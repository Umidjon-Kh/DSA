"""
Hash function collision test.

Compares our custom hash_key against Python's built-in hash()
on 1 million elements of different types.

Metrics:
    collisions     — how many keys share a bucket with another key
    max_chain      — longest bucket chain (worst case search)
    empty_buckets  — how many buckets are unused
    distribution   — std deviation of bucket sizes (lower = better)
"""

import math
import random
import string

from hash_function import hash_key, next_prime

# ── Helpers ───────────────────────────────────────────────────────────────────


def _python_hash(key, capacity: int) -> int:
    return hash(key) % capacity


def _count_collisions(buckets: list) -> dict:
    total = sum(len(b) for b in buckets)
    collisions = sum(len(b) - 1 for b in buckets if len(b) > 1)
    max_chain = max(len(b) for b in buckets)
    empty = sum(1 for b in buckets if len(b) == 0)
    sizes = [len(b) for b in buckets]
    mean = total / len(buckets)
    variance = sum((s - mean) ** 2 for s in sizes) / len(buckets)
    std_dev = math.sqrt(variance)

    return {
        "total": total,
        "collisions": collisions,
        "collision_%": round(collisions / total * 100, 2),
        "max_chain": max_chain,
        "empty_buckets": empty,
        "std_dev": round(std_dev, 4),
    }


def _run_test(keys: list, capacity: int, label: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {label}")
    print(f"  keys={len(keys):,}  capacity={capacity}")
    print(f"{'─' * 60}")

    # our hash
    our_buckets = [[] for _ in range(capacity)]
    for key in keys:
        idx = hash_key(key, capacity)
        our_buckets[idx].append(key)

    # python hash
    py_buckets = [[] for _ in range(capacity)]
    for key in keys:
        idx = _python_hash(key, capacity)
        py_buckets[idx].append(key)

    our = _count_collisions(our_buckets)
    py = _count_collisions(py_buckets)

    print(f"{'metric':<20} {'ours':>12} {'python':>12}")
    print(f"{'─' * 44}")
    for k in our:
        print(f"{k:<20} {str(our[k]):>12} {str(py[k]):>12}")


# ── Tests ─────────────────────────────────────────────────────────────────────

CAPACITY = next_prime(1_000_000)
N = 1_000_000

print(f"\nCapacity (next prime after 1M): {CAPACITY}")

# ── int ───────────────────────────────────────────────────────────────────────

int_keys = random.sample(range(0, 10_000_000), N)
_run_test(int_keys, CAPACITY, "INT keys — random range 0..10M")

int_seq = list(range(0, N * 10, 10))  # multiples of 10
_run_test(int_seq, CAPACITY, "INT keys — multiples of 10 (clustering test)")

# ── float ─────────────────────────────────────────────────────────────────────

float_keys = [random.uniform(-1_000_000, 1_000_000) for _ in range(N)]
_run_test(float_keys, CAPACITY, "FLOAT keys — random")

float_whole = [float(i) for i in range(N)]  # 0.0, 1.0, 2.0 ...
_run_test(float_whole, CAPACITY, "FLOAT keys — whole numbers (0.0, 1.0, ...)")

# ── str ───────────────────────────────────────────────────────────────────────


def _rand_str(length: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


str_keys_short = [_rand_str(5) for _ in range(N)]
_run_test(str_keys_short, CAPACITY, "STR keys — random length 5")

str_keys_long = [_rand_str(20) for _ in range(N)]
_run_test(str_keys_long, CAPACITY, "STR keys — random length 20")

# anagrams — same chars different order
anagram_base = list("abcdefghij")
anagram_keys = []
for _ in range(N):
    random.shuffle(anagram_base)
    anagram_keys.append("".join(anagram_base))
_run_test(anagram_keys, CAPACITY, "STR keys — anagrams (same chars, diff order)")

# ── tuple ─────────────────────────────────────────────────────────────────────

tuple_keys = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(N)]
_run_test(tuple_keys, CAPACITY, "TUPLE keys — (int, int) pairs")

print(f"\n{'═' * 60}")
print("  done")
print(f"{'═' * 60}\n")
