from abc import abstractmethod
from typing import Any

from .base_collection import BaseCollection


class BaseQueue(BaseCollection):
    """
    Abstract base class for all simple queue types.

    Defines the FIFO (First In, First Out) interface.
    Array-based (static and dynamic) and node-based queues
    inherit from this.

    Subclass:
        BaseBoundedQueue — adds capacity tracking and is_full check
                           for fixed-size queue implementations

    Required to implement (in addition to BaseCollection):
        enqueue, dequeue, peek, is_empty
    """

    __slots__ = ()

    @abstractmethod
    def enqueue(self, value: Any) -> None:
        """
        Adds value to the rear of the queue.

        Raises:
            OverflowError: If the queue is full (bounded queues only).
            TypeError:     If value type does not match dtype (typed queues only).
        """
        ...

    @abstractmethod
    def dequeue(self) -> Any:
        """
        Removes and returns the value from the front of the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        ...

    @abstractmethod
    def peek(self) -> Any:
        """
        Returns the front value without removing it.

        Raises:
            IndexError: If the queue is empty.
        """
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the queue contains no elements."""
        ...


class BaseBoundedQueue(BaseQueue):
    """
    Abstract base class for fixed-capacity queues.

    Extends BaseQueue with capacity tracking and a fullness check.
    Used by array-based static and circular queue implementations.

    Required to implement (in addition to BaseQueue):
        is_full
    """

    __slots__ = ()

    @abstractmethod
    def is_full(self) -> bool:
        """Returns True if size == capacity."""
        ...


class BaseDeque(BaseCollection):
    """
    Abstract base class for all deque types.

    Defines the double-ended interface — elements can be added and
    removed from both the front and the rear.
    Both array-based and node-based deques inherit from this.

    Subclass:
        BaseBoundedDeque — adds capacity tracking and is_full check
                           for fixed-size deque implementations

    Required to implement (in addition to BaseCollection):
        enqueue_front, enqueue_rear,
        dequeue_front, dequeue_rear,
        peek_front, peek_rear,
        is_empty
    """

    __slots__ = ()

    @abstractmethod
    def enqueue_front(self, value: Any) -> None:
        """
        Adds value to the front of the deque.

        Raises:
            OverflowError: If the deque is full (bounded deques only).
            TypeError:     If value type does not match dtype (typed deques only).
        """
        ...

    @abstractmethod
    def enqueue_rear(self, value: Any) -> None:
        """
        Adds value to the rear of the deque.

        Raises:
            OverflowError: If the deque is full (bounded deques only).
            TypeError:     If value type does not match dtype (typed deques only).
        """
        ...

    @abstractmethod
    def dequeue_front(self) -> Any:
        """
        Removes and returns the value from the front of the deque.

        Raises:
            IndexError: If the deque is empty.
        """
        ...

    @abstractmethod
    def dequeue_rear(self) -> Any:
        """
        Removes and returns the value from the rear of the deque.

        Raises:
            IndexError: If the deque is empty.
        """
        ...

    @abstractmethod
    def peek_front(self) -> Any:
        """
        Returns the front value without removing it.

        Raises:
            IndexError: If the deque is empty.
        """
        ...

    @abstractmethod
    def peek_rear(self) -> Any:
        """
        Returns the rear value without removing it.

        Raises:
            IndexError: If the deque is empty.
        """
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the deque contains no elements."""
        ...


class BaseBoundedDeque(BaseDeque):
    """
    Abstract base class for fixed-capacity deques.

    Extends BaseDeque with capacity tracking and a fullness check.
    Used by array-based static deque implementations.

    Required to implement (in addition to BaseDeque):
        is_full
    """

    __slots__ = ()

    @abstractmethod
    def is_full(self) -> bool:
        """Returns True if size == capacity."""
        ...
