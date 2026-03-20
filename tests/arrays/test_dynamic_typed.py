import pytest

from data_structures.arrays import DynamicTypedArray


# -------------- Fixtures ----------------
@pytest.fixture
def empty_int_arr() -> DynamicTypedArray:
    return DynamicTypedArray(int)


@pytest.fixture
def filled_int_arr() -> DynamicTypedArray:
    return DynamicTypedArray(int, 1, 2, 3, 4, 5)


@pytest.fixture
def empty_float_arr() -> DynamicTypedArray:
    return DynamicTypedArray(float)


@pytest.fixture
def filled_float_arr() -> DynamicTypedArray:
    return DynamicTypedArray(float, 1.1, 2.2, 3.3)


@pytest.fixture
def empty_bool_arr() -> DynamicTypedArray:
    return DynamicTypedArray(bool)


@pytest.fixture
def empty_str_arr() -> DynamicTypedArray:
    return DynamicTypedArray(str, str_length=20)


# -------------- Creation Tests ----------------
def test_int_empty_creation(empty_int_arr) -> None:
    assert len(empty_int_arr) == 0
    assert empty_int_arr._capacity == 4


def test_int_creation_with_args(filled_int_arr) -> None:
    assert len(filled_int_arr) == 5
    assert filled_int_arr[0] == 1
    assert filled_int_arr[4] == 5


def test_unsupported_dtype() -> None:
    with pytest.raises(TypeError):
        DynamicTypedArray(list)


def test_str_length_only_for_str() -> None:
    with pytest.raises(ValueError):
        DynamicTypedArray(int, str_length=20)


# -------------- Int Array Tests ----------------
def test_int_append(empty_int_arr) -> None:
    empty_int_arr.append(42)
    assert empty_int_arr[0] == 42
    assert len(empty_int_arr) == 1


def test_int_append_wrong_type(empty_int_arr) -> None:
    with pytest.raises(TypeError):
        empty_int_arr.append("hello")


def test_int_append_triggers_resize() -> None:
    arr = DynamicTypedArray(int)
    initial_capacity = arr._capacity
    for i in range(initial_capacity + 1):
        arr.append(i)
    assert arr._capacity > initial_capacity


def test_int_insert_at_beginning(filled_int_arr) -> None:
    filled_int_arr.insert(0, 99)
    assert filled_int_arr[0] == 99
    assert filled_int_arr[1] == 1


def test_int_insert_wrong_type(filled_int_arr) -> None:
    with pytest.raises(TypeError):
        filled_int_arr.insert(0, "hello")


def test_int_insert_out_of_range(filled_int_arr) -> None:
    with pytest.raises(IndexError):
        filled_int_arr.insert(999, 99)


def test_int_remove_first(filled_int_arr) -> None:
    removed = filled_int_arr.remove(0)
    assert removed == 1
    assert len(filled_int_arr) == 4
    assert filled_int_arr[0] == 2


def test_int_remove_last(filled_int_arr) -> None:
    removed = filled_int_arr.remove(-1)
    assert removed == 5
    assert len(filled_int_arr) == 4


def test_int_remove_out_of_range(filled_int_arr) -> None:
    with pytest.raises(IndexError):
        filled_int_arr.remove(999)


def test_int_getitem(filled_int_arr) -> None:
    assert filled_int_arr[0] == 1
    assert filled_int_arr[-1] == 5


def test_int_setitem(filled_int_arr) -> None:
    filled_int_arr[0] = 99
    assert filled_int_arr[0] == 99


def test_int_setitem_wrong_type(filled_int_arr) -> None:
    with pytest.raises(TypeError):
        filled_int_arr[0] = "hello"


def test_int_len(filled_int_arr) -> None:
    assert len(filled_int_arr) == 5


def test_int_iter(filled_int_arr) -> None:
    assert list(filled_int_arr) == [1, 2, 3, 4, 5]


def test_int_repr(filled_int_arr) -> None:
    assert repr(filled_int_arr).startswith("DynamicTypedArray")


# -------------- Float Array Tests ----------------
def test_float_append(empty_float_arr) -> None:
    empty_float_arr.append(3.14)
    assert round(empty_float_arr[0], 2) == 3.14


def test_float_wrong_type(empty_float_arr) -> None:
    with pytest.raises(TypeError):
        empty_float_arr.append("hello")


def test_float_iter(filled_float_arr) -> None:
    values = [round(v, 1) for v in filled_float_arr]
    assert values == [1.1, 2.2, 3.3]


# -------------- Bool Array Tests ----------------
def test_bool_append(empty_bool_arr) -> None:
    empty_bool_arr.append(True)
    empty_bool_arr.append(False)
    assert empty_bool_arr[0] is True
    assert empty_bool_arr[1] is False


def test_bool_wrong_type(empty_bool_arr) -> None:
    with pytest.raises(TypeError):
        empty_bool_arr.append("hello")


# -------------- Str Array Tests ----------------
def test_str_append(empty_str_arr) -> None:
    empty_str_arr.append("hello")
    assert empty_str_arr[0] == "hello"


def test_str_too_long(empty_str_arr) -> None:
    with pytest.raises(ValueError):
        empty_str_arr.append("a" * 100)


def test_str_wrong_type(empty_str_arr) -> None:
    with pytest.raises(TypeError):
        empty_str_arr.append(42)


def test_str_default_length() -> None:
    arr = DynamicTypedArray(str)
    arr.append("hello")
    assert arr[0] == "hello"
