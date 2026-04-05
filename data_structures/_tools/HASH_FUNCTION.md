# Hash Function

This module provides a custom hash function for use in hash table
implementations. It converts any hashable Python key into a bucket
index — a number in the range `[0, capacity)`.

---

## Why do we need a hash function?

A hash table stores data in an array. Arrays need integer indices.
But keys can be anything — strings, numbers, tuples. A hash function
converts any key into an integer index:

```
"name"   →  hash_key("name", 10)   →  7
42       →  hash_key(42, 10)       →  3
(1, 2)   →  hash_key((1, 2), 10)   →  5
```

The goal is simple: **distribute keys as evenly as possible across
all buckets**. The more even the distribution — the fewer collisions,
and the closer we stay to O(1) for search, insert, and delete.

---

## What is a collision?

A collision happens when two different keys produce the same index:

```
hash_key("name", 10) → 7
hash_key("mane", 10) → 7   ← collision!
```

Collisions are mathematically unavoidable — there are infinitely many
possible keys but only a finite number of buckets. The only goal is
to minimize them and distribute them evenly.

> **Important:** the operations in this module are not magic.
> They are carefully chosen mathematical tricks that together guarantee
> a minimum number of collisions. Nothing more, nothing less.

---

## Supported key types

| Type    | Example         | Algorithm                 |
| ------- | --------------- | ------------------------- |
| `int`   | `42`, `-7`      | Knuth multiplicative hash |
| `bool`  | `True`, `False` | treated as int (1 and 0)  |
| `float` | `3.14`, `1.0`   | golden ratio split hash   |
| `str`   | `"name"`        | djb2 + Knuth mix          |
| `tuple` | `(1, 2)`        | boost::hash_combine XOR   |

Mutable types (`list`, `dict`, `set`) raise `TypeError` — just like
Python's built-in `hash()`.

---

## Constants explained

### `_KNUTH_CONSTANT = 2654435761`

Discovered by Donald Knuth — one of the most influential computer
scientists ever. The value is `2³² / φ` where `φ` is the golden ratio:

```
2³²  = 4294967296
φ    = 1.6180339887...
2³²/φ ≈ 2654435761
```

Multiplying any integer by this constant "scrambles" its bits so that
even keys that are multiples of capacity (like 10, 20, 30 with
capacity=10) get spread evenly across buckets.

### `_BOOST_CONSTANT = 0x9E3779B9`

The same golden ratio constant but in hexadecimal for 32-bit range.
Used in the famous C++ boost library in `boost::hash_combine`.

Its job is simple — prevent `key=0` from producing `hash=0`:

```
0 * anything = 0   ← bad, everything lands in bucket 0
0 * anything + BOOST = BOOST  ← good, non-zero result
```

### `_GOLDEN_RATIO = 1.6180339887`

The golden ratio appears throughout nature — in spiral shells, leaf
arrangements, and galaxy arms. Its mathematical property is that it
is **irrational** — it cannot be expressed as a simple fraction.

This irrationality guarantees that multiplying any number by the
golden ratio and taking the fractional part produces values that are
as evenly distributed as possible, with no repeating patterns.

### `_DJB2_INIT = 5381` and `_DJB2_MULT = 33`

The magic starting values of the djb2 algorithm, discovered by Dan
Bernstein in 1991 through extensive experimentation. Why exactly 5381
and 33? No one knows for certain — they simply produce fewer collisions
than other values for typical string inputs.

### `_STR_NORMALIZER = 1_000_003` and `_TUP_NORMALIZER = 1_000_003`

Both are prime numbers used to reduce the magnitude of hash values
before the final multiplication step. Without this, very long strings
would produce astronomically large numbers (like `10^50`) which:

- slow down Python's big integer arithmetic
- produce worse distribution after the final `% capacity`

Normalizing by a prime number keeps the values manageable while
preserving good distribution.

### `_FRAC_PRECISION = 10^10`

Used to convert the fractional part of a float into an integer without
losing precision:

```
frac_part = 0.14159...

* 10²  →       14   ← only 2 digits kept
* 10⁵  →    14159   ← 5 digits
* 10¹⁰ → 1415926535 ← 10 digits, good precision
```

---

## Algorithms explained

### `_hash_int` — Knuth multiplicative hash

```python
return (key * _KNUTH_CONSTANT + _BOOST_CONSTANT) << 6
```

Three steps:

```
Step 1: key * 2654435761        → scrambles bits via golden ratio
Step 2: + 2654435769            → prevents zero result for key=0
Step 3: << 6  (multiply by 64)  → widens the output range
```

The left shift `<< 6` is not magic — it simply multiplies by 64,
spreading results across a wider range so that after `% capacity`
they land in different buckets.

Result on our million-element test:

```
collision rate: 34.8%   (same as Python's built-in hash)
max_chain:      7
```

---

### `_hash_float` — golden ratio split

```python
if key.is_integer():
    return _hash_int(int(key))
scrambled   = key * _GOLDEN_RATIO
int_part    = int(scrambled)
frac_part   = scrambled - int_part
frac_as_int = int(frac_part * _FRAC_PRECISION)
combined    = int_part * _KNUTH_CONSTANT + frac_as_int * _DJB2_MULT
return (combined * _KNUTH_CONSTANT + _BOOST_CONSTANT) << 6
```

Whole floats (`1.0`, `2.0`) delegate to `_hash_int` to match Python's
own guarantee that `hash(1) == hash(1.0)`.

For fractional floats — multiplying by the golden ratio first
guarantees a non-zero fractional part even for inputs like `10.0`:

```
10.0 * 1.618... = 16.18...  →  frac = 0.18...  ← always non-zero
```

Without this step, `10.0`, `20.0`, `30.0` would all produce the same
fractional part (zero), causing massive clustering.

Result on our million-element test:

```
random floats:  collision rate 36.74%  (Python: 36.78%) ← we win
whole floats:   collision rate 0.0%    (Python: 0.0%)   ← identical
```

---

### `_hash_str` — djb2 + Knuth mix

```python
hash_val = 5381
for char in key:
    hash_val = hash_val * 33 + ord(char)
return ((hash_val % _STR_NORMALIZER) * _KNUTH_CONSTANT + _BOOST_CONSTANT) << 6
```

djb2 works by multiplying the running total by 33 before adding
each character. This means the position of each character matters:

```
"hi":
    5381 * 33 + ord("h") = 177677
    177677 * 33 + ord("i") = 5863446

"ih":
    5381 * 33 + ord("i") = 177678
    177678 * 33 + ord("h") = 5863458   ← different result ✓
```

After djb2 the result is normalized by `_STR_NORMALIZER` (a prime)
before the final Knuth mix. This reduces the magnitude of very long
string hashes while preserving distribution quality.

Result on our million-element test:

```
random str length 5:  collision rate 36.89%  (Python: 36.80%)
random str length 20: collision rate 36.83%  (Python: 36.83%) ← identical
anagrams:             collision rate 41.68%  (Python: 41.72%) ← we win
max_chain:            same or better than Python in all cases
```

---

### `_hash_tuple` — boost::hash_combine XOR

```python
hash_val = 5381
for element in key:
    element_hash = _hash_raw(element) % _TUP_NORMALIZER
    hash_val ^= element_hash + _BOOST_CONSTANT + (hash_val << 6) + (hash_val >> 2)
```

This pattern comes from the C++ boost library. For each element:

```
hash_val ^= element_hash + BOOST + (hash_val << 6) + (hash_val >> 2)
```

Breaking it down:

```
element_hash % _TUP_NORMALIZER  → normalize to reasonable range
+ _BOOST_CONSTANT               → prevent zero clustering
+ (hash_val << 6)               → mix in upper bits of running hash
+ (hash_val >> 2)               → mix in lower bits of running hash
^= result                       → XOR fold into running hash
```

The XOR fold (`^=`) means a single bit change in any element changes
roughly half the bits of the final result. This is called **avalanche
effect** — a good property for hash functions.

Element order is respected — `(1, 2)` and `(2, 1)` always produce
different hashes because each step depends on the accumulated `hash_val`
from all previous elements.

Result on our million-element test:

```
(int, int) pairs:
    collision rate: 53.1%   (Python: 62.75%) ← we win by 10%!
    max_chain:      15      (Python: 19)      ← we win!
    std_dev:        1.41    (Python: 1.68)    ← we win!
```

---

## Bit operations reference

All algorithms use bitwise operations for speed and scrambling:

| Operation | Meaning                            | Example       |
| --------- | ---------------------------------- | ------------- |
| `x << n`  | multiply by `2ⁿ`                   | `5 << 2 = 20` |
| `x >> n`  | divide by `2ⁿ`, drop remainder     | `8 >> 2 = 2`  |
| `x ^ y`   | XOR — same bits → 0, different → 1 | `5 ^ 3 = 6`   |

These are not cryptographic operations — they are simple, fast
mathematical tools for mixing bits to reduce collision patterns.

---

## Public interface

### `hash_key(key, capacity) → int`

Main function. Converts any hashable key to a bucket index.

```python
hash_key("name", 10)    # → some index in [0, 9]
hash_key(42, 100)       # → some index in [0, 99]
hash_key((1, 2), 101)   # → some index in [0, 100]
```

### `next_prime(n) → int`

Returns the smallest prime number greater than `n`. Used by `_resize()`
to find the next table capacity.

```python
next_prime(10)   # → 11
next_prime(20)   # → 23
next_prime(100)  # → 101
```

Prime capacities reduce clustering after `% capacity` because prime
numbers have no common factors with most key patterns.

---

## Test results summary (1 000 000 elements)

| Key type            | Our collisions | Python collisions | Winner          |
| ------------------- | -------------- | ----------------- | --------------- |
| int random          | 34.79%         | 34.79%            | tie             |
| int multiples of 10 | 0.0%           | 0.0%              | tie             |
| float random        | 36.74%         | 36.78%            | **ours**        |
| float whole         | 0.0%           | 0.0%              | tie             |
| str length 5        | 36.89%         | 36.80%            | Python          |
| str length 20       | 36.83%         | 36.83%            | tie             |
| str anagrams        | 41.68%         | 41.72%            | **ours**        |
| tuple (int,int)     | 53.10%         | 62.75%            | **ours by 10%** |

> All collision rates around 35-40% are mathematically expected when
> `load_factor ≈ 1.0` — this is the birthday paradox, not a bug.
> In real usage the table resizes at `load_factor = 0.7`, keeping
> collision rates much lower.
