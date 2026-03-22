import pytest

from data_structures.stacks import StaticTypedStack

# -------------- Fixtures ----------------


@pytest.fixture
def empty_sts() -> StaticTypedStack:
    return StaticTypedStack(dtype=int, capacity=5)


@pytest.fixture
def filled_sts() -> StaticTypedStack:
    return StaticTypedStack(1, 2, 3, 4, 5, dtype=int, capacity=10)


@pytest.fixture
def full_sts() -> StaticTypedStack:
    return StaticTypedStack(1, 2, 3, dtype=int, capacity=3)


# -------------- Creation Tests ----------------


def test_empty_creation(empty_sts: StaticTypedStack) -> None:
    assert len(empty_sts) == 5
    assert empty_sts._top == -1
    assert empty_sts.is_empty()


def test_creation_with_args(filled_sts: StaticTypedStack) -> None:
    assert filled_sts._top == 4
    assert filled_sts.peek() == 5


def test_creation_wrong_type() -> None:
    with pytest.raises(TypeError):
        StaticTypedStack(1, 2, "hello", dtype=int)


def test_creation_overflow() -> None:
    with pytest.raises(OverflowError):
        StaticTypedStack(1, 2, 3, dtype=int, capacity=2)


# -------------- Push Tests ----------------


def test_push(empty_sts: StaticTypedStack) -> None:
    empty_sts.push(42)
    assert empty_sts.peek() == 42
    assert empty_sts._top == 0


def test_push_wrong_type(empty_sts: StaticTypedStack) -> None:
    with pytest.raises(TypeError):
        empty_sts.push("hello")


def test_push_full(full_sts: StaticTypedStack) -> None:
    with pytest.raises(OverflowError):
        full_sts.push(99)


# -------------- Pop Tests ----------------


def test_pop(filled_sts: StaticTypedStack) -> None:
    value = filled_sts.pop()
    assert value == 5
    assert filled_sts._top == 3


def test_pop_resets_slot(filled_sts: StaticTypedStack) -> None:
    filled_sts.pop()
    assert filled_sts._data[4] == 0  # int default


def test_pop_empty(empty_sts: StaticTypedStack) -> None:
    with pytest.raises(IndexError):
        empty_sts.pop()


# -------------- Peek Tests ----------------


def test_peek(filled_sts: StaticTypedStack) -> None:
    assert filled_sts.peek() == 5
    assert filled_sts._top == 4


def test_peek_empty(empty_sts: StaticTypedStack) -> None:
    with pytest.raises(IndexError):
        empty_sts.peek()


# -------------- is_empty / is_full Tests ----------------


def test_is_empty(empty_sts: StaticTypedStack) -> None:
    assert empty_sts.is_empty()


def test_is_full(full_sts: StaticTypedStack) -> None:
    assert full_sts.is_full()


# -------------- copy Tests ----------------


def test_copy(filled_sts: StaticTypedStack) -> None:
    copied = filled_sts.copy()
    assert copied == filled_sts


def test_copy_is_independent(filled_sts: StaticTypedStack) -> None:
    copied = filled_sts.copy()
    copied.push(99)
    assert filled_sts.peek() == 5


# -------------- __eq__ Tests ----------------


def test_eq(filled_sts: StaticTypedStack) -> None:
    other = StaticTypedStack(1, 2, 3, 4, 5, dtype=int)
    assert filled_sts == other


def test_eq_different_dtype() -> None:
    s1 = StaticTypedStack(1, dtype=int)
    s2 = StaticTypedStack(1.0, dtype=float)
    assert s1 != s2


# -------------- __iter__ Tests ----------------


def test_iter(filled_sts: StaticTypedStack) -> None:
    assert list(filled_sts) == [5, 4, 3, 2, 1]


def test_iter_empty(empty_sts: StaticTypedStack) -> None:
    assert list(empty_sts) == []


# -------------- __repr__ Tests ----------------


def test_repr(filled_sts: StaticTypedStack) -> None:
    assert repr(filled_sts).startswith("StaticTypedStack")
