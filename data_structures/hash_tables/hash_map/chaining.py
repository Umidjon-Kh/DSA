from typing import Any, Iterator, Optional

from ..._base import BaseHashMap
from ..._tools import hash_key, next_prime
from ...arrays import StaticUniversalArray
from ...nodes import LinearNode

_INITIAL_CAPACITY = 11
_MAX_LOAD_FACTOR = 0.7


class ChainingHashMap(BaseHashMap):
    """
    A hash map that resolves collisions via chaining.

    Each bucket is a singly linked list of LinearNode instances.
    Every node stores a (key, value) tuple in its value slot.
    When two keys hash to the same bucket index they are chained
    together — the new node becomes the new head of that bucket.

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
        is_empty:     O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — yields values
        __reversed__: O(n) — reverse bucket order
        __contains__: O(1) average
        __eq__:       O(n)
        __repr__:     O(n)
    """

    __slots__ = ("_buckets", "_size", "_capacity")

    def __init__(self, *args: tuple) -> None:
        """
        Creates a ChainingHashMap with optional initial key-value pairs.

        Args:
            *args: Optional (key, value) tuples inserted in order.

        Examples:
            m = ChainingHashMap()
            m = ChainingHashMap(("name", "Umidjon"), ("age", 25))
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
        Returns the bucket index for given key.

        Time complexity: O(k) where k is the size of the key
        """
        return hash_key(key, self._capacity)

    def _load_factor(self) -> float:
        """
        Returns current load factor: size / capacity.

        Time complexity: O(1)
        """
        return self._size / self._capacity

    def _get_node(self, key: Any) -> Optional[LinearNode]:
        """
        Returns the node whose value[0] == key, or None if not found.

        Traverses the linked list at the bucket index for given key.

        Time complexity: O(1) average
        """
        index = self._hash(key)
        current = self._buckets[index]
        while current is not None:
            if current.value[0] == key:
                return current
            current = current.next
        return None

    # -------------------------------------------------------------------------
    # Internal resize

    def _resize(self) -> None:
        """
        Grows the bucket array and rehashes all existing pairs.

        New capacity is the next prime after doubling current capacity.
        All existing (key, value) pairs are reinserted — their bucket
        indices change because capacity changed.

        Called automatically by insert when load factor exceeds 0.7.

        Time complexity: O(n)
        """
        old_buckets = self._buckets
        old_capacity = self._capacity

        self._capacity = next_prime(self._capacity * 2)
        self._size = 0
        self._buckets = StaticUniversalArray(capacity=self._capacity)

        for i in range(old_capacity):
            current = old_buckets[i]
            while current is not None:
                key, value = current.value
                self.insert(key, value)
                current = current.next

    # -------------------------------------------------------------------------
    # Core operations

    def insert(self, key: Any, value: Any) -> None:
        """
        Inserts or updates a key-value pair.

        If key exists — updates its value in the existing node.
        If key does not exist — prepends a new node to the bucket.
        Triggers _resize if load factor exceeds 0.7 after insert.

        Prepending is O(1) — no need to traverse to the tail.

        Time complexity: O(1) amortized

        Raises:
            TypeError: If key is not hashable.
        """
        if self._load_factor() >= _MAX_LOAD_FACTOR:
            self._resize()

        node = self._get_node(key)
        if node is not None:
            node.value = (key, value)
            return

        index = self._hash(key)
        new_node = LinearNode((key, value))
        new_node.next = self._buckets[index]
        self._buckets[index] = new_node
        self._size += 1

    def get(self, key: Any, default: Any = None) -> Any:
        """
        Returns the value for key, or default if key not found.

        Time complexity: O(1) average
        """
        node = self._get_node(key)
        return node.value[1] if node is not None else default

    def delete(self, key: Any) -> None:
        """
        Removes the key-value pair with given key.

        Traverses the bucket keeping a prev pointer to relink nodes.
        If key not found — does nothing.

        Time complexity: O(1) average
        """
        index = self._hash(key)
        prev = None
        current = self._buckets[index]

        while current is not None:
            if current.value[0] == key:
                if prev is None:
                    self._buckets[index] = current.next
                else:
                    prev.next = current.next
                self._size -= 1
                return
            prev = current
            current = current.next

    def contains(self, key: Any) -> bool:
        """
        Returns True if key exists in the map.

        Time complexity: O(1) average
        """
        return self._get_node(key) is not None

    def setdefault(self, key: Any, default: Any = None) -> Any:
        """
        Returns value for key if it exists.
        If key not found — inserts (key, default) and returns default.

        Time complexity: O(1) average
        """
        node = self._get_node(key)
        if node is not None:
            return node.value[1]
        self.insert(key, default)
        return default

    # -------------------------------------------------------------------------
    # Iterators

    def keys(self) -> Iterator[Any]:
        """
        Yields all keys in bucket order.

        Time complexity: O(n)
        """
        for i in range(self._capacity):
            current = self._buckets[i]
            while current is not None:
                yield current.value[0]
                current = current.next

    def values(self) -> Iterator[Any]:
        """
        Yields all values in bucket order.

        Time complexity: O(n)
        """
        for i in range(self._capacity):
            current = self._buckets[i]
            while current is not None:
                yield current.value[1]
                current = current.next

    def items(self) -> Iterator[tuple]:
        """
        Yields all (key, value) pairs in bucket order.

        Time complexity: O(n)
        """
        for i in range(self._capacity):
            current = self._buckets[i]
            while current is not None:
                yield current.value
                current = current.next

    # -------------------------------------------------------------------------
    # Internal deep copy helper

    def _deep_copy_value(self, value: Any) -> Any:
        """
        Recursively deep copies a value.

        ChainingHashMap → deepcopy()
        list            → new list with deep copied elements
        dict            → new dict with deep copied values
        tuple           → new tuple with deep copied elements
        other           → returned as-is (immutable)

        Time complexity: O(n) where n is total nested size
        """
        if isinstance(value, ChainingHashMap):
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

        Drops the reference to the bucket array — GC handles the nodes.

        Time complexity: O(1)
        """
        self._capacity = _INITIAL_CAPACITY
        self._size = 0
        self._buckets = StaticUniversalArray(capacity=self._capacity)

    def copy(self) -> "ChainingHashMap":
        """
        Returns a shallow copy — structure is new but values are shared.

        Time complexity: O(n)
        """
        new_map = ChainingHashMap()
        for key, value in self.items():
            new_map.insert(key, value)
        return new_map

    def deepcopy(self) -> "ChainingHashMap":
        """
        Returns a deep copy — structure and all nested values are new.

        Recursively copies lists, dicts, tuples, and nested
        ChainingHashMap instances. Immutable values (int, str, float,
        bool) are shared — they cannot change.

        Time complexity: O(n) where n is total nested size
        """
        new_map = ChainingHashMap()
        for key, value in self.items():
            new_map.insert(key, self._deep_copy_value(value))
        return new_map

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the map contains no pairs. O(1)"""
        return self._size == 0

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of key-value pairs. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the map is not empty. O(1)"""
        return self._size > 0

    def __getitem__(self, key: Any) -> Any:
        """
        Returns value for key.
        Format: map["name"]

        Raises:
            KeyError: If key not found.
        """
        node = self._get_node(key)
        if node is None:
            raise KeyError(key)
        return node.value[1]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Inserts or updates key-value pair.
        Format: map["name"] = "Umidjon"
        """
        self.insert(key, value)

    def __delitem__(self, key: Any) -> None:
        """
        Removes item by received key from map.
        Format: del map["key"]
        If key does not exits not raises any error just ignores it.
        """
        self.delete(key)

    def __iter__(self) -> Iterator[Any]:
        """
        Yields values in bucket order.

        Note: yields values not keys — use keys() for keys,
        items() for (key, value) pairs.

        Time complexity: O(n)
        """
        yield from self.values()

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields values in reverse bucket order.

        Time complexity: O(n)
        """
        for i in range(self._capacity - 1, -1, -1):
            current = self._buckets[i]
            while current is not None:
                yield current.value[1]
                current = current.next

    def __contains__(self, key: Any) -> bool:
        """Returns True if key exists in the map. O(1) average"""
        return self.contains(key)

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both maps contain the same key-value pairs.

        Order and internal bucket layout do not matter — only the
        set of (key, value) pairs is compared.

        Time complexity: O(n)
        """
        if not isinstance(other, ChainingHashMap):
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
        Format: ChainingHashMap(size=2){"name": "Umidjon", "age": 25}

        Time complexity: O(n)
        """
        pairs = ", ".join(f"{key!r}: {value!r}" for key, value in self.items())
        return f"ChainingHashMap(size={self._size})" + "{" + pairs + "}"
