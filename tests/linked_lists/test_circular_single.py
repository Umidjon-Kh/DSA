import pytest

from data_structures.linked_lists import CircularSinglyLinkedList


# -------------- Fixtures ---------------
@pytest.fixture
def empty_csl() -> CircularSinglyLinkedList:
    return CircularSinglyLinkedList()


@pytest.fixture
def filled_csl() -> CircularSinglyLinkedList:
    return CircularSinglyLinkedList(1, 2, 3, 4, 5, 6, 7, 8)


# --------------- Creation Tests -------------
def test_empty_creation(empty_csl) -> None:
    assert len(empty_csl) == 0
    assert empty_csl._head is None
    assert empty_csl._tail is None


def test_creation_with_args(filled_csl) -> None:
    assert len(filled_csl) == 8
    assert filled_csl.get_node(0).value == 1
    assert filled_csl.get_node(4).value == 5
    assert filled_csl.get_node(-1).value == 8


def test_creation_head_tail(filled_csl) -> None:
    assert filled_csl._head.value == 1
    assert filled_csl._tail.value == 8
    assert filled_csl._tail.next is filled_csl._head


# ------------- Append Tests -------------
def test_empty_csl_append(empty_csl) -> None:
    empty_csl.append("Back")
    assert empty_csl._head.value == "Back"
    assert empty_csl._tail.value == "Back"
    assert empty_csl._tail is empty_csl._head


def test_filled_csl_append(filled_csl) -> None:
    filled_csl.append("Back")
    assert filled_csl._tail.value == "Back"
    assert len(filled_csl) == 9
    assert filled_csl._tail.next is filled_csl._head


# ------------- Prepend Tests --------------
def test_empty_csl_prepend(empty_csl) -> None:
    empty_csl.prepend("Head")
    assert empty_csl._head.value == "Head"
    assert empty_csl._head is empty_csl._tail
    assert empty_csl._tail.next is empty_csl._head


def test_filled_csl_prepend(filled_csl) -> None:
    filled_csl.prepend("Head")
    assert filled_csl._head.value == "Head"
    assert len(filled_csl) == 9
    assert filled_csl._tail.next.value == "Head"


# ------------- Insert Tests --------------
def test_insert_at_zero(filled_csl) -> None:
    filled_csl.insert(0, 99)
    assert filled_csl._head.value == 99
    assert len(filled_csl) == 9


def test_insert_at_end(filled_csl) -> None:
    filled_csl.insert(len(filled_csl), 99)
    assert filled_csl._tail.value == 99
    assert len(filled_csl) == 9


def test_insert_in_middle(filled_csl) -> None:
    filled_csl.insert(3, 99)
    assert filled_csl.get_node(3).value == 99
    assert filled_csl.get_node(4).value == 4
    assert filled_csl.get_node(3).next.value == 4
    assert len(filled_csl) == 9


def test_insert_out_of_range(filled_csl) -> None:
    with pytest.raises(IndexError):
        filled_csl.insert(99, 0)


def test_insert_wrong_type(filled_csl) -> None:
    with pytest.raises(TypeError):
        filled_csl.insert("a", 0)


# --------------- set_node Tests ----------------
def test_set_node(filled_csl) -> None:
    filled_csl.set_node(0, 99)
    assert filled_csl.get_node(0).value == 99


def test_set_node_at_size(filled_csl) -> None:
    filled_csl.set_node(len(filled_csl), 99)
    assert filled_csl._tail.value == 99
    assert len(filled_csl) == 9
    assert filled_csl._tail.next is filled_csl._head


def test_set_node_negative(filled_csl) -> None:
    filled_csl.set_node(-1, 99)
    assert filled_csl._tail.value == 99


# --------------- remove_head Tests ----------------
def test_remove_head(filled_csl) -> None:
    value = filled_csl.remove_head()
    assert value == 1
    assert filled_csl._head.value == 2
    assert filled_csl._tail.next.value == 2
    assert len(filled_csl) == 7


def test_remove_head_single_element(empty_csl) -> None:
    empty_csl.append(1)
    value = empty_csl.remove_head()
    assert value == 1
    assert empty_csl._head is None
    assert empty_csl._tail is None
    assert len(empty_csl) == 0


def test_remove_head_empty(empty_csl) -> None:
    with pytest.raises(IndexError):
        empty_csl.remove_head()


# --------------- remove_tail Tests ----------------
def test_remove_tail(filled_csl) -> None:
    value = filled_csl.remove_tail()
    assert value == 8
    assert filled_csl._tail.value == 7
    assert filled_csl._tail.next is filled_csl._head
    assert len(filled_csl) == 7


def test_remove_tail_single_element(empty_csl) -> None:
    empty_csl.append(1)
    value = empty_csl.remove_tail()
    assert value == 1
    assert empty_csl._head is None
    assert empty_csl._tail is None
    assert len(empty_csl) == 0


def test_remove_tail_empty(empty_csl) -> None:
    with pytest.raises(IndexError):
        empty_csl.remove_tail()


# --------------- remove Tests ----------------
def test_remove_middle(filled_csl) -> None:
    value = filled_csl.remove(3)
    assert value == 4
    assert filled_csl.get_node(3).value == 5
    assert len(filled_csl) == 7


def test_remove_at_zero(filled_csl) -> None:
    value = filled_csl.remove(0)
    assert value == 1
    assert filled_csl._head.value == 2


def test_remove_at_last(filled_csl) -> None:
    value = filled_csl.remove(len(filled_csl) - 1)
    assert value == 8
    assert filled_csl._tail.value == 7


def test_remove_negative(filled_csl) -> None:
    value = filled_csl.remove(-1)
    assert value == 8


def test_remove_out_of_range(filled_csl) -> None:
    with pytest.raises(IndexError):
        filled_csl.remove(99)


# --------------- find Tests ----------------
def test_find_existing(filled_csl) -> None:
    assert filled_csl.find(1) == 0
    assert filled_csl.find(8) == 7
    assert filled_csl.find(5) == 4


def test_find_not_existing(filled_csl) -> None:
    assert filled_csl.find(99) == -1


def test_find_empty(empty_csl) -> None:
    assert empty_csl.find(1) == -1


# --------------- __iter__ Tests ----------------
def test_iter(filled_csl) -> None:
    values = list(filled_csl)
    assert values == [1, 2, 3, 4, 5, 6, 7, 8]


def test_iter_empty(empty_csl) -> None:
    assert list(empty_csl) == []


# --------------- __contains__ Tests ----------------
def test_contains_existing(filled_csl) -> None:
    assert 1 in filled_csl
    assert 8 in filled_csl


def test_contains_not_existing(filled_csl) -> None:
    assert 99 not in filled_csl


# --------------- __len__ Tests ----------------
def test_len_empty(empty_csl) -> None:
    assert len(empty_csl) == 0


def test_len_after_operations(empty_csl) -> None:
    empty_csl.append(1)
    empty_csl.append(2)
    empty_csl.prepend(0)
    assert len(empty_csl) == 3
    empty_csl.remove_head()
    assert len(empty_csl) == 2


# --------------- __repr__ Tests ----------------
def test_repr_empty(empty_csl) -> None:
    assert repr(empty_csl) == "CircularSinglyLinkedList([(back to head)])"


def test_repr_filled(filled_csl) -> None:
    assert (
        repr(filled_csl)
        == "CircularSinglyLinkedList([1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> (back to head)])"
    )
