import pytest

from data_structures.stacks import (
    DynamicNodeMinStack,
    DynamicTypedMinStack,
    DynamicUniversalMinStack,
    StaticTypedMinStack,
    StaticUniversalMinStack,
)

# ═══════════════════════════════════════════════
# StaticUniversalMinStack
# ═══════════════════════════════════════════════


@pytest.fixture
def empty_sums() -> StaticUniversalMinStack:
    return StaticUniversalMinStack(capacity=10)


@pytest.fixture
def filled_sums() -> StaticUniversalMinStack:
    return StaticUniversalMinStack(5, 3, 7, 1, 8, capacity=10)


@pytest.fixture
def key_sums() -> StaticUniversalMinStack:
    return StaticUniversalMinStack("hello", "hi", "hey", capacity=10, key=len)


# -------------- Creation Tests ----------------
def test_sums_empty_creation(empty_sums: StaticUniversalMinStack) -> None:
    assert empty_sums.is_empty()
    assert empty_sums._top == -1
    assert empty_sums._min_top == -1


def test_sums_creation_with_args(filled_sums: StaticUniversalMinStack) -> None:
    assert filled_sums._top == 4
    assert filled_sums.peek() == 8


def test_sums_creation_no_args_no_capacity() -> None:
    with pytest.raises(TypeError):
        StaticUniversalMinStack()


def test_sums_creation_invalid_capacity() -> None:
    with pytest.raises(TypeError):
        StaticUniversalMinStack(capacity="hello")


def test_sums_creation_overflow() -> None:
    with pytest.raises(OverflowError):
        StaticUniversalMinStack(1, 2, 3, capacity=2)


def test_sums_creation_invalid_key() -> None:
    with pytest.raises(TypeError):
        StaticUniversalMinStack(capacity=5, key="not_callable")  # type: ignore[union-attr]


# -------------- Push Tests ----------------
def test_sums_push(empty_sums: StaticUniversalMinStack) -> None:
    empty_sums.push(42)
    assert empty_sums.peek() == 42
    assert empty_sums._top == 0


def test_sums_push_full(filled_sums: StaticUniversalMinStack) -> None:
    s = StaticUniversalMinStack(1, 2, 3, capacity=3)
    with pytest.raises(OverflowError):
        s.push(99)


# -------------- Pop Tests ----------------
def test_sums_pop(filled_sums: StaticUniversalMinStack) -> None:
    value = filled_sums.pop()
    assert value == 8
    assert filled_sums._top == 3


def test_sums_pop_empty(empty_sums: StaticUniversalMinStack) -> None:
    with pytest.raises(IndexError):
        empty_sums.pop()


def test_sums_pop_updates_min(filled_sums: StaticUniversalMinStack) -> None:
    # stack: [5, 3, 7, 1, 8], min=1
    filled_sums.pop()  # remove 8, min still 1
    assert filled_sums.get_min() == 1
    filled_sums.pop()  # remove 1, min becomes 3
    assert filled_sums.get_min() == 3


# -------------- Peek Tests ----------------
def test_sums_peek(filled_sums: StaticUniversalMinStack) -> None:
    assert filled_sums.peek() == 8
    assert filled_sums._top == 4


def test_sums_peek_empty(empty_sums: StaticUniversalMinStack) -> None:
    with pytest.raises(IndexError):
        empty_sums.peek()


# -------------- get_min Tests ----------------
def test_sums_get_min(filled_sums: StaticUniversalMinStack) -> None:
    assert filled_sums.get_min() == 1


def test_sums_get_min_empty(empty_sums: StaticUniversalMinStack) -> None:
    with pytest.raises(IndexError):
        empty_sums.get_min()


def test_sums_get_min_with_key(key_sums: StaticUniversalMinStack) -> None:
    assert key_sums.get_min() == "hi"  # len=2, shortest


def test_sums_get_min_stays_correct_after_pop() -> None:
    s = StaticUniversalMinStack(5, 1, 3, capacity=5)
    assert s.get_min() == 1
    s.pop()  # remove 3
    assert s.get_min() == 1
    s.pop()  # remove 1
    assert s.get_min() == 5


# -------------- copy Tests ----------------
def test_sums_copy(filled_sums: StaticUniversalMinStack) -> None:
    copied = filled_sums.copy()
    assert copied == filled_sums


def test_sums_copy_independent(filled_sums: StaticUniversalMinStack) -> None:
    copied = filled_sums.copy()
    copied.push(99)
    assert filled_sums.peek() == 8


def test_sums_copy_preserves_min(filled_sums: StaticUniversalMinStack) -> None:
    copied = filled_sums.copy()
    assert copied.get_min() == filled_sums.get_min()


# -------------- __eq__ Tests ----------------
def test_sums_eq(filled_sums: StaticUniversalMinStack) -> None:
    other = StaticUniversalMinStack(5, 3, 7, 1, 8, capacity=10)
    assert filled_sums == other


def test_sums_eq_different(filled_sums: StaticUniversalMinStack) -> None:
    other = StaticUniversalMinStack(1, 2, 3, capacity=10)
    assert filled_sums != other


# -------------- __iter__ Tests ----------------
def test_sums_iter(filled_sums: StaticUniversalMinStack) -> None:
    assert list(filled_sums) == [8, 1, 7, 3, 5]


def test_sums_iter_empty(empty_sums: StaticUniversalMinStack) -> None:
    assert list(empty_sums) == []


# -------------- __repr__ Tests ----------------
def test_sums_repr(filled_sums: StaticUniversalMinStack) -> None:
    assert repr(filled_sums).startswith("StaticUniversalMinStack")


# ═══════════════════════════════════════════════
# StaticTypedMinStack
# ═══════════════════════════════════════════════


@pytest.fixture
def empty_stms() -> StaticTypedMinStack:
    return StaticTypedMinStack(dtype=int, capacity=10)


@pytest.fixture
def filled_stms() -> StaticTypedMinStack:
    return StaticTypedMinStack(5, 3, 7, 1, 8, dtype=int, capacity=10)


# -------------- Creation Tests ----------------
def test_stms_empty_creation(empty_stms: StaticTypedMinStack) -> None:
    assert empty_stms.is_empty()
    assert empty_stms._top == -1
    assert empty_stms._min_top == -1


def test_stms_creation_with_args(filled_stms: StaticTypedMinStack) -> None:
    assert filled_stms._top == 4
    assert filled_stms.peek() == 8


def test_stms_creation_wrong_type() -> None:
    with pytest.raises(TypeError):
        StaticTypedMinStack(1, 2, "hello", dtype=int)


def test_stms_creation_overflow() -> None:
    with pytest.raises(OverflowError):
        StaticTypedMinStack(1, 2, 3, dtype=int, capacity=2)


# -------------- Push Tests ----------------
def test_stms_push(empty_stms: StaticTypedMinStack) -> None:
    empty_stms.push(42)
    assert empty_stms.peek() == 42


def test_stms_push_wrong_type(empty_stms: StaticTypedMinStack) -> None:
    with pytest.raises(TypeError):
        empty_stms.push("hello")


def test_stms_push_full() -> None:
    s = StaticTypedMinStack(1, 2, 3, dtype=int, capacity=3)
    with pytest.raises(OverflowError):
        s.push(99)


# -------------- Pop Tests ----------------
def test_stms_pop(filled_stms: StaticTypedMinStack) -> None:
    value = filled_stms.pop()
    assert value == 8


def test_stms_pop_resets_slot(filled_stms: StaticTypedMinStack) -> None:
    filled_stms.pop()
    assert filled_stms._main_data[4] == 0


def test_stms_pop_empty(empty_stms: StaticTypedMinStack) -> None:
    with pytest.raises(IndexError):
        empty_stms.pop()


def test_stms_pop_updates_min() -> None:
    s = StaticTypedMinStack(5, 1, 3, dtype=int, capacity=5)
    assert s.get_min() == 1
    s.pop()  # remove 3
    assert s.get_min() == 1
    s.pop()  # remove 1
    assert s.get_min() == 5


# -------------- get_min Tests ----------------
def test_stms_get_min(filled_stms: StaticTypedMinStack) -> None:
    assert filled_stms.get_min() == 1


def test_stms_get_min_empty(empty_stms: StaticTypedMinStack) -> None:
    with pytest.raises(IndexError):
        empty_stms.get_min()


# -------------- copy Tests ----------------
def test_stms_copy(filled_stms: StaticTypedMinStack) -> None:
    copied = filled_stms.copy()
    assert copied == filled_stms


def test_stms_copy_independent(filled_stms: StaticTypedMinStack) -> None:
    copied = filled_stms.copy()
    copied.push(99)
    assert filled_stms.peek() == 8


# -------------- __iter__ Tests ----------------
def test_stms_iter(filled_stms: StaticTypedMinStack) -> None:
    assert list(filled_stms) == [8, 1, 7, 3, 5]


def test_stms_iter_empty(empty_stms: StaticTypedMinStack) -> None:
    assert list(empty_stms) == []


# -------------- __repr__ Tests ----------------
def test_stms_repr(filled_stms: StaticTypedMinStack) -> None:
    assert repr(filled_stms).startswith("StaticTypedMinStack")


# ═══════════════════════════════════════════════
# DynamicUniversalMinStack
# ═══════════════════════════════════════════════


@pytest.fixture
def empty_dums() -> DynamicUniversalMinStack:
    return DynamicUniversalMinStack()


@pytest.fixture
def filled_dums() -> DynamicUniversalMinStack:
    return DynamicUniversalMinStack(5, 3, 7, 1, 8)


@pytest.fixture
def key_dums() -> DynamicUniversalMinStack:
    return DynamicUniversalMinStack("hello", "hi", "hey", key=len)


# -------------- Creation Tests ----------------
def test_dums_empty_creation(empty_dums: DynamicUniversalMinStack) -> None:
    assert empty_dums.is_empty()
    assert len(empty_dums) == 0


def test_dums_creation_with_args(filled_dums: DynamicUniversalMinStack) -> None:
    assert len(filled_dums) == 5
    assert filled_dums.peek() == 8


def test_dums_creation_invalid_key() -> None:
    with pytest.raises(TypeError):
        DynamicUniversalMinStack(key="not_callable")  # type: ignore[union-attr]


# -------------- Push Tests ----------------
def test_dums_push(empty_dums: DynamicUniversalMinStack) -> None:
    empty_dums.push(42)
    assert empty_dums.peek() == 42
    assert len(empty_dums) == 1


def test_dums_push_grows(empty_dums: DynamicUniversalMinStack) -> None:
    for i in range(100):
        empty_dums.push(i)
    assert len(empty_dums) == 100


# -------------- Pop Tests ----------------
def test_dums_pop(filled_dums: DynamicUniversalMinStack) -> None:
    value = filled_dums.pop()
    assert value == 8
    assert len(filled_dums) == 4


def test_dums_pop_empty(empty_dums: DynamicUniversalMinStack) -> None:
    with pytest.raises(IndexError):
        empty_dums.pop()


def test_dums_pop_updates_min() -> None:
    s = DynamicUniversalMinStack(5, 1, 3)
    assert s.get_min() == 1
    s.pop()
    assert s.get_min() == 1
    s.pop()
    assert s.get_min() == 5


# -------------- get_min Tests ----------------
def test_dums_get_min(filled_dums: DynamicUniversalMinStack) -> None:
    assert filled_dums.get_min() == 1


def test_dums_get_min_empty(empty_dums: DynamicUniversalMinStack) -> None:
    with pytest.raises(IndexError):
        empty_dums.get_min()


def test_dums_get_min_with_key(key_dums: DynamicUniversalMinStack) -> None:
    assert key_dums.get_min() == "hi"


# -------------- copy Tests ----------------
def test_dums_copy(filled_dums: DynamicUniversalMinStack) -> None:
    copied = filled_dums.copy()
    assert copied == filled_dums


def test_dums_copy_independent(filled_dums: DynamicUniversalMinStack) -> None:
    copied = filled_dums.copy()
    copied.push(99)
    assert filled_dums.peek() == 8


def test_dums_copy_preserves_min(filled_dums: DynamicUniversalMinStack) -> None:
    copied = filled_dums.copy()
    assert copied.get_min() == filled_dums.get_min()


# -------------- __iter__ Tests ----------------
def test_dums_iter(filled_dums: DynamicUniversalMinStack) -> None:
    assert list(filled_dums) == [8, 1, 7, 3, 5]


def test_dums_iter_empty(empty_dums: DynamicUniversalMinStack) -> None:
    assert list(empty_dums) == []


# -------------- __repr__ Tests ----------------
def test_dums_repr(filled_dums: DynamicUniversalMinStack) -> None:
    assert repr(filled_dums).startswith("DynamicUniversalMinStack")


# ═══════════════════════════════════════════════
# DynamicTypedMinStack
# ═══════════════════════════════════════════════


@pytest.fixture
def empty_dtms() -> DynamicTypedMinStack:
    return DynamicTypedMinStack(dtype=int)


@pytest.fixture
def filled_dtms() -> DynamicTypedMinStack:
    return DynamicTypedMinStack(5, 3, 7, 1, 8, dtype=int)


# -------------- Creation Tests ----------------
def test_dtms_empty_creation(empty_dtms: DynamicTypedMinStack) -> None:
    assert empty_dtms.is_empty()
    assert len(empty_dtms) == 0


def test_dtms_creation_with_args(filled_dtms: DynamicTypedMinStack) -> None:
    assert len(filled_dtms) == 5
    assert filled_dtms.peek() == 8


def test_dtms_creation_wrong_type() -> None:
    with pytest.raises(TypeError):
        DynamicTypedMinStack(1, 2, "hello", dtype=int)


# -------------- Push Tests ----------------
def test_dtms_push(empty_dtms: DynamicTypedMinStack) -> None:
    empty_dtms.push(42)
    assert empty_dtms.peek() == 42


def test_dtms_push_wrong_type(empty_dtms: DynamicTypedMinStack) -> None:
    with pytest.raises(TypeError):
        empty_dtms.push("hello")


def test_dtms_push_grows(empty_dtms: DynamicTypedMinStack) -> None:
    for i in range(100):
        empty_dtms.push(i)
    assert len(empty_dtms) == 100


# -------------- Pop Tests ----------------
def test_dtms_pop(filled_dtms: DynamicTypedMinStack) -> None:
    value = filled_dtms.pop()
    assert value == 8
    assert len(filled_dtms) == 4


def test_dtms_pop_empty(empty_dtms: DynamicTypedMinStack) -> None:
    with pytest.raises(IndexError):
        empty_dtms.pop()


def test_dtms_pop_updates_min() -> None:
    s = DynamicTypedMinStack(5, 1, 3, dtype=int)
    assert s.get_min() == 1
    s.pop()
    assert s.get_min() == 1
    s.pop()
    assert s.get_min() == 5


# -------------- get_min Tests ----------------
def test_dtms_get_min(filled_dtms: DynamicTypedMinStack) -> None:
    assert filled_dtms.get_min() == 1


def test_dtms_get_min_empty(empty_dtms: DynamicTypedMinStack) -> None:
    with pytest.raises(IndexError):
        empty_dtms.get_min()


# -------------- copy Tests ----------------
def test_dtms_copy(filled_dtms: DynamicTypedMinStack) -> None:
    copied = filled_dtms.copy()
    assert copied == filled_dtms


def test_dtms_copy_independent(filled_dtms: DynamicTypedMinStack) -> None:
    copied = filled_dtms.copy()
    copied.push(99)
    assert filled_dtms.peek() == 8


# -------------- __eq__ Tests ----------------
def test_dtms_eq_different_dtype() -> None:
    s1 = DynamicTypedMinStack(1, dtype=int)
    s2 = DynamicTypedMinStack(dtype=float)
    s2.push(1.0)
    assert s1 != s2


# -------------- __iter__ Tests ----------------
def test_dtms_iter(filled_dtms: DynamicTypedMinStack) -> None:
    assert list(filled_dtms) == [8, 1, 7, 3, 5]


def test_dtms_iter_empty(empty_dtms: DynamicTypedMinStack) -> None:
    assert list(empty_dtms) == []


# -------------- __repr__ Tests ----------------
def test_dtms_repr(filled_dtms: DynamicTypedMinStack) -> None:
    assert repr(filled_dtms).startswith("DynamicTypedMinStack")


# ═══════════════════════════════════════════════
# DynamicNodeMinStack
# ═══════════════════════════════════════════════


@pytest.fixture
def empty_dnms() -> DynamicNodeMinStack:
    return DynamicNodeMinStack()


@pytest.fixture
def filled_dnms() -> DynamicNodeMinStack:
    return DynamicNodeMinStack(5, 3, 7, 1, 8)


@pytest.fixture
def key_dnms() -> DynamicNodeMinStack:
    return DynamicNodeMinStack("hello", "hi", "hey", key=len)


# -------------- Creation Tests ----------------
def test_dnms_empty_creation(empty_dnms: DynamicNodeMinStack) -> None:
    assert empty_dnms.is_empty()
    assert len(empty_dnms) == 0
    assert empty_dnms._main_head is None
    assert empty_dnms._min_head is None


def test_dnms_creation_with_args(filled_dnms: DynamicNodeMinStack) -> None:
    assert len(filled_dnms) == 5
    assert filled_dnms.peek() == 8
    assert filled_dnms._main_head.value == 8  # type: ignore[union-attr]


def test_dnms_creation_invalid_key() -> None:
    with pytest.raises(TypeError):
        DynamicNodeMinStack(key="not_callable")  # type: ignore[union-attr]


# -------------- Push Tests ----------------
def test_dnms_push(empty_dnms: DynamicNodeMinStack) -> None:
    empty_dnms.push(42)
    assert empty_dnms.peek() == 42
    assert len(empty_dnms) == 1
    assert empty_dnms._main_head.value == 42  # type: ignore[union-attr]


def test_dnms_push_updates_min_head() -> None:
    s = DynamicNodeMinStack()
    s.push(5)
    assert s._min_head.value == 5  # type: ignore[union-attr]
    s.push(3)
    assert s._min_head.value == 3  # type: ignore[union-attr]
    s.push(7)
    assert s._min_head.value == 3  # type: ignore[union-attr]


def test_dnms_push_any_type(empty_dnms: DynamicNodeMinStack) -> None:
    empty_dnms._key = len
    empty_dnms.push("hello")
    empty_dnms.push([1, 2])
    assert len(empty_dnms) == 2


# -------------- Pop Tests ----------------
def test_dnms_pop(filled_dnms: DynamicNodeMinStack) -> None:
    value = filled_dnms.pop()
    assert value == 8
    assert len(filled_dnms) == 4
    assert filled_dnms._main_head.value == 1  # type: ignore[union-attr]


def test_dnms_pop_empty(empty_dnms: DynamicNodeMinStack) -> None:
    with pytest.raises(IndexError):
        empty_dnms.pop()


def test_dnms_pop_updates_min() -> None:
    s = DynamicNodeMinStack(5, 1, 3)
    assert s.get_min() == 1
    s.pop()  # remove 3
    assert s.get_min() == 1
    s.pop()  # remove 1
    assert s.get_min() == 5


def test_dnms_pop_until_empty(filled_dnms: DynamicNodeMinStack) -> None:
    for _ in range(5):
        filled_dnms.pop()
    assert filled_dnms.is_empty()
    assert filled_dnms._main_head is None
    assert filled_dnms._min_head is None


# -------------- Peek Tests ----------------
def test_dnms_peek(filled_dnms: DynamicNodeMinStack) -> None:
    assert filled_dnms.peek() == 8
    assert len(filled_dnms) == 5


def test_dnms_peek_empty(empty_dnms: DynamicNodeMinStack) -> None:
    with pytest.raises(IndexError):
        empty_dnms.peek()


# -------------- get_min Tests ----------------
def test_dnms_get_min(filled_dnms: DynamicNodeMinStack) -> None:
    assert filled_dnms.get_min() == 1


def test_dnms_get_min_empty(empty_dnms: DynamicNodeMinStack) -> None:
    with pytest.raises(IndexError):
        empty_dnms.get_min()


def test_dnms_get_min_with_key(key_dnms: DynamicNodeMinStack) -> None:
    assert key_dnms.get_min() == "hi"


def test_dnms_get_min_stays_correct() -> None:
    s = DynamicNodeMinStack(5, 1, 3)
    assert s.get_min() == 1
    s.pop()
    assert s.get_min() == 1
    s.pop()
    assert s.get_min() == 5


# -------------- copy Tests ----------------
def test_dnms_copy(filled_dnms: DynamicNodeMinStack) -> None:
    copied = filled_dnms.copy()
    assert copied == filled_dnms


def test_dnms_copy_independent(filled_dnms: DynamicNodeMinStack) -> None:
    copied = filled_dnms.copy()
    copied.push(99)
    assert filled_dnms.peek() == 8


def test_dnms_copy_preserves_min(filled_dnms: DynamicNodeMinStack) -> None:
    copied = filled_dnms.copy()
    assert copied.get_min() == filled_dnms.get_min()


def test_dnms_copy_preserves_order(filled_dnms: DynamicNodeMinStack) -> None:
    copied = filled_dnms.copy()
    assert list(copied) == list(filled_dnms)


# -------------- __eq__ Tests ----------------
def test_dnms_eq(filled_dnms: DynamicNodeMinStack) -> None:
    other = DynamicNodeMinStack(5, 3, 7, 1, 8)
    assert filled_dnms == other


def test_dnms_eq_different(filled_dnms: DynamicNodeMinStack) -> None:
    other = DynamicNodeMinStack(1, 2, 3)
    assert filled_dnms != other


# -------------- __iter__ Tests ----------------
def test_dnms_iter(filled_dnms: DynamicNodeMinStack) -> None:
    assert list(filled_dnms) == [8, 1, 7, 3, 5]


def test_dnms_iter_empty(empty_dnms: DynamicNodeMinStack) -> None:
    assert list(empty_dnms) == []


def test_dnms_iter_does_not_modify(filled_dnms: DynamicNodeMinStack) -> None:
    list(filled_dnms)
    assert len(filled_dnms) == 5
    assert filled_dnms.peek() == 8


# -------------- __repr__ Tests ----------------
def test_dnms_repr(filled_dnms: DynamicNodeMinStack) -> None:
    assert repr(filled_dnms).startswith("DynamicNodeMinStack")
