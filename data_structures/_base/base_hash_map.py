from abc import abstractmethod
from typing import Any, Iterator

from .base_collection import BaseCollection


class BaseHashMap(BaseCollection):
    """
    Abstract base class for all hash map implementations.

    Defines the shared interface for key-value storage structures
    backed by a hash table. Supports chaining and open addressing
    collision resolution strategies.

    For every node, all values in the left subtree are smaller and
    all values in the right subtree are larger.

    Subclasses:
        ChainingHashMap      — collision resolution via linked buckets
        OpenAddressingHashMap — collision resolution via probing

    Required to implement (in addition to BaseCollection):
        insert, get, delete, contains, setdefault,
        keys, values, items, resize,
        _hash, _load_factor
    """

    __slots__ = ()

    @abstractmethod
    def insert(self, key: Any, value: Any) -> None:
        """
        Inserts or updates a key-value pair in the map.

        If key already exists — updates its value.
        If key does not exist — inserts new pair.
        Triggers resize if load factor exceeds threshold.

        Time complexity: O(1) amortized

        Raises:
            TypeError: If key is not hashable.
        """
        ...

    @abstractmethod
    def get(self, key: Any, default: Any = None) -> Any:
        """
        Returns the value associated with key.

        If key does not exist — returns default.

        Time complexity: O(1) average

        Args:
            key:     The key to look up.
            default: Value to return if key not found. Defaults to None.
        """
        ...

    @abstractmethod
    def delete(self, key: Any) -> None:
        """
        Removes the key-value pair with given key.

        If key does not exist — does nothing.

        Time complexity: O(1) average
        """
        ...

    @abstractmethod
    def contains(self, key: Any) -> bool:
        """
        Returns True if key exists in the map.

        Time complexity: O(1) average
        """
        ...

    @abstractmethod
    def setdefault(self, key: Any, default: Any = None) -> Any:
        """
        Returns value for key if it exists.
        If key does not exist — inserts (key, default) and returns default.

        Time complexity: O(1) average

        Args:
            key:     The key to look up or insert.
            default: Value to insert and return if key not found.
        """
        ...

    @abstractmethod
    def keys(self) -> Iterator[Any]:
        """
        Yields all keys in bucket order.

        Time complexity: O(n)
        """
        ...

    @abstractmethod
    def values(self) -> Iterator[Any]:
        """
        Yields all values in bucket order.

        Time complexity: O(n)
        """
        ...

    @abstractmethod
    def items(self) -> Iterator[tuple]:
        """
        Yields all (key, value) pairs in bucket order.

        Time complexity: O(n)
        """
        ...

    @abstractmethod
    def _resize(self) -> None:
        """
        Grows the internal bucket array and rehashes all existing pairs.

        Called automatically when load factor exceeds threshold (0.7).
        New capacity is the next prime number after doubling current size.
        All existing pairs are reinserted using the new capacity.

        Time complexity: O(n)
        """
        ...

    @abstractmethod
    def __getitem__(self, key: Any) -> Any:
        """
        Returns value for key.
        Format: map["name"]
        """
        ...

    @abstractmethod
    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Inserts or updates key-value pair.
        Format: map["name"] = "Umidjon"
        """
        ...

    @abstractmethod
    def __delitem__(self, key: Any) -> None:
        """
        Removes item by received key from map.
        Format: del map["key"]
        """
        ...

    @abstractmethod
    def _hash(self, key: Any) -> int:
        """
        Computes the bucket index for given key.

        Uses a custom polynomial rolling hash for strings and
        falls back to Python's built-in hash() for other types.
        Result is always in range [0, capacity).

        Time complexity: O(k) where k is the length of the key
        """
        ...

    @abstractmethod
    def _load_factor(self) -> float:
        """
        Returns the current load factor of the map.

        load_factor = number of elements / number of buckets

        Used internally to decide when to trigger resize.

        Time complexity: O(1)
        """
        ...


class BaseHashSet(BaseCollection):
    """
    Abstract base class for all hash set implementations.

    Defines the shared interface for key-only storage structures
    backed by a hash table. A hash set is like a hash map but stores
    only keys — no associated values.

    Subclasses:
        ChainingHashSet       — collision resolution via linked buckets
        OpenAddressingHashSet — collision resolution via probing

    Required to implement (in addition to BaseCollection):
        add, remove, contains, resize,
        _hash, _load_factor
    """

    __slots__ = ()

    @abstractmethod
    def add(self, key: Any) -> None:
        """
        Adds key to the set.

        If key already exists — does nothing.
        Triggers resize if load factor exceeds threshold.

        Time complexity: O(1) amortized

        Raises:
            TypeError: If key is not hashable.
        """
        ...

    @abstractmethod
    def remove(self, key: Any) -> None:
        """
        Removes key from the set.

        If key does not exist — does nothing.

        Time complexity: O(1) average
        """
        ...

    @abstractmethod
    def contains(self, key: Any) -> bool:
        """
        Returns True if key exists in the set.

        Time complexity: O(1) average
        """
        ...

    @abstractmethod
    def _resize(self) -> None:
        """
        Grows the internal bucket array and rehashes all existing keys.

        Called automatically when load factor exceeds threshold (0.7).
        New capacity is the next prime number after doubling current size.
        All existing keys are reinserted using the new capacity.

        Time complexity: O(n)
        """
        ...

    @abstractmethod
    def _hash(self, key: Any) -> int:
        """
        Computes the bucket index for given key.

        Time complexity: O(k) where k is the length of the key
        """
        ...

    @abstractmethod
    def _load_factor(self) -> float:
        """
        Returns the current load factor of the set.

        load_factor = number of elements / number of buckets

        Time complexity: O(1)
        """
        ...

    @abstractmethod
    def __delitem__(self, key: Any) -> None:
        """
        Removes item by received key from map.
        Format: del map["key"]
        """
        ...
