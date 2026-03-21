import pytest

from data_structures import DoublyLinkedList


# ----------------- Fixtures ----------------
@pytest.fixture
def empty_dll() -> DoublyLinkedList:
    return DoublyLinkedList()


@pytest.fixture
def filled_dll() -> DoublyLinkedList:
    return DoublyLinkedList(1, 2, 3, 4, 5, 6, 7, 8)


# ---------------- Creation Tests ----------------
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
    assert filled_dll._tail.prev.value == 7
    assert filled_dll._tail.next is None


# -------------- Append Tests -----------------
def test_empty_dll_append(empty_dll) -> None:
    empty_dll.append("Back")
    assert empty_dll._head.value == "Back"
    assert empty_dll._head is empty_dll._tail
