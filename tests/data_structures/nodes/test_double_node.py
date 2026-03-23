import pytest

from data_structures.nodes import DoubleNode


class TestDoubleNodeInit:
    def test_stores_integer_value(self):
        node = DoubleNode(42)
        assert node.value == 42

    def test_stores_string_value(self):
        node = DoubleNode("hello")
        assert node.value == "hello"

    def test_stores_none_value(self):
        node = DoubleNode(None)
        assert node.value is None

    def test_next_is_none_by_default(self):
        node = DoubleNode(1)
        assert node.next is None

    def test_prev_is_none_by_default(self):
        node = DoubleNode(1)
        assert node.prev is None


class TestDoubleNodeLinking:
    def test_link_next(self):
        a = DoubleNode(1)
        b = DoubleNode(2)
        a.next = b
        assert a.next is b

    def test_link_prev(self):
        a = DoubleNode(1)
        b = DoubleNode(2)
        b.prev = a
        assert b.prev is a

    def test_bidirectional_link(self):
        a = DoubleNode(1)
        b = DoubleNode(2)
        a.next = b
        b.prev = a
        assert a.next is b
        assert b.prev is a

    def test_chain_three_nodes(self):
        a = DoubleNode(1)
        b = DoubleNode(2)
        c = DoubleNode(3)
        a.next = b
        b.prev = a
        b.next = c
        c.prev = b
        assert a.next.next is c
        assert c.prev.prev is a

    def test_unlink_next(self):
        a = DoubleNode(1)
        b = DoubleNode(2)
        a.next = b
        a.next = None
        assert a.next is None

    def test_self_loop(self):
        a = DoubleNode(1)
        a.next = a
        a.prev = a
        assert a.next is a
        assert a.prev is a


class TestDoubleNodeRepr:
    def test_repr_no_links(self):
        node = DoubleNode(42)
        assert repr(node) == "None <-> DoubleNode(42) <-> None"

    def test_repr_with_next(self):
        a = DoubleNode(1)
        b = DoubleNode(2)
        a.next = b
        assert repr(a) == "None <-> DoubleNode(1) <-> 2"

    def test_repr_with_prev(self):
        a = DoubleNode(1)
        b = DoubleNode(2)
        b.prev = a
        assert repr(b) == "1 <-> DoubleNode(2) <-> None"

    def test_repr_with_both(self):
        a = DoubleNode(1)
        b = DoubleNode(2)
        c = DoubleNode(3)
        a.next = b
        b.prev = a
        b.next = c
        c.prev = b
        assert repr(b) == "1 <-> DoubleNode(2) <-> 3"

    def test_repr_string_value(self):
        node = DoubleNode("hi")
        assert repr(node) == "None <-> DoubleNode('hi') <-> None"
