from abc import ABC, abstractmethod
from typing import Any


class BaseNode(ABC):
    """
    Abstract base class for all node types.

    A node is the fundamental building block of linked data structures.
    It stores a single value and maintains references to neighboring nodes.

    Subclasses define which neighbor references they hold:
        LinearNode   — next
        BiLinearNode — prev, next
        TreeNode     — left, right, parent

    All subclasses must use __slots__ and implement __repr__.

    Time complexity:
        __init__: O(1)
        __repr__: O(1)
    """

    __slots__ = ("value",)

    def __init__(self, value: Any) -> None:
        """
        Stores given value in the node.

        Args:
            value: Any Python object to store.
        """
        self.value = value

    @abstractmethod
    def __repr__(self) -> str:
        """Returns a string representation of the node."""
        ...
