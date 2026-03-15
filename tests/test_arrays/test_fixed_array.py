import pytest
from data_structures.arrays import FixedArray


@pytest.fixture
def array() -> FixedArray:
    return FixedArray(5)


def test_fixed_array_creation(array) -> None:
    assert len(array) == 5


def test_fixed_array_all_slots_none(array) -> None:
    for value in array:
        assert value is None


def test_fixed_array_invalid_capacity() -> None:
    with pytest.raises(ValueError):
        FixedArray(0)
    with pytest.raises(ValueError):
        FixedArray(-1)


def test_fixed_array_setitem(array) -> None:
    array[0] = 'hello'
    array[4] = 42
    assert array[0] == 'hello'
    assert array[4] == 42


def test_fixed_array_getitem(array) -> None:
    array[2] = [1, 2, 3]
    assert array[2] == [1, 2, 3]


def test_fixed_array_accepts_any_type(array) -> None:
    array[0] = 1
    array[1] = 'string'
    array[2] = [1, 2]
    array[3] = {'key': 'val'}
    array[4] = None
    assert array[0] == 1
    assert array[1] == 'string'
    assert array[2] == [1, 2]
    assert array[3] == {'key': 'val'}
    assert array[4] is None


def test_fixed_array_index_error(array) -> None:
    with pytest.raises(IndexError):
        array[5]
    with pytest.raises(IndexError):
        array[5] = 1


def test_fixed_array_type_error(array) -> None:
    with pytest.raises(TypeError):
        array['hello']
    with pytest.raises(TypeError):
        array['hello'] = 1


def test_fixed_array_no_negative_index(array) -> None:
    with pytest.raises(IndexError):
        array[-1]


def test_fixed_array_iter(array) -> None:
    array[0] = 10
    array[2] = 20
    values = list(array)
    assert values == [10, None, 20, None, None]


def test_fixed_array_repr(array) -> None:
    assert repr(array).startswith('FixedArray(capacity=5')
