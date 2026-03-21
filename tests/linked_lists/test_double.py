import pytest

from data_structures.linked_lists import DoublyLinkedList


@pytest.fixture
def empty_dll() -> DoublyLinkedList:
    return DoublyLinkedList()


@pytest.fixture
def filled_dll() -> DoublyLinkedList:
    return DoublyLinkedList(1, 2, 3, 4, 5, 6, 7, 8)


# --------------- Creation Tests -------------
def test_empty_creation(empty_dll) -> None:
    assert len(empty_dll) == 0
    assert empty_dll._head is None
    assert empty_dll._tail is None


def test_creation_with_args(filled_dll) -> None:
    assert len(filled_dll) == 8
    assert filled_dll.get_node(0).value == 1
    assert filled_dll.get_node(4).value == 5
    assert filled_dll.get_node(-1).value == 8


def test_creation_head_tail(filled_dll) -> None:
    assert filled_dll._head.value == 1
    assert filled_dll._tail.value == 8
    assert filled_dll._tail.next is None
    assert filled_dll._head.prev is None


# --------------- Append Tests -------------
def test_empty_dll_append(empty_dll) -> None:
    empty_dll.append("Back")
    assert empty_dll._tail.value == "Back"
    assert empty_dll._head is empty_dll._tail


def test_filled_dll_append(filled_dll) -> None:
    filled_dll.append("Back")
    assert filled_dll._tail.value == "Back"
    assert filled_dll._tail.prev.value == 8
    assert len(filled_dll) == 9
    assert filled_dll._tail.next is None


def test_append_updates_tail(empty_dll) -> None:
    empty_dll.append(1)
    empty_dll.append(2)
    empty_dll.append(3)
    assert empty_dll._tail.value == 3
    assert empty_dll._tail.prev.value == 2
    assert empty_dll._tail.prev.prev is empty_dll._head


# ------------ Prepend Tests ------------
def test_empty_dll(empty_dll) -> None:
    empty_dll.prepend("Head")
    assert empty_dll._head.value == "Head"
    assert empty_dll._head is empty_dll._tail


def test_filled_dll_prepend(filled_dll) -> None:
    filled_dll.prepend("Head")
    assert filled_dll._head.value == "Head"
    assert len(filled_dll) == 9
    assert filled_dll._head.next.value == 1
    assert filled_dll._head.next.prev is filled_dll._head


# -------------- Insert Tests -------------
def test_insert_at_zero(filled_dll) -> None:
    filled_dll.insert(0, 99)
    assert filled_dll._head.value == 99
    assert filled_dll._head.next.value == 1
    assert len(filled_dll) == 9


def test_insert_at_end(filled_dll) -> None:
    filled_dll.insert(len(filled_dll), 99)
    assert filled_dll._tail.value == 99
    assert filled_dll._tail.prev.value == 8
    assert filled_dll._tail.prev.next.value == 99


def test_insert_in_middle(filled_dll) -> None:
    filled_dll.insert(3, 99)
    assert filled_dll.get_node(3).value == 99
    assert filled_dll.get_node(4).value == 4
    assert filled_dll.get_node(3).next is filled_dll.get_node(4)
    assert filled_dll.get_node(4).prev is filled_dll.get_node(3)


def test_insert_out_of_range(filled_dll) -> None:
    with pytest.raises(IndexError):
        filled_dll.insert(99, 0)


def test_insert_wront_type(filled_dll) -> None:
    with pytest.raises(TypeError):
        filled_dll.insert("a", 0)


# ------------- set_node Tests -------------
def test_set_node(filled_dll) -> None:
    filled_dll.set_node(0, 99)
    assert filled_dll.get_node(0).value == 99


def test_set_node_at_size(filled_dll) -> None:
    filled_dll.set_node(len(filled_dll), 99)
    assert filled_dll._tail.value == 99
    assert len(filled_dll) == 9


def test_set_node_negaitive(filled_dll) -> None:
    filled_dll.set_node(-1, 99)
    assert filled_dll._tail.value == 99


# -------------- remove_head Tests -------------
def test_remove_head(filled_dll) -> None:
    value = filled_dll.remove_head()
    assert value == 1
    assert filled_dll._head.value == 2
    assert filled_dll._head.prev is None
    assert len(filled_dll) == 7


def test_remove_head_singe_element(empty_dll) -> None:
    empty_dll.append(1)
    value = empty_dll.remove_head()
    assert value == 1
    assert empty_dll._head is None and empty_dll._tail is None
    assert len(empty_dll) == 0


def test_remove_head_empty(empty_dll) -> None:
    with pytest.raises(IndexError):
        empty_dll.remove_head()


# ---------------- remove_tail Tests --------------
def test_remove_tail(filled_dll) -> None:
    value = filled_dll.remove_tail()
    assert value == 8
    assert filled_dll._tail.value == 7
    assert filled_dll._tail.next is None
    assert len(filled_dll) == 7


def test_remove_tail_singe_element(empty_dll) -> None:
    empty_dll.append(1)
    value = empty_dll.remove_tail()
    assert value == 1
    assert empty_dll._head is None and empty_dll._tail is None
    assert len(empty_dll) == 0


def test_remove_tail_empty(empty_dll) -> None:
    with pytest.raises(IndexError):
        empty_dll.remove_tail()


# -------------- remove Tests ---------------
def test_remove_middle(filled_dll) -> None:
    value = filled_dll.remove(3)
    assert value == 4
    assert filled_dll.get_node(3).value == 5
    assert len(filled_dll) == 7


def test_remove_at_zero(filled_dll) -> None:
    value = filled_dll.remove(0)
    assert value == 1
    assert filled_dll._head.value == 2
    assert filled_dll._head.prev is None


def test_remove_at_last(filled_dll) -> None:
    value = filled_dll.remove(-1)
    assert value == 8
    assert filled_dll._tail.value == 7
    assert filled_dll._tail.next is None
    assert len(filled_dll) == 7


def test_remove_out_of_range(empty_dll) -> None:
    with pytest.raises(IndexError):
        empty_dll.remove(99)


# ----------------- find Tests --------------
def test_find_existing(filled_dll) -> None:
    assert filled_dll.find(1) == 0
    assert filled_dll.find(8) == 7
    assert filled_dll.find(5) == 4


def test_find_not_existing(filled_dll) -> None:
    assert filled_dll.find(99) == -1


def test_find_empty(empty_dll) -> None:
    assert empty_dll.find(1) == -1


# --------------- __iter__ Tests ---------------
def test_iter(filled_dll) -> None:
    values = list(filled_dll)
    assert values == [1, 2, 3, 4, 5, 6, 7, 8]


def test_iter_empty(empty_dll) -> None:
    assert list(empty_dll) == []


# --------------- __contains__ Tests ----------------
def test_contains_existing(filled_dll) -> None:
    assert 1 in filled_dll
    assert 8 in filled_dll


def test_contains_not_existing(filled_dll) -> None:
    assert 99 not in filled_dll


# --------------- __len__ Tests ----------------
def test_len_empty(empty_dll) -> None:
    assert len(empty_dll) == 0


def test_len_after_operations(empty_dll) -> None:
    empty_dll.append(1)
    empty_dll.append(2)
    empty_dll.prepend(0)
    assert len(empty_dll) == 3
    empty_dll.remove_head()
    assert len(empty_dll) == 2


# --------------- __repr__ Tests ----------------
def test_repr_empty(empty_dll) -> None:
    assert repr(empty_dll) == "DoublyLinkedList([None -><- None])"


def test_repr_filled(filled_dll) -> None:
    assert (
        repr(filled_dll)
        == "DoublyLinkedList([None -><- 1 -><- 2 -><- 3 -><- 4 -><- 5 -><- 6 -><- 7 -><- 8 -><- None])"
    )
