import pytest

from data_structures.arrays import DynamicUniversalArray


# -------------- Fixtures ----------------
@pytest.fixture
def empty_arr() -> DynamicUniversalArray:
    return DynamicUniversalArray()


@pytest.fixture
def filled_arr() -> DynamicUniversalArray:
    return DynamicUniversalArray(1, 2, 3, 4, 5)


# -------------- Creation Tests ----------------
def test_empty_creation(empty_arr) -> None:
    assert len(empty_arr) == 0
    assert empty_arr._capacity == 4


def test_creation_with_args(filled_arr) -> None:
    assert len(filled_arr) == 5
    assert filled_arr[0] == 1
    assert filled_arr[4] == 5


def test_creation_capacity_grows_with_args() -> None:
    arr = DynamicUniversalArray(*range(10))
    assert len(arr) == 10
    assert arr._capacity >= 10


def test_creation_single_list_arg() -> None:
    arr = DynamicUniversalArray([1, 2, 3])
    assert len(arr) == 1
    assert arr[0] == [1, 2, 3]


# -------------- Append Tests ----------------
def test_append(empty_arr) -> None:
    empty_arr.append(99)
    assert len(empty_arr) == 1
    assert empty_arr[0] == 99


def test_append_triggers_resize() -> None:
    arr = DynamicUniversalArray()
    initial_capacity = arr._capacity
    for i in range(initial_capacity + 1):
        arr.append(i)
    assert arr._capacity > initial_capacity


def test_append_any_type(empty_arr) -> None:
    empty_arr.append(1)
    empty_arr.append("hello")
    empty_arr.append([1, 2])
    empty_arr.append(None)
    assert len(empty_arr) == 4


# -------------- Insert Tests ----------------
def test_insert_at_beginning(filled_arr) -> None:
    filled_arr.insert(0, 99)
    assert filled_arr[0] == 99
    assert filled_arr[1] == 1


def test_insert_at_middle(filled_arr) -> None:
    filled_arr.insert(2, 99)
    assert filled_arr[2] == 99
    assert filled_arr[3] == 3


def test_insert_at_end(filled_arr) -> None:
    filled_arr.insert(len(filled_arr), 99)
    assert filled_arr[-1] == 99


def test_insert_wrong_type(filled_arr) -> None:
    with pytest.raises(TypeError):
        filled_arr.insert("hello", 99)


def test_insert_out_of_range(filled_arr) -> None:
    with pytest.raises(IndexError):
        filled_arr.insert(999, 99)


def test_insert_negative_index(filled_arr) -> None:
    filled_arr.insert(-1, 99)
    assert filled_arr[-2] == 99


# -------------- Remove Tests ----------------
def test_remove_first(filled_arr) -> None:
    removed = filled_arr.remove(0)
    assert removed == 1
    assert len(filled_arr) == 4
    assert filled_arr[0] == 2


def test_remove_last(filled_arr) -> None:
    removed = filled_arr.remove(-1)
    assert removed == 5
    assert len(filled_arr) == 4


def test_remove_middle(filled_arr) -> None:
    removed = filled_arr.remove(2)
    assert removed == 3
    assert filled_arr[2] == 4


def test_remove_returns_value(filled_arr) -> None:
    assert filled_arr.remove(0) == 1


def test_remove_wrong_type(filled_arr) -> None:
    with pytest.raises(TypeError):
        filled_arr.remove("hello")


def test_remove_out_of_range(filled_arr) -> None:
    with pytest.raises(IndexError):
        filled_arr.remove(999)


# -------------- Getitem / Setitem Tests ----------------
def test_getitem(filled_arr) -> None:
    assert filled_arr[0] == 1
    assert filled_arr[4] == 5


def test_getitem_negative(filled_arr) -> None:
    assert filled_arr[-1] == 5
    assert filled_arr[-5] == 1


def test_getitem_out_of_range(filled_arr) -> None:
    with pytest.raises(IndexError):
        _ = filled_arr[999]  # noqa


def test_setitem(filled_arr) -> None:
    filled_arr[0] = 99
    assert filled_arr[0] == 99


def test_setitem_out_of_range(filled_arr) -> None:
    with pytest.raises(IndexError):
        filled_arr[999] = 99


# -------------- Other Methods Tests ----------------
def test_len(filled_arr) -> None:
    assert len(filled_arr) == 5


def test_iter(filled_arr) -> None:
    assert list(filled_arr) == [1, 2, 3, 4, 5]


def test_repr(filled_arr) -> None:
    assert repr(filled_arr).startswith("DynamicUniversalArray")
