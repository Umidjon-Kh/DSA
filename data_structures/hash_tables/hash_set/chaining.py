from typing import Any, Iterator, Optional

from ..._base import BaseHashSet
from ..._tools import hash_key, next_prime
from ...arrays import StaticUniversalArray
from ...nodes import LinearNode

_INITIAL_CAPACITY = 11
_MAX_LOAD_FACTOR = 0.7


class ChainingHashSet(BaseHashSet):
    """
    A hash set that resolves collisions via chaining.

    Each bucket is a singly linked list of LinearNode instances.
    Every node stores a single hashable key in its value slot.
    When two keys hash to the same bucket index they are chained
    together — the new node becomes the new head of that bucket.

    A hash set is a hash map without values — only keys are stored.
    Duplicate keys are silently ignored on add.

    Resizes automatically when load factor exceeds 0.7.
    New capacity is always the next prime after doubling.

    Time complexity:
        add:          O(1) amortized — O(n) on resize
        remove:       O(1) average
        contains:     O(1) average
        _resize:      O(n)
        clear:        O(1)
        copy:         O(n)
        __delitem__:  O(1) average
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — yields keys in bucket order
        __reversed__: O(n) — reverse bucket order
        __contains__: O(1) average
        __eq__:       O(n)
        __repr__:     O(n)
    """

    __slots__ = ("_buckets", "_size", "_capacity")

    def __init__(self, *keys: Any) -> None:
        """
        Creates a ChainingHashSet with optional initial keys.

        Args:
            *keys: Optional hashable keys inserted in order.

        Examples:
            s = ChainingHashSet()
            s = ChainingHashSet("name", "age", 25)
        """
        self._capacity: int = _INITIAL_CAPACITY
        self._size: int = 0
        self._buckets: StaticUniversalArray = StaticUniversalArray(
            capacity=self._capacity
        )

        for key in keys:
            self.add(key)

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
        Returns the node whose value == key, or None if not found.

        Traverses the linked list at the bucket index for given key.

        Time complexity: O(1) average
        """
        index = self._hash(key)
        current = self._buckets[index]
        while current is not None:
            if current.value == key:
                return current
            current = current.next
        return None

    # -------------------------------------------------------------------------
    # Internal resize

    def _resize(self) -> None:
        """
        Grows the bucket array and rehashes all existing keys.

        New capacity is the next prime after doubling current capacity.
        All existing keys are reinserted — their bucket indices change
        because capacity changed.

        Called automatically by add when load factor exceeds 0.7.

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
                self.add(current.value)
                current = current.next

    # -------------------------------------------------------------------------
    # Core operations

    def add(self, key: Any) -> None:
        """
        Adds key to the set.

        If key already exists — does nothing.
        If key does not exist — prepends a new node to the bucket.
        Triggers _resize if load factor exceeds 0.7 before add.

        Prepending is O(1) — no need to traverse to the tail.

        Time complexity: O(1) amortized

        Raises:
            TypeError: If key is not hashable.
        """
        if self._load_factor() >= _MAX_LOAD_FACTOR:
            self._resize()

        if self._get_node(key) is not None:
            return

        index = self._hash(key)
        new_node = LinearNode(key)
        new_node.next = self._buckets[index]
        self._buckets[index] = new_node
        self._size += 1

    def remove(self, key: Any) -> None:
        """
        Removes key from the set.

        Traverses the bucket keeping a prev pointer to relink nodes.
        If key not found — does nothing.

        Time complexity: O(1) average
        """
        index = self._hash(key)
        prev = None
        current = self._buckets[index]

        while current is not None:
            if current.value == key:
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
        Returns True if key exists in the set.

        Time complexity: O(1) average
        """
        return self._get_node(key) is not None

    # -------------------------------------------------------------------------
    # Collection methods

    def clear(self) -> None:
        """
        Removes all keys and resets to initial capacity.

        Drops the reference to the bucket array — GC handles the nodes.

        Time complexity: O(1)
        """
        self._capacity = _INITIAL_CAPACITY
        self._size = 0
        self._buckets = StaticUniversalArray(capacity=self._capacity)

    def copy(self) -> "ChainingHashSet":
        """
        Returns a shallow copy — structure is new, keys are shared.

        Keys are always immutable (hashable), so shallow == deep here.

        Time complexity: O(n)
        """
        new_set = ChainingHashSet()
        for key in self:
            new_set.add(key)
        return new_set

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of keys in the set. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the set is not empty. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields all keys in bucket order.

        Time complexity: O(n)
        """
        for i in range(self._capacity):
            current = self._buckets[i]
            while current is not None:
                yield current.value
                current = current.next

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields all keys in reverse bucket order.

        Time complexity: O(n)
        """
        for i in range(self._capacity - 1, -1, -1):
            current = self._buckets[i]
            while current is not None:
                yield current.value
                current = current.next

    def __contains__(self, key: Any) -> bool:
        """Returns True if key exists in the set. O(1) average"""
        return self.contains(key)

    def __delitem__(self, key: Any) -> None:
        """
        Removes key from the set.
        Format: del set["name"]

        If key does not exist — does nothing.

        Time complexity: O(1) average
        """
        self.remove(key)

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both sets contain exactly the same keys.

        Order and internal bucket layout do not matter — only the
        set of keys is compared.

        Time complexity: O(n)
        """
        if not isinstance(other, ChainingHashSet):
            return NotImplemented
        if self._size != other._size:
            return False
        for key in self:
            if not other.contains(key):
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the set.
        Format: ChainingHashSet(size=3){"name", "age", 25}

        Time complexity: O(n)
        """
        keys = ", ".join(repr(key) for key in self)
        return f"ChainingHashSet(size={self._size})" + "{" + keys + "}"
