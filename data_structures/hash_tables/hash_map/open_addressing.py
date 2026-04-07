from typing import Any, Iterator, Optional

from ..._base import BaseHashMap
from ..._tools import hash_key, next_prime
from ...arrays import StaticUniversalArray

_INITIAL_CAPACITY = 11
_MAX_LOAD_FACTOR = 0.7


class OpenAddressingHashMap(BaseHashMap):
    """
    A hash map that resolves collisions via linear probing.

    Each bucket holds exactly one (key, value) tuple, None, or a
    _DELETED tombstone marker. When a collision occurs the map probes
    forward — (index + 1) % capacity — until a free slot is found.

    Deletion uses a tombstone (_DELETED) instead of None so that
    probe sequences started before the deletion remain intact.
    Tombstones are cleared automatically on every resize.

    Resizes automatically when load factor exceeds 0.7.
    New capacity is always the next prime after doubling.

    Time complexity:
        insert:       O(1) amortized — O(n) on resize
        get:          O(1) average
        delete:       O(1) average
        contains:     O(1) average
        setdefault:   O(1) average
        keys:         O(n)
        values:       O(n)
        items:        O(n)
        _resize:      O(n)
        clear:        O(1)
        copy:         O(n)
        deepcopy:     O(n)
        __getitem__:  O(1) avarage
        __setitem__:  O(1) avarage
        __delitem__:  O(1) avarage
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — yields values
        __reversed__: O(n) — reverse bucket order
        __contains__: O(1) average
        __eq__:       O(n)
        __repr__:     O(n)
    """

    _DELETED = object()

    __slots__ = ("_buckets", "_size", "_capacity")

    def __init__(self, *args: tuple) -> None:
        """
        Creates an OpenAddressingHashMap with optional initial key-value pairs.

        Args:
            *args: Optional (key, value) tuples inserted in order.

        Examples:
            m = OpenAddressingHashMap()
            m = OpenAddressingHashMap(("name", "Umidjon"), ("age", 25))
        """
        self._capacity: int = _INITIAL_CAPACITY
        self._size: int = 0
        self._buckets: StaticUniversalArray = StaticUniversalArray(
            capacity=self._capacity
        )

        for item in args:
            self.insert(item[0], item[1])

    # -------------------------------------------------------------------------
    # Internal helpers

    def _hash(self, key: Any) -> int:
        """
        Returns the initial bucket index for given key.

        Time complexity: O(k) where k is the size of the key
        """
        return hash_key(key, self._capacity)

    def _load_factor(self) -> float:
        """
        Returns current load factor: size / capacity.

        Time complexity: O(1)
        """
        return self._size / self._capacity

    def _probe(self, key: Any) -> tuple:
        """
        Probes the bucket array for given key using linear probing.

        Returns (index, found) where:
            index — the slot where key was found or should be inserted
            found — True if key exists, False otherwise

        Traversal rules:
            None     -> key does not exist, this slot is free for insert
            _DELETED -> skip (tombstone), continue probing
            (k, v)   -> compare k with key, stop if match

        Tracks the first _DELETED slot seen — if key is not found,
        returns that slot index so insert can reuse it.

        Stops after capacity steps to guarantee termination even if
        the table contains no None slots (only possible without resize,
        kept as a safety guard).

        Time complexity: O(1) average
        """
        index = self._hash(key)
        first_deleted: Optional[int] = None
        step = 0

        while step < self._capacity:
            slot = self._buckets[index]

            if slot is None:
                if first_deleted is not None:
                    return first_deleted, False
                return index, False

            if slot is self._DELETED:
                if first_deleted is None:
                    first_deleted = index

            elif slot[0] == key:
                return index, True

            step += 1
            index = (index + 1) % self._capacity

        if first_deleted is not None:
            return first_deleted, False
        return index, False

    # -------------------------------------------------------------------------
    # Internal resize

    def _resize(self) -> None:
        """
        Grows the bucket array and rehashes all existing pairs.

        New capacity is the next prime after doubling current capacity.
        All _DELETED tombstones are dropped — they are not reinserted.
        All existing (key, value) pairs are reinserted using new capacity.

        Called automatically by insert when load factor exceeds 0.7.

        Time complexity: O(n)
        """
        old_buckets = self._buckets
        old_capacity = self._capacity

        self._capacity = next_prime(self._capacity * 2)
        self._size = 0
        self._buckets = StaticUniversalArray(capacity=self._capacity)

        for i in range(old_capacity):
            slot = old_buckets[i]
            if slot is None or slot is self._DELETED:
                continue
            self.insert(slot[0], slot[1])

    # -------------------------------------------------------------------------
    # Core operations

    def insert(self, key: Any, value: Any) -> None:
        """
        Inserts or updates a key-value pair.

        If key exists — updates value in place.
        If key does not exist — places (key, value) at the probed slot.
        Triggers _resize if load factor exceeds 0.7 before insert.

        Time complexity: O(1) amortized

        Raises:
            TypeError: If key is not hashable.
        """
        if self._load_factor() >= _MAX_LOAD_FACTOR:
            self._resize()

        index, found = self._probe(key)

        if found:
            self._buckets[index] = (key, value)
            return

        self._buckets[index] = (key, value)
        self._size += 1

    def get(self, key: Any, default: Any = None) -> Any:
        """
        Returns the value for key, or default if key not found.

        Time complexity: O(1) average
        """
        index, found = self._probe(key)
        if not found:
            return default
        return self._buckets[index][1]

    def delete(self, key: Any) -> None:
        """
        Removes the key-value pair with given key.

        Places a _DELETED tombstone at the slot so that probe sequences
        through this slot remain intact for future lookups.
        If key not found — does nothing.

        Tombstones are cleaned up automatically on the next _resize.

        Time complexity: O(1) average
        """
        index, found = self._probe(key)
        if not found:
            return
        self._buckets[index] = self._DELETED
        self._size -= 1

    def contains(self, key: Any) -> bool:
        """
        Returns True if key exists in the map.

        Time complexity: O(1) average
        """
        _, found = self._probe(key)
        return found

    def setdefault(self, key: Any, default: Any = None) -> Any:
        """
        Returns value for key if it exists.
        If key not found — inserts (key, default) and returns default.

        Time complexity: O(1) average
        """
        index, found = self._probe(key)
        if found:
            return self._buckets[index][1]
        self.insert(key, default)
        return default

    # -------------------------------------------------------------------------
    # Iterators

    def keys(self) -> Iterator[Any]:
        """
        Yields all keys skipping None and _DELETED slots.

        Time complexity: O(n)
        """
        for i in range(self._capacity):
            slot = self._buckets[i]
            if slot is None or slot is self._DELETED:
                continue
            yield slot[0]

    def values(self) -> Iterator[Any]:
        """
        Yields all values skipping None and _DELETED slots.

        Time complexity: O(n)
        """
        for i in range(self._capacity):
            slot = self._buckets[i]
            if slot is None or slot is self._DELETED:
                continue
            yield slot[1]

    def items(self) -> Iterator[tuple]:
        """
        Yields all (key, value) pairs skipping None and _DELETED slots.

        Time complexity: O(n)
        """
        for i in range(self._capacity):
            slot = self._buckets[i]
            if slot is None or slot is self._DELETED:
                continue
            yield slot

    # -------------------------------------------------------------------------
    # Internal deep copy helper

    def _deep_copy_value(self, value: Any) -> Any:
        """
        Recursively deep copies a value.

        OpenAddressingHashMap -> deepcopy()
        list                  -> new list with deep copied elements
        dict                  -> new dict with deep copied values
        tuple                 -> new tuple with deep copied elements
        other                 -> returned as-is (immutable)

        Time complexity: O(n) where n is total nested size
        """
        if isinstance(value, OpenAddressingHashMap):
            return value.deepcopy()
        if isinstance(value, list):
            return [self._deep_copy_value(v) for v in value]
        if isinstance(value, dict):
            return {k: self._deep_copy_value(v) for k, v in value.items()}
        if isinstance(value, tuple):
            return tuple(self._deep_copy_value(v) for v in value)
        return value

    # -------------------------------------------------------------------------
    # Collection methods

    def clear(self) -> None:
        """
        Removes all pairs and resets to initial capacity.

        Time complexity: O(1)
        """
        self._capacity = _INITIAL_CAPACITY
        self._size = 0
        self._buckets = StaticUniversalArray(capacity=self._capacity)

    def copy(self) -> "OpenAddressingHashMap":
        """
        Returns a shallow copy — structure is new but values are shared.

        Time complexity: O(n)
        """
        new_map = OpenAddressingHashMap()
        for key, value in self.items():
            new_map.insert(key, value)
        return new_map

    def deepcopy(self) -> "OpenAddressingHashMap":
        """
        Returns a deep copy — structure and all nested values are new.

        Time complexity: O(n) where n is total nested size
        """
        new_map = OpenAddressingHashMap()
        for key, value in self.items():
            new_map.insert(key, self._deep_copy_value(value))
        return new_map

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of key-value pairs. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the map is not empty. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields values in bucket order, skipping empty and deleted slots.

        Time complexity: O(n)
        """
        yield from self.values()

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields values in reverse bucket order.

        Time complexity: O(n)
        """
        for i in range(self._capacity - 1, -1, -1):
            slot = self._buckets[i]
            if slot is None or slot is self._DELETED:
                continue
            yield slot[1]

    def __contains__(self, key: Any) -> bool:
        """Returns True if key exists in the map. O(1) average"""
        return self.contains(key)

    def __getitem__(self, key: Any) -> Any:
        """
        Returns value for key.
        Format: map["name"]

        Raises:
            KeyError: If key not found.
        """
        index, found = self._probe(key)
        if not found:
            raise KeyError(key)
        return self._buckets[index][1]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Inserts or updates key-value pair.
        Format: map["name"] = "Umidjon"
        """
        self.insert(key, value)

    def __delitem__(self, key: Any) -> None:
        """
        Removes key-value pair with given key.
        Format: del map["name"]

        If key not found — does nothing.
        """
        self.delete(key)

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both maps contain the same key-value pairs.

        Order and internal layout do not matter.

        Time complexity: O(n)
        """
        if not isinstance(other, OpenAddressingHashMap):
            return NotImplemented
        if self._size != other._size:
            return False
        for key, value in self.items():
            if not other.contains(key):
                return False
            if other.get(key) != value:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the map.
        Format: OpenAddressingHashMap(size=2){"name": "Umidjon", "age": 25}

        Time complexity: O(n)
        """
        pairs = ", ".join(f"{key!r}: {value!r}" for key, value in self.items())
        return f"OpenAddressingHashMap(size={self._size})" + "{" + pairs + "}"
