import pytest

from data_structures.array import Array

# -------------- TESTS ----------------


# Creation tests
def test_array_creatinon() -> None:
    # Test creation of Array
    array = Array(capacity=10)
    assert "Array(capacity=10," in repr(array)


def test_array_invalid_capacity() -> None:
    # Checking raises invlid capacity error or not
    with pytest.raises(ValueError):
        Array(-7)


def test_array_invalid_type() -> None:
    # Checking raises invalid type or not
    with pytest.raises(TypeError):
        Array("h")


# Reading / Writing tests
def test_set_and_get_item() -> None:
    # Checking setting and getting methods of array
    array = Array(10)
    array[0] = 99
    assert array[0] == 99
    assert array[1] is None


def test_getitem_out_of_range() -> None:
    # Checking getting item out of range error
    array = Array(10)

    with pytest.raises(IndexError):
        val = array[99]  # noqa


def test_setitem_out_of_range() -> None:
    # Checking setting item out of range error
    array = Array(10)

    with pytest.raises(IndexError):
        array[99] = "error"


def test_getitem_wrong_type() -> None:
    # Checking getting item index wrong type error
    array = Array(10)

    with pytest.raises(TypeError):
        val = array["error"]  # noqa


def test_setitem_wrong_type() -> None:
    # Checking setting item index wrong type error
    array = Array(10)

    with pytest.raises(TypeError):
        array["error"] = 1


# Others methods tests
def test_len() -> None:
    # Checking method lenght properly work
    array = Array(10)
    assert len(array) == 10


def test_bool() -> None:
    # Checking bool method of array
    array = Array(10)
    assert bool(array) is False  # must return False


def test_iter() -> None:
    # Checking method iter properly work
    array = Array(10)

    for index in range(len(array)):
        array[index] = index

    for index in range(len(array)):
        assert array[index] == index


def test_accepts_any_type() -> None:
    """Checking array accpets any type of python obj or not"""
    array = Array(10)
    array[1] = "Hello"
    array[9] = 7
    array[6] = 1.6
    array[2] = [1, 2, "hello"]

    assert isinstance(array[1], str)
    assert isinstance(array[9], int)
    assert isinstance(array[6], float)
    assert isinstance(array[2], list)
