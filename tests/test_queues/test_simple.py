import pytest
from data_structures.queues import SimpleQueue


@pytest.fixture
def filled_queue() -> SimpleQueue:
    queue = SimpleQueue()
    for n in range(10):
        queue.enqueue(n)
    return queue


@pytest.fixture
def empty_queue() -> SimpleQueue:
    return SimpleQueue()


def test_queue_creation(empty_queue, filled_queue) -> None:
    assert bool(empty_queue) is False
    assert bool(filled_queue) is True


def test_queue_len(empty_queue, filled_queue) -> None:
    assert len(empty_queue) == 0
    assert len(filled_queue) == 10


def test_queue_enqueue(empty_queue, filled_queue) -> None:
    empty_queue.enqueue(1)
    filled_queue.enqueue(1)
    assert len(empty_queue) == 1
    assert len(filled_queue) == 11


def test_queue_dequeue(filled_queue) -> None:
    # FIFO — first enqueued (0) is first out
    assert filled_queue.dequeue() == 0
    assert len(filled_queue) == 9


def test_queue_dequeue_empty(empty_queue) -> None:
    with pytest.raises(IndexError):
        empty_queue.dequeue()


def test_queue_dequeue_until_empty(empty_queue) -> None:
    empty_queue.enqueue(1)
    empty_queue.dequeue()
    # After last dequeue, both head and tail must be None
    assert empty_queue._head is None
    assert empty_queue._tail is None


def test_queue_peek(filled_queue) -> None:
    filled_queue.enqueue(99)
    # peek shows head — which is still 0
    assert filled_queue.peek() == 0
    assert len(filled_queue) == 11


def test_queue_peek_empty(empty_queue) -> None:
    with pytest.raises(IndexError):
        empty_queue.peek()


def test_queue_copy(filled_queue) -> None:
    copied = filled_queue.copy()
    assert copied is not filled_queue
    assert copied == filled_queue


def test_queue_copy_independence(filled_queue) -> None:
    copied = filled_queue.copy()
    filled_queue.enqueue(99)
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
    assert str(filled_queue).startswith('SimpleQueue(head ->')
    assert str(filled_queue).endswith('<- tail)')


def test_queue_size_method(filled_queue) -> None:
    assert filled_queue.size() == 10
