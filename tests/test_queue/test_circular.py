import pytest
from data_structures.queue import CircularQueue


# ---------- Fixtures -----------
@pytest.fixture
def filled_queue() -> CircularQueue:
    queue = CircularQueue()
    for n in range(10):
        queue.enqueue(n)
    return queue


@pytest.fixture
def empty_queue() -> CircularQueue:
    return CircularQueue()


# -------- Tests ---------
def test_queue_creation(empty_queue, filled_queue) -> None:
    # Checking dunder method of queue and queue properly creation
    assert bool(empty_queue) is False
    assert bool(filled_queue) is True


def test_circular_equality(filled_queue) -> None:
    # Checking Circulation of queue
    assert filled_queue._head is filled_queue._tail.next
    assert filled_queue._head.value == filled_queue._tail.next.value


def test_queue_len_method(empty_queue, filled_queue) -> None:
    # Checking properly work of dunder len method
    assert len(filled_queue) == 10
    assert len(empty_queue) == 0


def test_queue_enqueue_method(empty_queue, filled_queue) -> None:
    # Checking queue enqueue method that adds new node to queue
    empty_queue.enqueue(1)
    filled_queue.enqueue(1)

    assert len(empty_queue) == 1
    assert len(filled_queue) == 11


def test_queue_dequeue_method(filled_queue) -> None:
    # Checking queue dequeue method work
    assert filled_queue.dequeue() == 0


def test_queue_dequeue_index_err(empty_queue) -> None:
    # Checking queue raises Indexerror for empty queue ot not
    with pytest.raises(IndexError):
        empty_queue.dequeue()


def test_queue_peek_method(filled_queue) -> None:
    # Checking queue peek method
    filled_queue.enqueue(15)
    assert filled_queue.peek() == 0


def test_queue_peek_index_err(empty_queue) -> None:
    # Checking queue raises IndexError for empty queue or not
    with pytest.raises(IndexError):
        empty_queue.peek()


def test_queue_copy_method(filled_queue) -> None:
    copied_queue = filled_queue.copy()

    assert copied_queue is not filled_queue
    assert copied_queue == filled_queue


def test_queue_iter_method(filled_queue) -> None:
    values = list(filled_queue)
    assert values == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_queue_reversed_method(filled_queue) -> None:
    values = list(reversed(filled_queue))
    assert values == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


def test_queue_contain_method(filled_queue, empty_queue) -> None:
    # Checking queue contain method
    assert 7 in filled_queue
    assert 3 not in empty_queue


def test_queue_str_method(filled_queue) -> None:
    assert str(filled_queue).startswith('CircularQueue(front -')
    assert str(filled_queue).endswith(' - rear)')
