import pytest
from data_structures.queues import Deque


@pytest.fixture
def filled_queue() -> Deque:
    queue = Deque()
    for n in range(10):
        queue.add_back(n)
    return queue


@pytest.fixture
def empty_queue() -> Deque:
    return Deque()


def test_queue_creation(empty_queue, filled_queue) -> None:
    assert bool(empty_queue) is False
    assert bool(filled_queue) is True


def test_queue_len(empty_queue, filled_queue) -> None:
    assert len(empty_queue) == 0
    assert len(filled_queue) == 10


def test_queue_add_front(empty_queue, filled_queue) -> None:
    empty_queue.add_front(1)
    filled_queue.add_front(1)
    assert len(empty_queue) == 1
    assert len(filled_queue) == 11


def test_queue_add_back(empty_queue, filled_queue) -> None:
    empty_queue.add_back(1)
    filled_queue.add_back(1)
    assert len(empty_queue) == 1
    assert len(filled_queue) == 11


def test_queue_remove_front(filled_queue) -> None:
    assert filled_queue.remove_front() == 0
    assert len(filled_queue) == 9


def test_queue_remove_back(filled_queue) -> None:
    assert filled_queue.remove_back() == 9
    assert len(filled_queue) == 9


def test_queue_remove_front_error(empty_queue) -> None:
    with pytest.raises(IndexError):
        empty_queue.remove_front()


def test_queue_remove_back_error(empty_queue) -> None:
    with pytest.raises(IndexError):
        empty_queue.remove_back()


def test_queue_remove_unit_empty(empty_queue) -> None:
    empty_queue.add_back(1)
    empty_queue.remove_front()
    # After last remove, both head and tail must be None
    assert empty_queue._head is None
    assert empty_queue._tail is None
    assert empty_queue._size == 0


def test_queue_front_peek(filled_queue) -> None:
    filled_queue.add_back(99)
    # front_peek shows head - which is still 0
    assert filled_queue.peek_front() == 0
    assert len(filled_queue) == 11


def test_queue_back_peek(filled_queue) -> None:
    filled_queue.add_front(99)
    # peek_back shows tail - which is still 9
    assert filled_queue.peek_back() == 9
    assert len(filled_queue) == 11


def test_queue_peek_front_empty_error(empty_queue) -> None:
    with pytest.raises(IndexError):
        empty_queue.peek_front()


def test_queue_peek_back_empty_error(empty_queue) -> None:
    with pytest.raises(IndexError):
        empty_queue.peek_back()


def test_queue_copy(filled_queue) -> None:
    copied = filled_queue.copy()
    assert copied is not filled_queue
    assert copied == filled_queue


def test_queue_copy_independence(filled_queue) -> None:
    copied = filled_queue.copy()
    filled_queue.add_front(99)
    assert copied != filled_queue


def test_queue_iter(filled_queue) -> None:
    # FIFO order: first in, first out
    assert list(filled_queue) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_queue_reversed(filled_queue) -> None:
    assert list(reversed(filled_queue)) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


def test_queue_contains(filled_queue, empty_queue) -> None:
    assert 7 in filled_queue
    assert 99 not in filled_queue
    assert 3 not in empty_queue


def test_queue_str(filled_queue) -> None:
    assert str(filled_queue).startswith('Deque(head ->')
    assert str(filled_queue).endswith('<- tail)')


def test_queueu_size_method(filled_queue) -> None:
    assert filled_queue.size() == 10
