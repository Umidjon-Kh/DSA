from abc import abstractmethod
from typing import Any

from .base_collection import BaseCollection


class BaseQueue(BaseCollection):
    """
    Abstract base class for all queue types.

    Defines the FIFO (First In, First Out) interface.
    Simple, circular, and node-based queues inherit from this.

    Subclasses:
        BaseBoundedQueue  — adds capacity tracking and is_full check
        BaseDeque         — extends with front/back push and pop
        BasePriorityQueue — extends enqueue with a priority argument

    Required to implement (in addition to BaseCollection):
        enqueue, dequeue, peek, is_empty
    """

    @abstractmethod
    def enqueue(self, value: Any) -> None:
        """
        Adds value to the back of the queue.

        Raises:
            OverflowError: If the queue is full (bounded queues only).
            TypeError:     If value type does not match dtype (typed queues only).
        """
        ...

    @abstractmethod
    def dequeue(self) -> Any:
        """
        Removes and returns the front element.

        Raises:
            IndexError: If the queue is empty.
        """
        ...

    @abstractmethod
    def peek(self) -> Any:
        """
        Returns the front element without removing it.

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
    Used by static array-based circular queue implementations.

    Required to implement (in addition to BaseQueue):
        is_full, capacity (property)
    """

    @property
    @abstractmethod
    def capacity(self) -> int:
        """Returns the fixed maximum number of elements the queue can hold."""
        ...

    @abstractmethod
    def is_full(self) -> bool:
        """Returns True if size == capacity."""
        ...


class BaseDeque(BaseCollection):
    """
    Abstract base class for double-ended queues.

    Supports push and pop from both front and back.
    Does not inherit from BaseQueue — deques are not strictly FIFO.

    Subclass:
        BaseBoundedDeque — adds capacity tracking and is_full check

    Required to implement (in addition to BaseCollection):
        push_front, push_back, pop_front, pop_back, peek_front, peek_back, is_empty
    """

    @abstractmethod
    def push_front(self, value: Any) -> None:
        """
        Adds value to the front of the deque.

        Raises:
            OverflowError: If the deque is full (bounded deques only).
            TypeError:     If value type does not match dtype (typed deques only).
        """
        ...

    @abstractmethod
    def push_back(self, value: Any) -> None:
        """
        Adds value to the back of the deque.

        Raises:
            OverflowError: If the deque is full (bounded deques only).
            TypeError:     If value type does not match dtype (typed deques only).
        """
        ...

    @abstractmethod
    def pop_front(self) -> Any:
        """
        Removes and returns the front element.

        Raises:
            IndexError: If the deque is empty.
        """
        ...

    @abstractmethod
    def pop_back(self) -> Any:
        """
        Removes and returns the back element.

        Raises:
            IndexError: If the deque is empty.
        """
        ...

    @abstractmethod
    def peek_front(self) -> Any:
        """
        Returns the front element without removing it.

        Raises:
            IndexError: If the deque is empty.
        """
        ...

    @abstractmethod
    def peek_back(self) -> Any:
        """
        Returns the back element without removing it.

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
    Used by static array-based deque implementations.

    Required to implement (in addition to BaseDeque):
        is_full, capacity (property)
    """

    @property
    @abstractmethod
    def capacity(self) -> int:
        """Returns the fixed maximum number of elements the deque can hold."""
        ...

    @abstractmethod
    def is_full(self) -> bool:
        """Returns True if size == capacity."""
        ...


class BasePriorityQueue(BaseCollection):
    """
    Abstract base class for priority queues.

    Elements are dequeued in priority order, not insertion order.
    Does not inherit from BaseQueue — the enqueue signature differs.

    Required to implement (in addition to BaseCollection):
        enqueue, dequeue, peek, is_empty
    """

    @abstractmethod
    def enqueue(self, value: Any, priority: Any) -> None:
        """
        Adds value with given priority to the queue.

        Lower or higher priority wins depending on implementation
        (min-priority or max-priority queue).

        Raises:
            TypeError: If priority type is not comparable.
        """
        ...

    @abstractmethod
    def dequeue(self) -> Any:
        """
        Removes and returns the element with the highest priority.

        Raises:
            IndexError: If the queue is empty.
        """
        ...

    @abstractmethod
    def peek(self) -> Any:
        """
        Returns the highest-priority element without removing it.

        Raises:
            IndexError: If the queue is empty.
        """
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the queue contains no elements."""
        ...
