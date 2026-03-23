import pytest

from data_structures.nodes import SingleNode


class TestSingleNodeInit:
    def test_stores_integer_value(self):
        node = SingleNode(42)
        assert node.value == 42

    def test_stores_string_value(self):
        node = SingleNode("hello")
        assert node.value == "hello"

    def test_stores_float_value(self):
        node = SingleNode(3.14)
        assert node.value == 3.14

    def test_stores_none_value(self):
        node = SingleNode(None)
        assert node.value is None

    def test_stores_list_value(self):
        node = SingleNode([1, 2, 3])
        assert node.value == [1, 2, 3]

    def test_next_is_none_by_default(self):
        node = SingleNode(1)
        assert node.next is None


class TestSingleNodeLinking:
    def test_link_two_nodes(self):
        a = SingleNode(1)
        b = SingleNode(2)
        a.next = b
        assert a.next is b

    def test_link_chain(self):
        a = SingleNode(1)
        b = SingleNode(2)
        c = SingleNode(3)
        a.next = b
        b.next = c
        assert a.next.next is c

    def test_next_value_accessible(self):
        a = SingleNode(10)
        b = SingleNode(20)
        a.next = b
        assert a.next.value == 20

    def test_unlink_node(self):
        a = SingleNode(1)
        b = SingleNode(2)
        a.next = b
        a.next = None
        assert a.next is None

    def test_self_loop(self):
        a = SingleNode(1)
        a.next = a
        assert a.next is a


class TestSingleNodeRepr:
    def test_repr_no_next(self):
        node = SingleNode(42)
        assert repr(node) == "SingleNode(42) -> None"

    def test_repr_with_next(self):
        a = SingleNode(42)
        b = SingleNode(10)
        a.next = b
        assert repr(a) == "SingleNode(42) -> 10"

    def test_repr_string_value(self):
        node = SingleNode("hi")
        assert repr(node) == "SingleNode('hi') -> None"

    def test_repr_none_value(self):
        node = SingleNode(None)
        assert repr(node) == "SingleNode(None) -> None"
