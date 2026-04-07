# Hash Tables

A **hash table** is a data structure that lets you store and find data almost
instantly — no matter how many elements you have. Instead of searching through
everything one by one, a hash table uses a **hash function** to jump directly
to the right spot.

Hash tables are everywhere: Python's `dict` and `set` are hash tables,
every database index uses them, and they power language interpreters,
caches, and symbol tables.

This layer implements two structures, each in two collision-resolution flavours:

- **HashMap** — stores key → value pairs (like Python's `dict`)
- **HashSet** — stores keys only, no values (like Python's `set`)

Both come in two variants:

- **Chaining** — each bucket holds a linked list of entries
- **Open Addressing** — all entries live inside the bucket array itself

---

## The core idea

Imagine you have 1 000 000 books and you want to find one by title.
Checking them one by one could take 1 000 000 steps. A hash table does it
in roughly **1 step** on average.

Here is how:

```
key: "Harry Potter"
         │
         ▼
   hash_function("Harry Potter", capacity=11)
         │
         ▼
   bucket index: 4
         │
         ▼
   table[4] → value
```

The hash function converts any key into an integer index. You store the
value at that index. When you look it up later you apply the same function
and land on the same index — instant access.

> For a detailed explanation of how the hash function itself works,
> see [`_tools/HASH_FUNCTION.md`](../_tools/HASH_FUNCTION.md).

---

## Key vocabulary

| Term        | Meaning                                               |
| ----------- | ----------------------------------------------------- |
| key         | The thing you look up by (e.g. `"name"`, `42`)        |
| value       | The data you store (e.g. `"Umidjon"`, `[1, 2, 3]`)    |
| bucket      | One slot in the internal array                        |
| hash        | The integer index produced by the hash function       |
| collision   | Two different keys that produce the same bucket index |
| load factor | `size / capacity` — how full the table is             |
| resize      | Growing the bucket array when the table gets too full |

---

## What is a collision?

No matter how good your hash function is, two different keys can end up at
the same bucket index:

```
hash("name", 11) → 7
hash("mane", 11) → 7   ← collision! same index, different key
```

This happens because there are infinitely many possible keys but only a
finite number of buckets. The question is not _whether_ collisions happen —
they always do — but _how you handle them_. This is where the two variants
come in.

---

## Chaining

In chaining each bucket is a **linked list**. If two keys collide they
simply become neighbours in the same bucket's list.

```
buckets:
  [0] → None
  [1] → ("city", "Tokyo") → None
  [2] → None
  [3] → ("age", 25) → ("zip", 100) → None   ← two keys in bucket 3
  [4] → ("name", "Umidjon") → None
  ...
```

**Insert:** hash the key, prepend a new node to that bucket's list. O(1).

**Get:** hash the key, walk the list at that bucket until you find the key. O(1) average.

**Delete:** hash the key, walk the list, unlink the node. O(1) average.

Chaining is simple and handles high load factors gracefully — buckets just
grow longer. The downside is that every entry allocates a separate node object.

---

## Open Addressing

In open addressing the bucket array holds entries **directly** — no linked
lists at all. When a collision happens the algorithm **probes** for the next
available slot.

This implementation uses **linear probing**: if bucket `i` is taken,
try `i+1`, then `i+2`, and so on (wrapping around).

```
insert("name", "Umidjon") → hash → bucket 4 is free → store there
insert("mane", "Dilnoza") → hash → bucket 4 is taken → try 5 → free → store there

buckets:
  [0] → empty
  [1] → empty
  [2] → empty
  [3] → empty
  [4] → ("name", "Umidjon")
  [5] → ("mane", "Dilnoza")   ← probed to the next slot
  ...
```

**Deleted slots** are marked with a special **tombstone** sentinel so that
probing chains are not broken. Without tombstones, deleting an entry in the
middle of a chain would make everything after it invisible.

```
Before delete:      After delete (with tombstone):

  [4] → ("name", …)    [4] → ("name", …)
  [5] → ("mane", …)    [5] → TOMBSTONE      ← marker, not empty
  [6] → ("amen", …)    [6] → ("amen", …)    ← still reachable
```

Open addressing is cache-friendly because all data sits in one contiguous
array. The downside is that it degrades fast when the load factor is high —
probing chains get long.

---

## Load factor and resizing

Both variants track the **load factor**:

```
load_factor = size / capacity
```

When the load factor exceeds **0.7** (70% full) the table automatically
resizes — a new bucket array is created with the next prime number after
`capacity * 2`, and every existing entry is reinserted.

```
capacity = 11, size = 8  →  load_factor = 0.72  →  resize!
new_capacity = next_prime(22) = 23
all 8 entries reinserted into the 23-bucket array
```

Why a **prime** number for capacity? Because prime capacities reduce the
chance of keys clustering into a small number of buckets, regardless of
which hash function is used.

Why **0.7** as the threshold? It is an empirically chosen sweet spot:
below 0.7 the table is fast; above 0.7 collisions grow quickly and
performance degrades.

---

## HashMap vs HashSet

| Feature      | HashMap                        | HashSet                |
| ------------ | ------------------------------ | ---------------------- |
| Stores       | key → value pairs              | keys only              |
| Python equiv | `dict`                         | `set`                  |
| Main use     | lookup table, cache, counter   | membership test, dedup |
| insert       | `insert(key, value)`           | `add(key)`             |
| lookup       | `get(key)` / `map[key]`        | `contains(key)`        |
| delete       | `delete(key)` / `del map[key]` | `remove(key)`          |

A HashSet is simply a HashMap where you do not care about the value — it
stores only keys and answers "is this key present?".

---

## Quick Reference

```
hash_tables/
├── hash_map/
│   ├── chaining.py          # ChainingHashMap
│   └── open_addressing.py   # OpenAddressingHashMap
└── hash_set/
    ├── chaining.py          # ChainingHashSet
    └── open_addressing.py   # OpenAddressingHashSet
```

| Class                   | Strategy       | insert      | get / contains | delete   |
| ----------------------- | -------------- | ----------- | -------------- | -------- |
| `ChainingHashMap`       | linked lists   | O(1) amort. | O(1) avg       | O(1) avg |
| `OpenAddressingHashMap` | linear probing | O(1) amort. | O(1) avg       | O(1) avg |
| `ChainingHashSet`       | linked lists   | O(1) amort. | O(1) avg       | O(1) avg |
| `OpenAddressingHashSet` | linear probing | O(1) amort. | O(1) avg       | O(1) avg |

All four resize automatically and keep the load factor below 0.7.

**When to use which variant?**

- Use **Chaining** when you expect a high number of entries or unpredictable
  load — it degrades more gracefully.
- Use **Open Addressing** when you want better cache performance and the
  load factor stays comfortably below 0.7.

---

## Example usage

```python
from data_structures import ChainingHashMap, ChainingHashSet

# HashMap — store and retrieve key-value pairs
m = ChainingHashMap()
m.insert("name", "Umidjon")
m.insert("city", "Tashkent")
print(m.get("name"))          # Umidjon
print(m["city"])              # Tashkent
m.delete("city")

# Or pass initial pairs directly
m2 = ChainingHashMap(("a", 1), ("b", 2))

# Iterate
for key in m.keys(): print(key)
for key, val in m.items(): print(key, val)

# HashSet — membership only
s = ChainingHashSet()
s.add("apple")
s.add("banana")
print(s.contains("apple"))    # True
print(s.contains("grape"))    # False
s.remove("banana")
```
