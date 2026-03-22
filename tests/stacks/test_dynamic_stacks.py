import pytest

from data_structures.stacks import (
    DynamicNodeStack,
    DynamicTypedStack,
    DynamicUniversalStack,
)

# ═══════════════════════════════════════════════
# DynamicUniversalStack
# ═══════════════════════════════════════════════


@pytest.fixture
def empty_dus() -> DynamicUniversalStack:
    return DynamicUniversalStack()


@pytest.fixture
def filled_dus() -> DynamicUniversalStack:
    return DynamicUniversalStack(1, 2, 3, 4, 5)


# -------------- Creation Tests ----------------


def test_dus_empty_creation(empty_dus: DynamicUniversalStack) -> None:
    assert len(empty_dus) == 0
    assert empty_dus.is_empty()


def test_dus_creation_with_args(filled_dus: DynamicUniversalStack) -> None:
    assert len(filled_dus) == 5
    assert filled_dus.peek() == 5


# -------------- Push Tests ----------------


def test_dus_push(empty_dus: DynamicUniversalStack) -> None:
    empty_dus.push(42)
    assert empty_dus.peek() == 42
    assert len(empty_dus) == 1


def test_dus_push_any_type(empty_dus: DynamicUniversalStack) -> None:
    empty_dus.push("hello")
    empty_dus.push([1, 2])
    empty_dus.push(None)
    assert len(empty_dus) == 3


def test_dus_push_grows(empty_dus: DynamicUniversalStack) -> None:
    for i in range(100):
        empty_dus.push(i)
    assert len(empty_dus) == 100
    assert empty_dus.peek() == 99


# -------------- Pop Tests ----------------


def test_dus_pop(filled_dus: DynamicUniversalStack) -> None:
    value = filled_dus.pop()
    assert value == 5
    assert len(filled_dus) == 4


def test_dus_pop_empty(empty_dus: DynamicUniversalStack) -> None:
    with pytest.raises(IndexError):
        empty_dus.pop()


def test_dus_pop_until_empty(filled_dus: DynamicUniversalStack) -> None:
    for _ in range(5):
        filled_dus.pop()
    assert filled_dus.is_empty()


# -------------- Peek Tests ----------------


def test_dus_peek(filled_dus: DynamicUniversalStack) -> None:
    assert filled_dus.peek() == 5
    assert len(filled_dus) == 5


def test_dus_peek_empty(empty_dus: DynamicUniversalStack) -> None:
    with pytest.raises(IndexError):
        empty_dus.peek()


# -------------- copy Tests ----------------


def test_dus_copy(filled_dus: DynamicUniversalStack) -> None:
    copied = filled_dus.copy()
    assert copied == filled_dus


def test_dus_copy_independent(filled_dus: DynamicUniversalStack) -> None:
    copied = filled_dus.copy()
    copied.push(99)
    assert filled_dus.peek() == 5


# -------------- __eq__ Tests ----------------


def test_dus_eq(filled_dus: DynamicUniversalStack) -> None:
    other = DynamicUniversalStack(1, 2, 3, 4, 5)
    assert filled_dus == other


def test_dus_eq_different(filled_dus: DynamicUniversalStack) -> None:
    other = DynamicUniversalStack(1, 2, 3)
    assert filled_dus != other


# -------------- __iter__ Tests ----------------


def test_dus_iter(filled_dus: DynamicUniversalStack) -> None:
    assert list(filled_dus) == [5, 4, 3, 2, 1]


def test_dus_iter_empty(empty_dus: DynamicUniversalStack) -> None:
    assert list(empty_dus) == []


# ═══════════════════════════════════════════════
# DynamicTypedStack
# ═══════════════════════════════════════════════


@pytest.fixture
def empty_dts() -> DynamicTypedStack:
    return DynamicTypedStack(dtype=int)


@pytest.fixture
def filled_dts() -> DynamicTypedStack:
    return DynamicTypedStack(1, 2, 3, 4, 5, dtype=int)


# -------------- Creation Tests ----------------


def test_dts_empty_creation(empty_dts: DynamicTypedStack) -> None:
    assert len(empty_dts) == 0
    assert empty_dts.is_empty()


def test_dts_creation_with_args(filled_dts: DynamicTypedStack) -> None:
    assert len(filled_dts) == 5
    assert filled_dts.peek() == 5


def test_dts_creation_wrong_type() -> None:
    with pytest.raises(TypeError):
        DynamicTypedStack(1, 2, "hello", dtype=int)


# -------------- Push Tests ----------------


def test_dts_push(empty_dts: DynamicTypedStack) -> None:
    empty_dts.push(42)
    assert empty_dts.peek() == 42
    assert len(empty_dts) == 1


def test_dts_push_wrong_type(empty_dts: DynamicTypedStack) -> None:
    with pytest.raises(TypeError):
        empty_dts.push("hello")


def test_dts_push_grows(empty_dts: DynamicTypedStack) -> None:
    for i in range(100):
        empty_dts.push(i)
    assert len(empty_dts) == 100
    assert empty_dts.peek() == 99


# -------------- Pop Tests ----------------


def test_dts_pop(filled_dts: DynamicTypedStack) -> None:
    value = filled_dts.pop()
    assert value == 5
    assert len(filled_dts) == 4


def test_dts_pop_empty(empty_dts: DynamicTypedStack) -> None:
    with pytest.raises(IndexError):
        empty_dts.pop()


# -------------- Peek Tests ----------------


def test_dts_peek(filled_dts: DynamicTypedStack) -> None:
    assert filled_dts.peek() == 5
    assert len(filled_dts) == 5


def test_dts_peek_empty(empty_dts: DynamicTypedStack) -> None:
    with pytest.raises(IndexError):
        empty_dts.peek()


# -------------- copy Tests ----------------


def test_dts_copy(filled_dts: DynamicTypedStack) -> None:
    copied = filled_dts.copy()
    assert copied == filled_dts


def test_dts_copy_independent(filled_dts: DynamicTypedStack) -> None:
    copied = filled_dts.copy()
    copied.push(99)
    assert filled_dts.peek() == 5


# -------------- __eq__ Tests ----------------


def test_dts_eq(filled_dts: DynamicTypedStack) -> None:
    other = DynamicTypedStack(1, 2, 3, 4, 5, dtype=int)
    assert filled_dts == other


def test_dts_eq_different_dtype() -> None:
    s1 = DynamicTypedStack(1, dtype=int)
    s2 = DynamicTypedStack(dtype=float)
    s2.push(1.0)
    assert s1 != s2


# -------------- __iter__ Tests ----------------


def test_dts_iter(filled_dts: DynamicTypedStack) -> None:
    assert list(filled_dts) == [5, 4, 3, 2, 1]


def test_dts_iter_empty(empty_dts: DynamicTypedStack) -> None:
    assert list(empty_dts) == []


# ═══════════════════════════════════════════════
# DynamicNodeStack
# ═══════════════════════════════════════════════


@pytest.fixture
def empty_dns() -> DynamicNodeStack:
    return DynamicNodeStack()


@pytest.fixture
def filled_dns() -> DynamicNodeStack:
    return DynamicNodeStack(1, 2, 3, 4, 5)


# -------------- Creation Tests ----------------


def test_dns_empty_creation(empty_dns: DynamicNodeStack) -> None:
    assert len(empty_dns) == 0
    assert empty_dns.is_empty()
    assert empty_dns._head is None


def test_dns_creation_with_args(filled_dns: DynamicNodeStack) -> None:
    assert len(filled_dns) == 5
    assert filled_dns.peek() == 5
    assert filled_dns._head.value == 5  # type: ignore[attr-name]


# -------------- Push Tests ----------------


def test_dns_push(empty_dns: DynamicNodeStack) -> None:
    empty_dns.push(42)
    assert empty_dns.peek() == 42
    assert len(empty_dns) == 1
    assert empty_dns._head.value == 42  # type: ignore[attr-name]


def test_dns_push_links(empty_dns: DynamicNodeStack) -> None:
    empty_dns.push(1)
    empty_dns.push(2)
    assert empty_dns._head.value == 2  # type: ignore[attr-name]
    assert empty_dns._head.next.value == 1  # type: ignore[attr-name]


def test_dns_push_any_type(empty_dns: DynamicNodeStack) -> None:
    empty_dns.push("hello")
    empty_dns.push([1, 2])
    assert len(empty_dns) == 2


# -------------- Pop Tests ----------------


def test_dns_pop(filled_dns: DynamicNodeStack) -> None:
    value = filled_dns.pop()
    assert value == 5
    assert len(filled_dns) == 4
    assert filled_dns._head.value == 4  # type: ignore[attr-name]


def test_dns_pop_empty(empty_dns: DynamicNodeStack) -> None:
    with pytest.raises(IndexError):
        empty_dns.pop()


def test_dns_pop_until_empty(filled_dns: DynamicNodeStack) -> None:
    for _ in range(5):
        filled_dns.pop()
    assert filled_dns.is_empty()
    assert filled_dns._head is None


# -------------- Peek Tests ----------------


def test_dns_peek(filled_dns: DynamicNodeStack) -> None:
    assert filled_dns.peek() == 5
    assert len(filled_dns) == 5


def test_dns_peek_empty(empty_dns: DynamicNodeStack) -> None:
    with pytest.raises(IndexError):
        empty_dns.peek()


# -------------- copy Tests ----------------


def test_dns_copy(filled_dns: DynamicNodeStack) -> None:
    copied = filled_dns.copy()
    assert copied == filled_dns


def test_dns_copy_independent(filled_dns: DynamicNodeStack) -> None:
    copied = filled_dns.copy()
    copied.push(99)
    assert filled_dns.peek() == 5


def test_dns_copy_order(filled_dns: DynamicNodeStack) -> None:
    copied = filled_dns.copy()
    assert list(copied) == list(filled_dns)


# -------------- __eq__ Tests ----------------


def test_dns_eq(filled_dns: DynamicNodeStack) -> None:
    other = DynamicNodeStack(1, 2, 3, 4, 5)
    assert filled_dns == other


def test_dns_eq_different(filled_dns: DynamicNodeStack) -> None:
    other = DynamicNodeStack(1, 2, 3)
    assert filled_dns != other


# -------------- __iter__ Tests ----------------


def test_dns_iter(filled_dns: DynamicNodeStack) -> None:
    assert list(filled_dns) == [5, 4, 3, 2, 1]


def test_dns_iter_empty(empty_dns: DynamicNodeStack) -> None:
    assert list(empty_dns) == []


def test_dns_iter_does_not_modify(filled_dns: DynamicNodeStack) -> None:
    list(filled_dns)
    assert len(filled_dns) == 5
    assert filled_dns.peek() == 5


# -------------- __repr__ Tests ----------------


def test_dns_repr(filled_dns: DynamicNodeStack) -> None:
    assert repr(filled_dns).startswith("DynamicNodeStack")
