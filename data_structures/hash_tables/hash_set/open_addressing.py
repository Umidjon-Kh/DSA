from typing import Any, Iterator, Optional

from ..._base import BaseHashSet
from ..._tools import hash_key, next_prime
from ...arrays import StaticUniversalArray

_INITIAL_CAPACITY = 11
_MAX_LOAD_FACTOR = 0.7


class OpenAddressingHashSet(BaseHashSet):
    """
    A hash set that resolves collisions via linear probing.

    Each bucket holds only one hashable(immutable) key, None, or a
    _DELETED tombstone marker. When a collison occurs tha map probes
    forward - (index + 1) % capacity - until a free slot is found.

    Deletion uses a tombstone (_DELETED) instead of None so that
    probe sequences started before the deletion remain intact,
    Tombstones are cleared automatically on every resize.

    Resizes automatically when load factor is exceeds 0.7.
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

    _DELETED = object()

    __slots__ = ("_buckets", "_size", "_capacity")

    def __init__(self, *keys: Any) -> None:
        """
        Creates an OpenAddressingHashSet with optional initial keys.

        Args:
            *keys: Optional initial keys inserted in order.

        Examples:
            s = OpenAddressingHashSet()
            s = OpenAddressingHashSet("name", "age", 25)
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

        Time complexity: O(k) where k is the size of the key.
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
        Probes the bucked array for given key using linear probing.

        Returns (index, found) where:
            index - the slot where key was found or should be inserted.
            found - True if key is exists, False otherwise

        Traversal rules:
            None    -> key does not exist, this slot is free for insert
            _DELETED -> skip (tombstone), continue probing
            exist_key      -> compare key with exist_key, stop if match

        Tracks the first _DELETED slot seen - if key is not found,
        returns that slot index so insert can reuse it.

        Stops after capacity steps to guarantee termination even if
        the table contains no None slots (only possible without resize,
        kept as a safety guard).

        Time complexity: O(1) avarage
        """
        index = self._hash(key)
        first_deleted: Optional[int] = None
        step = 0

        while step < self._capacity:
            slot = self._buckets[index]

            if slot is None:
                if first_deleted is None:
                    first_deleted = index

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
        Grows the bucket array and rehashes all existing keys.

        New capacity is the next prime after doubling current capacity.
        All _DELETED tombstones are dropped - they are not reinserted.
        All existing keys are reinserted using new capacity.

        Called automatically by add when load factor is exceedes 0.7.

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
            self.add(slot)

    # -------------------------------------------------------------------------
    # Core operations

    def add(self, key: Any) -> None:
        """
        Adds key to the set.

        If key is exists - does nothing.
        if key does not exist - places key at the probed slot.
        Triggers _resize if load favtor is exceeds 0.7 before insert.

        Time complexity: O(1) amortized

        Raises:
            TypeError: if key is not hashable.
        """
        if self._load_factor() >= _MAX_LOAD_FACTOR:
            self._resize()

        index, found = self._probe(key)

        if found:
            return

        self._buckets[index] = key
        self._size += 1

    def remove(self, key: Any) -> None:
        """
        Removes key from the set.

        Places a _DELETED tombstone at the slot so that probe sequences
        through this slot remain intact for future lookups.
        If key not found - does nothing.

        Tombstones are cleaned up automatically on the next _resize.

        Time complexity: O(1) avarage
        """
        index, found = self._probe(key)
        if not found:
            return
        self._buckets[index] = self._DELETED
        self._size -= 1

    def contains(self, key: Any) -> bool:
        """
        Returns True if key exists in the set.

        Time complexity: O(1) avarage
        """
        _, found = self._probe(key)
        return found

    # -------------------------------------------------------------------------
    # Collection methods

    def clear(self) -> None:
        """
        Removes all keys and resets to initial capacity.

        Time complexity: O(1)
        """
        self._capacity = _INITIAL_CAPACITY
        self._size = 0
        self._buckets = StaticUniversalArray(capacity=self._capacity)

    def copy(self) -> "OpenAddressingHashSet":
        """
        Returns a shallow copy - structure is new but keys are shared.

        Keys are always immutable (hashable), so shallow == deep here.

        Time complexity: O(n)
        """
        new_set = OpenAddressingHashSet()
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
            slot = self._buckets[i]
            if slot is None or slot is self._DELETED:
                continue
            yield slot

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields all keys in reverse bucket order.

        Time complexity: O(n)
        """
        for i in range(self._capacity - 1, -1, -1):
            slot = self._buckets[i]
            if slot is None or slot is self._DELETED:
                continue
            yield slot

    def __contains__(self, key: Any) -> bool:
        """Returns True if key is exists in the set. O(1) avarage"""
        return self.contains(key)

    def __delitem__(self, key: Any) -> None:
        """
        Removes key from the set.
        Format: set["name"]

        If key does not exist - does nothing.

        Time complexity: O(1) avarage
        """
        self.remove(key)

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both sets contain exactly the same keys.

        Order and initial layout do not matter.

        Time complexity: O(n)
        """
        if not isinstance(other, OpenAddressingHashSet):
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
        Format: OpenAddressingHashMap(size=2){"name", "age", 25}

        Time complexity: O(n)
        """
        keys = ", ".join(repr(key) for key in self)
        return f"OpenAddressingHashMap(size={self._size}" + "{" + keys + "}"
