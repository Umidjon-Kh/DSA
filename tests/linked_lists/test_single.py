import pytest

from data_structures.linked_lists import SinglyLinkedList


# ------------- Fixtures ------------------
@pytest.fixture
def empty_sll() -> SinglyLinkedList:
    return SinglyLinkedList()


@pytest.fixture
def filled_sll() -> SinglyLinkedList:
    return SinglyLinkedList(1, 2, 3, 4, 5, 6, 7, 8)


# -------------- Creation Tests ----------------
def test_empty_creation(empty_sll) -> None:
    assert len(empty_sll) == 0
    assert empty_sll._head is None
    assert empty_sll._tail is None


def test_creation_with_args(filled_sll) -> None:
    assert len(filled_sll) == 8
    assert filled_sll.get_node(0).value == 1
    assert filled_sll.get_node(4).value == 5
    assert filled_sll.get_node(-1).value == 8


def test_creation_head_tail(filled_sll) -> None:
    assert filled_sll._head.value == 1
    assert filled_sll._tail.value == 8
    assert filled_sll._tail.next is None


# ---------------- Append Tests --------------
def test_empty_sll_append(empty_sll) -> None:
    empty_sll.append("Back")
    assert empty_sll._head.value == "Back"
    assert empty_sll._tail is empty_sll._head


def test_filled_sll_append(filled_sll) -> None:
    filled_sll.append("Back")
    assert filled_sll._tail.value == "Back"
    assert len(filled_sll) == 9
    assert filled_sll._tail.next is None


def test_append_updates_tail(empty_sll) -> None:
    empty_sll.append(1)
    empty_sll.append(2)
    empty_sll.append(3)
    assert empty_sll._tail.value == 3
    assert empty_sll._head.value == 1


# -------------- Prepend Tests ---------------
def test_empty_sll_prepend(empty_sll) -> None:
    empty_sll.prepend("Head")
    assert empty_sll._head.value == "Head"
    assert empty_sll._tail is empty_sll._head


def test_filled_sll_prepend(filled_sll) -> None:
    filled_sll.prepend("Head")
    assert filled_sll._head.value == "Head"
    assert len(filled_sll) == 9


def test_prepend_links(empty_sll) -> None:
    empty_sll.prepend(2)
    empty_sll.prepend(1)
    assert empty_sll._head.value == 1
    assert empty_sll._head.next.value == 2


# --------------- Insert Tests ----------------
def test_insert_at_zero(filled_sll) -> None:
    filled_sll.insert(0, 99)
    assert filled_sll._head.value == 99
    assert len(filled_sll) == 9


def test_insert_at_end(filled_sll) -> None:
    filled_sll.insert(len(filled_sll), 99)
    assert filled_sll._tail.value == 99
    assert len(filled_sll) == 9


def test_insert_in_middle(filled_sll) -> None:
    filled_sll.insert(3, 99)
    assert filled_sll.get_node(3).value == 99
    assert filled_sll.get_node(4).value == 4
    assert len(filled_sll) == 9


def test_insert_out_of_range(filled_sll) -> None:
    with pytest.raises(IndexError):
        filled_sll.insert(99, 0)


def test_insert_wrong_type(filled_sll) -> None:
    with pytest.raises(TypeError):
        filled_sll.insert("a", 0)


# --------------- get_node Tests ----------------
def test_get_node(filled_sll) -> None:
    assert filled_sll.get_node(0).value == 1
    assert filled_sll.get_node(7).value == 8


def test_get_node_negative(filled_sll) -> None:
    assert filled_sll.get_node(-1).value == 8
    assert filled_sll.get_node(-8).value == 1


def test_get_node_out_of_range(filled_sll) -> None:
    with pytest.raises(IndexError):
        filled_sll.get_node(99)


def test_get_node_wrong_type(filled_sll) -> None:
    with pytest.raises(TypeError):
        filled_sll.get_node("a")


# --------------- set_node Tests ----------------
def test_set_node(filled_sll) -> None:
    filled_sll.set_node(0, 99)
    assert filled_sll.get_node(0).value == 99


def test_set_node_at_size(filled_sll) -> None:
    filled_sll.set_node(len(filled_sll), 99)
    assert filled_sll._tail.value == 99
    assert len(filled_sll) == 9


def test_set_node_negative(filled_sll) -> None:
    filled_sll.set_node(-1, 99)
    assert filled_sll._tail.value == 99


# --------------- remove_head Tests ----------------
def test_remove_head(filled_sll) -> None:
    value = filled_sll.remove_head()
    assert value == 1
    assert filled_sll._head.value == 2
    assert len(filled_sll) == 7


def test_remove_head_single_element(empty_sll) -> None:
    empty_sll.append(1)
    value = empty_sll.remove_head()
    assert value == 1
    assert empty_sll._head is None
    assert empty_sll._tail is None
    assert len(empty_sll) == 0


def test_remove_head_empty(empty_sll) -> None:
    with pytest.raises(IndexError):
        empty_sll.remove_head()


# --------------- remove_tail Tests ----------------
def test_remove_tail(filled_sll) -> None:
    value = filled_sll.remove_tail()
    assert value == 8
    assert filled_sll._tail.value == 7
    assert filled_sll._tail.next is None
    assert len(filled_sll) == 7


def test_remove_tail_single_element(empty_sll) -> None:
    empty_sll.append(1)
    value = empty_sll.remove_tail()
    assert value == 1
    assert empty_sll._head is None
    assert empty_sll._tail is None
    assert len(empty_sll) == 0


def test_remove_tail_empty(empty_sll) -> None:
    with pytest.raises(IndexError):
        empty_sll.remove_tail()


# --------------- remove Tests ----------------
def test_remove_middle(filled_sll) -> None:
    value = filled_sll.remove(3)
    assert value == 4
    assert filled_sll.get_node(3).value == 5
    assert len(filled_sll) == 7


def test_remove_at_zero(filled_sll) -> None:
    value = filled_sll.remove(0)
    assert value == 1
    assert filled_sll._head.value == 2


def test_remove_at_last(filled_sll) -> None:
    value = filled_sll.remove(len(filled_sll) - 1)
    assert value == 8
    assert filled_sll._tail.value == 7


def test_remove_negative(filled_sll) -> None:
    value = filled_sll.remove(-1)
    assert value == 8


def test_remove_out_of_range(filled_sll) -> None:
    with pytest.raises(IndexError):
        filled_sll.remove(99)


# --------------- find Tests ----------------
def test_find_existing(filled_sll) -> None:
    assert filled_sll.find(1) == 0
    assert filled_sll.find(8) == 7
    assert filled_sll.find(5) == 4


def test_find_not_existing(filled_sll) -> None:
    assert filled_sll.find(99) == -1


def test_find_empty(empty_sll) -> None:
    assert empty_sll.find(1) == -1


# --------------- __iter__ Tests ----------------
def test_iter(filled_sll) -> None:
    values = list(filled_sll)
    assert values == [1, 2, 3, 4, 5, 6, 7, 8]


def test_iter_empty(empty_sll) -> None:
    assert list(empty_sll) == []


# --------------- __contains__ Tests ----------------
def test_contains_existing(filled_sll) -> None:
    assert 1 in filled_sll
    assert 8 in filled_sll


def test_contains_not_existing(filled_sll) -> None:
    assert 99 not in filled_sll


# --------------- __len__ Tests ----------------
def test_len_empty(empty_sll) -> None:
    assert len(empty_sll) == 0


def test_len_after_operations(empty_sll) -> None:
    empty_sll.append(1)
    empty_sll.append(2)
    empty_sll.prepend(0)
    assert len(empty_sll) == 3
    empty_sll.remove_head()
    assert len(empty_sll) == 2


# --------------- __repr__ Tests ----------------
def test_repr_empty(empty_sll) -> None:
    assert repr(empty_sll) == "SinglyLinkedList([None])"


def test_repr_filled(filled_sll) -> None:
    assert (
        repr(filled_sll)
        == "SinglyLinkedList([1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> None])"
    )
