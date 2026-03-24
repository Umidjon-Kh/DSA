from abc import abstractmethod
from typing import Any

from .base_collection import BaseCollection


class BaseHashTable(BaseCollection):
    """
    Abstract base class for all hash table types.

    Defines the shared interface for chaining and open addressing implementations.
    Iteration yields all keys stored in the table.
    __contains__ checks for key existence.

    Required to implement (in addition to BaseCollection):
        put, get, delete, contains_key, __getitem__, __setitem__
    """

    @abstractmethod
    def put(self, key: Any, value: Any) -> None:
        """
        Inserts or updates the key-value pair in the table.
        If key already exists, its value is overwritten.

        Raises:
            TypeError: If key is not hashable.
        """
        ...

    @abstractmethod
    def get(self, key: Any) -> Any:
        """
        Returns the value associated with given key.

        Raises:
            TypeError: If key is not hashable.
            KeyError:  If key does not exist in the table.
        """
        ...

    @abstractmethod
    def delete(self, key: Any) -> None:
        """
        Removes the key-value pair with given key from the table.

        Raises:
            TypeError: If key is not hashable.
            KeyError:  If key does not exist in the table.
        """
        ...

    @abstractmethod
    def contains_key(self, key: Any) -> bool:
        """
        Returns True if key exists in the table.

        Raises:
            TypeError: If key is not hashable.
        """
        ...

    @abstractmethod
    def __getitem__(self, key: Any) -> Any:
        """
        Returns the value associated with given key. Alias for get().

        Raises:
            TypeError: If key is not hashable.
            KeyError:  If key does not exist in the table.
        """
        ...

    @abstractmethod
    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Inserts or updates the key-value pair. Alias for put().

        Raises:
            TypeError: If key is not hashable.
        """
        ...
