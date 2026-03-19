import pytest

from data_structures.arrays import StaticUniversalArray


# -------------- Fixtures ----------------
@pytest.fixture
def array() -> StaticUniversalArray:
    return StaticUniversalArray(10)


@pytest.fixture
def filled_array() -> StaticUniversalArray:
    arr = StaticUniversalArray(10)
    for i in range(10):
        arr[i] = i
    return arr


# -------------- Creation Tests ----------------
def test_array_creation(array) -> None:
    assert "StaticUniversalArray(capacity=10" in repr(array)


def test_array_invalid_capacity_type() -> None:
    with pytest.raises(TypeError):
        StaticUniversalArray("hello")


def test_array_negative_capacity() -> None:
    with pytest.raises(ValueError):
        StaticUniversalArray(-1)


def test_array_zero_capacity() -> None:
    with pytest.raises(ValueError):
        StaticUniversalArray(0)


# -------------- Reading / Writing Tests ----------------
def test_set_and_get_item(array) -> None:
    array[0] = 99
    assert array[0] == 99


def test_default_slots_are_none(array) -> None:
    for i in range(len(array)):
        assert array[i] is None


def test_getitem_out_of_range(array) -> None:
    with pytest.raises(IndexError):
        _ = array[99]


def test_setitem_out_of_range(array) -> None:
    with pytest.raises(IndexError):
        array[99] = "error"


def test_getitem_negative_index(array) -> None:
    with pytest.raises(IndexError):
        _ = array[-1]


def test_setitem_negative_index(array) -> None:
    with pytest.raises(IndexError):
        array[-1] = "error"


def test_getitem_wrong_type(array) -> None:
    with pytest.raises(TypeError):
        _ = array["error"]  # noqa


def test_setitem_wrong_type(array) -> None:
    with pytest.raises(TypeError):
        array["error"] = 1


def test_getitem_index_zero(array) -> None:
    array[0] = "first"
    assert array[0] == "first"


# -------------- Other Methods Tests ----------------
def test_len(array) -> None:
    assert len(array) == 10


def test_iter(filled_array) -> None:
    values = list(filled_array)
    assert values == list(range(10))


def test_accepts_any_type(array) -> None:
    array[0] = 1
    array[1] = "hello"
    array[2] = 3.14
    array[3] = [1, 2, 3]
    array[4] = {"key": "val"}
    array[5] = None

    assert isinstance(array[0], int)
    assert isinstance(array[1], str)
    assert isinstance(array[2], float)
    assert isinstance(array[3], list)
    assert isinstance(array[4], dict)
    assert array[5] is None


def test_repr(array) -> None:
    assert repr(array).startswith("StaticUniversalArray(capacity=10")
