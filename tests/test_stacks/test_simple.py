import pytest
from data_structures.stacks import SimpleStack


@pytest.fixture
def filled_stack() -> SimpleStack:
    stack = SimpleStack()
    for n in range(10):
        stack.push(n)
    return stack


@pytest.fixture
def empty_stack() -> SimpleStack:
    return SimpleStack()


def test_stack_creation(empty_stack, filled_stack) -> None:
    assert bool(empty_stack) is False
    assert bool(filled_stack) is True


def test_stack_len(empty_stack, filled_stack) -> None:
    assert len(empty_stack) == 0
    assert len(filled_stack) == 10


def test_stack_push(empty_stack, filled_stack) -> None:
    empty_stack.push(1)
    filled_stack.push(1)
    assert len(empty_stack) == 1
    assert len(filled_stack) == 11


def test_stack_pop(filled_stack) -> None:
    # LIFO — last pushed (9) is first out
    assert filled_stack.pop() == 9
    assert len(filled_stack) == 9


def test_stack_pop_empty(empty_stack) -> None:
    with pytest.raises(IndexError):
        empty_stack.pop()


def test_stack_peek(filled_stack) -> None:
    filled_stack.push(99)
    assert filled_stack.peek() == 99
    # peek does not remove
    assert len(filled_stack) == 11


def test_stack_peek_empty(empty_stack) -> None:
    with pytest.raises(IndexError):
        empty_stack.peek()


def test_stack_copy(filled_stack) -> None:
    copied = filled_stack.copy()
    assert copied is not filled_stack
    assert copied == filled_stack


def test_stack_copy_independence(filled_stack) -> None:
    copied = filled_stack.copy()
    filled_stack.push(99)
    assert copied != filled_stack


def test_stack_iter(filled_stack) -> None:
    # Iterates top to bottom: last pushed first
    values = list(filled_stack)
    assert values == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


def test_stack_reversed(filled_stack) -> None:
    values = list(reversed(filled_stack))
    assert values == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_stack_contains(filled_stack, empty_stack) -> None:
    assert 7 in filled_stack
    assert 99 not in filled_stack
    assert 3 not in empty_stack


def test_stack_str(filled_stack) -> None:
    assert str(filled_stack).startswith('Stack(top ->')


def test_stack_size_method(filled_stack) -> None:
    assert filled_stack.size() == 10
