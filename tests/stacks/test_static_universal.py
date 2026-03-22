import pytest

from data_structures.stacks import StaticUniversalStack

# -------------- Fixtures ----------------


@pytest.fixture
def empty_sus() -> StaticUniversalStack:
    return StaticUniversalStack(capacity=5)


@pytest.fixture
def filled_sus() -> StaticUniversalStack:
    return StaticUniversalStack(1, 2, 3, 4, 5, capacity=10)


@pytest.fixture
def full_sus() -> StaticUniversalStack:
    return StaticUniversalStack(1, 2, 3, capacity=3)


# -------------- Creation Tests ----------------


def test_empty_creation(empty_sus: StaticUniversalStack) -> None:
    assert len(empty_sus) == 5
    assert empty_sus._top == -1
    assert empty_sus.is_empty()


def test_creation_with_args(filled_sus: StaticUniversalStack) -> None:
    assert filled_sus._top == 4
    assert filled_sus.peek() == 5


def test_creation_capacity_from_args() -> None:
    s = StaticUniversalStack(1, 2, 3)
    assert len(s) == 3
    assert s._top == 2


def test_creation_overflow() -> None:
    with pytest.raises(OverflowError):
        StaticUniversalStack(1, 2, 3, capacity=2)


# -------------- Push Tests ----------------


def test_push(empty_sus: StaticUniversalStack) -> None:
    empty_sus.push(42)
    assert empty_sus.peek() == 42
    assert empty_sus._top == 0


def test_push_multiple(empty_sus: StaticUniversalStack) -> None:
    empty_sus.push(1)
    empty_sus.push(2)
    empty_sus.push(3)
    assert empty_sus.peek() == 3
    assert empty_sus._top == 2


def test_push_any_type(empty_sus: StaticUniversalStack) -> None:
    empty_sus.push("hello")
    empty_sus.push([1, 2])
    empty_sus.push(None)
    assert empty_sus.peek() is None


def test_push_full(full_sus: StaticUniversalStack) -> None:
    with pytest.raises(OverflowError):
        full_sus.push(99)


# -------------- Pop Tests ----------------


def test_pop(filled_sus: StaticUniversalStack) -> None:
    value = filled_sus.pop()
    assert value == 5
    assert filled_sus._top == 3


def test_pop_clears_slot(filled_sus: StaticUniversalStack) -> None:
    filled_sus.pop()
    assert filled_sus._data[4] is None


def test_pop_empty(empty_sus: StaticUniversalStack) -> None:
    with pytest.raises(IndexError):
        empty_sus.pop()


def test_pop_until_empty(filled_sus: StaticUniversalStack) -> None:
    for _ in range(5):
        filled_sus.pop()
    assert filled_sus.is_empty()


# -------------- Peek Tests ----------------


def test_peek(filled_sus: StaticUniversalStack) -> None:
    assert filled_sus.peek() == 5
    assert filled_sus._top == 4


def test_peek_does_not_modify(filled_sus: StaticUniversalStack) -> None:
    filled_sus.peek()
    assert filled_sus._top == 4
    assert filled_sus.peek() == 5


def test_peek_empty(empty_sus: StaticUniversalStack) -> None:
    with pytest.raises(IndexError):
        empty_sus.peek()


# -------------- is_empty / is_full Tests ----------------


def test_is_empty(empty_sus: StaticUniversalStack) -> None:
    assert empty_sus.is_empty()


def test_is_not_empty(filled_sus: StaticUniversalStack) -> None:
    assert not filled_sus.is_empty()


def test_is_full(full_sus: StaticUniversalStack) -> None:
    assert full_sus.is_full()


def test_is_not_full(empty_sus: StaticUniversalStack) -> None:
    assert not empty_sus.is_full()


# -------------- copy Tests ----------------


def test_copy(filled_sus: StaticUniversalStack) -> None:
    copied = filled_sus.copy()
    assert copied == filled_sus


def test_copy_is_independent(filled_sus: StaticUniversalStack) -> None:
    copied = filled_sus.copy()
    copied.push(99)
    assert filled_sus.peek() == 5


def test_copy_empty(empty_sus: StaticUniversalStack) -> None:
    copied = empty_sus.copy()
    assert copied.is_empty()
    assert len(copied) == len(empty_sus)


# -------------- __eq__ Tests ----------------


def test_eq(filled_sus: StaticUniversalStack) -> None:
    other = StaticUniversalStack(1, 2, 3, 4, 5)
    assert filled_sus == other


def test_eq_different_elements(filled_sus: StaticUniversalStack) -> None:
    other = StaticUniversalStack(1, 2, 3)
    assert filled_sus != other


def test_eq_different_type(filled_sus: StaticUniversalStack) -> None:
    assert filled_sus != [1, 2, 3, 4, 5]


# -------------- __iter__ Tests ----------------


def test_iter(filled_sus: StaticUniversalStack) -> None:
    values = list(filled_sus)
    assert values == [5, 4, 3, 2, 1]


def test_iter_empty(empty_sus: StaticUniversalStack) -> None:
    assert list(empty_sus) == []


def test_iter_does_not_modify(filled_sus: StaticUniversalStack) -> None:
    list(filled_sus)
    assert filled_sus._top == 4


# -------------- __repr__ Tests ----------------


def test_repr(filled_sus: StaticUniversalStack) -> None:
    assert repr(filled_sus).startswith("StaticUniversalStack")
