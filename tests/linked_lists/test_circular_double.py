import pytest

from data_structures.linked_lists import CircularDoublyLinkedList


# -------------- Fixtures ---------------
@pytest.fixture
def empty_cdl() -> CircularDoublyLinkedList:
    return CircularDoublyLinkedList()


@pytest.fixture
def filled_cdl() -> CircularDoublyLinkedList:
    return CircularDoublyLinkedList(1, 2, 3, 4, 5, 6, 7, 8)


# --------------- Creation Tests -------------
def test_empty_creation(empty_cdl) -> None:
    assert len(empty_cdl) == 0
    assert empty_cdl._head is None
    assert empty_cdl._tail is None


def test_creation_with_args(filled_cdl) -> None:
    assert len(filled_cdl) == 8
    assert filled_cdl.get_node(0).value == 1
    assert filled_cdl.get_node(4).value == 5
    assert filled_cdl.get_node(7).value == 8


def test_creation_circular_links(filled_cdl) -> None:
    assert filled_cdl._tail.next is filled_cdl._head
    assert filled_cdl._head.prev is filled_cdl._tail
    assert filled_cdl._head.value == 1
    assert filled_cdl._tail.value == 8


# ------------- Append Tests -------------
def test_empty_cdl_append(empty_cdl) -> None:
    empty_cdl.append("Back")
    assert empty_cdl._head.value == "Back"
    assert empty_cdl._tail is empty_cdl._head
    assert empty_cdl._tail.next is empty_cdl._head
    assert empty_cdl._head.prev is empty_cdl._tail


def test_filled_cdl_append(filled_cdl) -> None:
    filled_cdl.append("Back")
    assert filled_cdl._tail.value == "Back"
    assert len(filled_cdl) == 9
    assert filled_cdl._tail.next is filled_cdl._head
    assert filled_cdl._head.prev is filled_cdl._tail
    assert filled_cdl._tail.prev.value == 8


def test_append_updates_links(empty_cdl) -> None:
    empty_cdl.append(1)
    empty_cdl.append(2)
    empty_cdl.append(3)
    assert empty_cdl._tail.value == 3
    assert empty_cdl._head.value == 1
    assert empty_cdl._tail.next is empty_cdl._head
    assert empty_cdl._head.prev is empty_cdl._tail


# ------------- Prepend Tests --------------
def test_empty_cdl_prepend(empty_cdl) -> None:
    empty_cdl.prepend("Head")
    assert empty_cdl._head.value == "Head"
    assert empty_cdl._head is empty_cdl._tail
    assert empty_cdl._tail.next is empty_cdl._head
    assert empty_cdl._head.prev is empty_cdl._tail


def test_filled_cdl_prepend(filled_cdl) -> None:
    filled_cdl.prepend("Head")
    assert filled_cdl._head.value == "Head"
    assert len(filled_cdl) == 9
    assert filled_cdl._tail.next is filled_cdl._head
    assert filled_cdl._head.prev is filled_cdl._tail
    assert filled_cdl._head.next.value == 1
    assert filled_cdl._head.next.prev is filled_cdl._head


# ------------- Insert Tests --------------
def test_insert_at_zero(filled_cdl) -> None:
    filled_cdl.insert(0, 99)
    assert filled_cdl._head.value == 99
    assert filled_cdl._head.next.value == 1
    assert filled_cdl._head.next.prev is filled_cdl._head
    assert len(filled_cdl) == 9


def test_insert_at_end(filled_cdl) -> None:
    filled_cdl.insert(len(filled_cdl), 99)
    assert filled_cdl._tail.value == 99
    assert filled_cdl._tail.prev.value == 8
    assert filled_cdl._tail.next is filled_cdl._head
    assert len(filled_cdl) == 9


def test_insert_in_middle(filled_cdl) -> None:
    filled_cdl.insert(3, 99)
    assert filled_cdl.get_node(3).value == 99
    assert filled_cdl.get_node(4).value == 4
    assert filled_cdl.get_node(3).next is filled_cdl.get_node(4)
    assert filled_cdl.get_node(4).prev is filled_cdl.get_node(3)
    assert len(filled_cdl) == 9


def test_insert_out_of_range(filled_cdl) -> None:
    with pytest.raises(IndexError):
        filled_cdl.insert(99, 0)


def test_insert_wrong_type(filled_cdl) -> None:
    with pytest.raises(TypeError):
        filled_cdl.insert("a", 0)


# --------------- get_node Tests ----------------
def test_get_node(filled_cdl) -> None:
    assert filled_cdl.get_node(0).value == 1
    assert filled_cdl.get_node(7).value == 8


def test_get_node_negative(filled_cdl) -> None:
    assert filled_cdl.get_node(-1).value == 8
    assert filled_cdl.get_node(-8).value == 1


def test_get_node_out_of_range(filled_cdl) -> None:
    with pytest.raises(IndexError):
        filled_cdl.get_node(99)


def test_get_node_wrong_type(filled_cdl) -> None:
    with pytest.raises(TypeError):
        filled_cdl.get_node("a")


# --------------- set_node Tests ----------------
def test_set_node(filled_cdl) -> None:
    filled_cdl.set_node(0, 99)
    assert filled_cdl.get_node(0).value == 99


def test_set_node_at_size(filled_cdl) -> None:
    filled_cdl.set_node(len(filled_cdl), 99)
    assert filled_cdl._tail.value == 99
    assert len(filled_cdl) == 9
    assert filled_cdl._tail.next is filled_cdl._head
    assert filled_cdl._head.prev is filled_cdl._tail


def test_set_node_negative(filled_cdl) -> None:
    filled_cdl.set_node(-1, 99)
    assert filled_cdl._tail.value == 99


# --------------- remove_head Tests ----------------
def test_remove_head(filled_cdl) -> None:
    value = filled_cdl.remove_head()
    assert value == 1
    assert filled_cdl._head.value == 2
    assert filled_cdl._head.prev is filled_cdl._tail
    assert filled_cdl._tail.next is filled_cdl._head
    assert len(filled_cdl) == 7


def test_remove_head_single_element(empty_cdl) -> None:
    empty_cdl.append(1)
    value = empty_cdl.remove_head()
    assert value == 1
    assert empty_cdl._head is None
    assert empty_cdl._tail is None
    assert len(empty_cdl) == 0


def test_remove_head_empty(empty_cdl) -> None:
    with pytest.raises(IndexError):
        empty_cdl.remove_head()


# --------------- remove_tail Tests ----------------
def test_remove_tail(filled_cdl) -> None:
    value = filled_cdl.remove_tail()
    assert value == 8
    assert filled_cdl._tail.value == 7
    assert filled_cdl._tail.next is filled_cdl._head
    assert filled_cdl._head.prev is filled_cdl._tail
    assert len(filled_cdl) == 7


def test_remove_tail_single_element(empty_cdl) -> None:
    empty_cdl.append(1)
    value = empty_cdl.remove_tail()
    assert value == 1
    assert empty_cdl._head is None
    assert empty_cdl._tail is None
    assert len(empty_cdl) == 0


def test_remove_tail_empty(empty_cdl) -> None:
    with pytest.raises(IndexError):
        empty_cdl.remove_tail()


# --------------- remove Tests ----------------
def test_remove_middle(filled_cdl) -> None:
    value = filled_cdl.remove(3)
    assert value == 4
    assert filled_cdl.get_node(3).value == 5
    assert filled_cdl.get_node(2).next is filled_cdl.get_node(3)
    assert filled_cdl.get_node(3).prev is filled_cdl.get_node(2)
    assert len(filled_cdl) == 7


def test_remove_at_zero(filled_cdl) -> None:
    value = filled_cdl.remove(0)
    assert value == 1
    assert filled_cdl._head.value == 2
    assert filled_cdl._head.prev is filled_cdl._tail


def test_remove_at_last(filled_cdl) -> None:
    value = filled_cdl.remove(-1)
    assert value == 8
    assert filled_cdl._tail.value == 7
    assert filled_cdl._tail.next is filled_cdl._head


def test_remove_out_of_range(filled_cdl) -> None:
    with pytest.raises(IndexError):
        filled_cdl.remove(99)


# --------------- find Tests ----------------
def test_find_existing(filled_cdl) -> None:
    assert filled_cdl.find(1) == 0
    assert filled_cdl.find(8) == 7
    assert filled_cdl.find(5) == 4


def test_find_not_existing(filled_cdl) -> None:
    assert filled_cdl.find(99) == -1


def test_find_empty(empty_cdl) -> None:
    assert empty_cdl.find(1) == -1


# --------------- __iter__ Tests ----------------
def test_iter(filled_cdl) -> None:
    values = list(filled_cdl)
    assert values == [1, 2, 3, 4, 5, 6, 7, 8]


def test_iter_empty(empty_cdl) -> None:
    assert list(empty_cdl) == []


# --------------- __reversed__ Tests ----------------
def test_reversed(filled_cdl) -> None:
    values = list(reversed(filled_cdl))
    assert values == [8, 7, 6, 5, 4, 3, 2, 1]


def test_reversed_empty(empty_cdl) -> None:
    assert list(reversed(empty_cdl)) == []


def test_reversed_single(empty_cdl) -> None:
    empty_cdl.append(42)
    assert list(reversed(empty_cdl)) == [42]


# --------------- __contains__ Tests ----------------
def test_contains_existing(filled_cdl) -> None:
    assert 1 in filled_cdl
    assert 8 in filled_cdl


def test_contains_not_existing(filled_cdl) -> None:
    assert 99 not in filled_cdl


# --------------- __len__ Tests ----------------
def test_len_empty(empty_cdl) -> None:
    assert len(empty_cdl) == 0


def test_len_after_operations(empty_cdl) -> None:
    empty_cdl.append(1)
    empty_cdl.append(2)
    empty_cdl.prepend(0)
    assert len(empty_cdl) == 3
    empty_cdl.remove_head()
    assert len(empty_cdl) == 2


# --------------- __repr__ Tests ----------------
def test_repr_empty(empty_cdl) -> None:
    assert (
        repr(empty_cdl)
        == "CircularDoublyLinkedList([(points to tail) -><- (back to head)])"
    )


def test_repr_filled(filled_cdl) -> None:
    assert (
        repr(filled_cdl)
        == "CircularDoublyLinkedList([(points to tail) -><- 1 -><- 2 -><- 3 -><- 4 -><- 5 -><- 6 -><- 7 -><- 8 -><- (back to head)])"
    )
