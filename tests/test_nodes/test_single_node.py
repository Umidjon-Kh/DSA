import pytest
from data_structures.nodes import SingleNode


def test_node_creation() -> None:
    node = SingleNode(42)
    assert node.value == 42
    assert node.next is None


def test_node_stores_any_type() -> None:
    assert SingleNode('hello').value == 'hello'
    assert SingleNode([1, 2, 3]).value == [1, 2, 3]
    assert SingleNode(None).value is None


def test_node_next_setter() -> None:
    node1 = SingleNode(1)
    node2 = SingleNode(2)
    node1.next = node2
    assert node1.next is node2
    assert node1.next.value == 2


def test_node_chain() -> None:
    node1 = SingleNode(1)
    node2 = SingleNode(2)
    node3 = SingleNode(3)
    node1.next = node2
    node2.next = node3
    assert node1.next.next.value == 3  # type: ignore


def test_node_next_reset_to_none() -> None:
    node1 = SingleNode(1)
    node2 = SingleNode(2)
    node1.next = node2
    node1.next = None
    assert node1.next is None


def test_node_value_is_readonly() -> None:
    node = SingleNode(1)
    with pytest.raises(AttributeError):
        node.value = 99  # type: ignore
