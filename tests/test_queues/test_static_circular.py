import pytest
from data_structures.queues import StaticCircularQueue


@pytest.fixture
def filled_queue() -> StaticCircularQueue:
    queue = StaticCircularQueue(10)
    for n in range(10):
        queue.enqueue(n)
    return queue


@pytest.fixture
def empty_queue() -> StaticCircularQueue:
    return StaticCircularQueue(10)


def test_queue_creation(empty_queue, filled_queue) -> None:
    assert bool(empty_queue) is False
    assert bool(filled_queue) is True


def test_queue_len(empty_queue, filled_queue) -> None:
    assert len(empty_queue) == 0
    assert len(filled_queue) == 10


def test_queue_is_full(filled_queue, empty_queue) -> None:
    assert filled_queue.is_full() is True
    assert empty_queue.is_full() is False


def test_queue_enqueue(empty_queue) -> None:
    empty_queue.enqueue(1)
    assert len(empty_queue) == 1
    assert empty_queue.peek() == 1


def test_queue_enqueue_full(filled_queue) -> None:
    with pytest.raises(MemoryError):
        filled_queue.enqueue(99)


def test_queue_dequeue(filled_queue) -> None:
    assert filled_queue.dequeue() == 0
    assert len(filled_queue) == 9


def test_queue_dequeue_clears_slot(empty_queue) -> None:
    empty_queue.enqueue(42)
    empty_queue.dequeue()
    # Slot must be cleared after dequeue
    assert empty_queue._array[0] is None


def test_queue_dequeue_empty(empty_queue) -> None:
    with pytest.raises(IndexError):
        empty_queue.dequeue()


def test_queue_peek(filled_queue) -> None:
    assert filled_queue.peek() == 0
    assert len(filled_queue) == 10


def test_queue_peek_empty(empty_queue) -> None:
    with pytest.raises(IndexError):
        empty_queue.peek()


def test_queue_wrap_around() -> None:
    # This tests the core circular behavior — tail wraps around to index 0
    queue = StaticCircularQueue(3)
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    queue.dequeue()  # frees slot 0
    queue.enqueue(4)  # should land at slot 0 again via wrap-around
    assert list(queue) == [2, 3, 4]


def test_queue_iter(filled_queue) -> None:
    assert list(filled_queue) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_queue_iter_wrap_around() -> None:
    queue = StaticCircularQueue(4)
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    queue.dequeue()
    queue.enqueue(4)
    # head=1, tail=0, wraps around
    assert list(queue) == [2, 3, 4]


def test_queue_reversed(filled_queue) -> None:
    assert list(reversed(filled_queue)) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


def test_queue_reversed_wrap_around() -> None:
    queue = StaticCircularQueue(4)
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    queue.dequeue()
    queue.enqueue(4)
    assert list(reversed(queue)) == [4, 3, 2]


def test_queue_contains(filled_queue, empty_queue) -> None:
    assert 7 in filled_queue
    assert 99 not in filled_queue
    assert 3 not in empty_queue


def test_queue_copy(filled_queue) -> None:
    copied = filled_queue.copy()
    assert copied is not filled_queue
    assert copied == filled_queue


def test_queue_copy_same_physical_layout(filled_queue) -> None:
    # Copy must have same head, tail, and slot positions — not just same values
    copied = filled_queue.copy()
    assert copied._head == filled_queue._head
    assert copied._tail == filled_queue._tail
    assert list(copied._array) == list(filled_queue._array)


def test_queue_copy_independence(filled_queue) -> None:
    copied = filled_queue.copy()
    filled_queue.dequeue()
    assert copied != filled_queue


def test_queue_str(filled_queue) -> None:
    result = str(filled_queue)
    assert result.startswith('StaticCircularQueue(capacity=')
    assert 'front ->' in result
    assert '<- rear)' in result
