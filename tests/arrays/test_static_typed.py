import pytest

from data_structures.arrays import StaticTypedArray


# -------------- Fixtures ----------------
@pytest.fixture
def int_array() -> StaticTypedArray:
    return StaticTypedArray(10, dtype=int)


@pytest.fixture
def float_array() -> StaticTypedArray:
    return StaticTypedArray(10, dtype=float)


@pytest.fixture
def bool_array() -> StaticTypedArray:
    return StaticTypedArray(10, dtype=bool)


@pytest.fixture
def str_array() -> StaticTypedArray:
    return StaticTypedArray(10, dtype=str, str_length=20)


# -------------- Creation Tests ----------------
def test_int_array_creation(int_array) -> None:
    assert "StaticTypedArray" in repr(int_array)


def test_array_invalid_capacity_type() -> None:
    with pytest.raises(TypeError):
        StaticTypedArray("hello", dtype=int)


def test_array_negative_capacity() -> None:
    with pytest.raises(ValueError):
        StaticTypedArray(-1, dtype=int)


def test_array_zero_capacity() -> None:
    with pytest.raises(ValueError):
        StaticTypedArray(0, dtype=int)


def test_unsupported_dtype() -> None:
    with pytest.raises(TypeError):
        StaticTypedArray(10, dtype=list)


def test_str_length_without_str_dtype() -> None:
    with pytest.raises(ValueError):
        StaticTypedArray(10, dtype=int, str_length=20)


def test_str_length_invalid_type() -> None:
    with pytest.raises(TypeError):
        StaticTypedArray(10, dtype=str, str_length="hello")


def test_str_length_invalid_value() -> None:
    with pytest.raises(ValueError):
        StaticTypedArray(10, dtype=str, str_length=0)


# -------------- Int Array Tests ----------------
def test_int_set_and_get(int_array) -> None:
    int_array[0] = 42
    assert int_array[0] == 42


def test_int_wrong_type(int_array) -> None:
    with pytest.raises(TypeError):
        int_array[0] = "hello"


def test_int_out_of_range(int_array) -> None:
    with pytest.raises(IndexError):
        int_array[99] = 1


def test_int_negative_index(int_array) -> None:
    with pytest.raises(IndexError):
        int_array[-1] = 1


def test_int_index_zero(int_array) -> None:
    int_array[0] = 7
    assert int_array[0] == 7


# -------------- Float Array Tests ----------------
def test_float_set_and_get(float_array) -> None:
    float_array[0] = 3.14
    assert round(float_array[0], 2) == 3.14


def test_float_wrong_type(float_array) -> None:
    with pytest.raises(TypeError):
        float_array[0] = "hello"


# -------------- Bool Array Tests ----------------
def test_bool_set_and_get(bool_array) -> None:
    bool_array[0] = True
    bool_array[1] = False
    assert bool_array[0] is True
    assert bool_array[1] is False


def test_bool_wrong_type(bool_array) -> None:
    with pytest.raises(TypeError):
        bool_array[0] = "hello"


# -------------- Str Array Tests ----------------
def test_str_set_and_get(str_array) -> None:
    str_array[0] = "hello"
    assert str_array[0] == "hello"


def test_str_wrong_type(str_array) -> None:
    with pytest.raises(TypeError):
        str_array[0] = 42


def test_str_too_long(str_array) -> None:
    with pytest.raises(ValueError):
        str_array[0] = "a" * 100


def test_str_default_length() -> None:
    arr = StaticTypedArray(5, dtype=str)
    arr[0] = "hello"
    assert arr[0] == "hello"


# -------------- Other Methods Tests ----------------
def test_len(int_array) -> None:
    assert len(int_array) == 10


def test_iter(int_array) -> None:
    for i in range(10):
        int_array[i] = i
    values = list(int_array)
    assert len(values) == 10


def test_repr(int_array) -> None:
    assert repr(int_array).startswith("StaticTypedArray")
