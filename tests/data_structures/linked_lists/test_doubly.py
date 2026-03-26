import pytest

from data_structures.linked_lists import DoublyLinkedList


class TestDoublyLinkedListInit:
    def test_empty_list(self):
        lst = DoublyLinkedList()
        assert len(lst) == 0
        assert lst._head is None
        assert lst._tail is None

    def test_single_element(self):
        lst = DoublyLinkedList(42)
        assert len(lst) == 1
        assert lst._head is lst._tail
        assert lst._head.value == 42  # type: ignore[union-attr]
        assert lst._head.next is None  # type: ignore[union-attr]
        assert lst._head.prev is None  # type: ignore[union-attr]

    def test_multiple_elements(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert len(lst) == 3
        assert list(lst) == [1, 2, 3]

    def test_head_and_tail_values(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert lst._head.value == 1  # type: ignore[union-attr]
        assert lst._tail.value == 3  # type: ignore[union-attr]

    def test_head_prev_is_none(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert lst._head.prev is None  # type: ignore[union-attr]

    def test_tail_next_is_none(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert lst._tail.next is None  # type: ignore[union-attr]

    def test_bidirectional_links(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert lst._head.next.prev is lst._head  # type: ignore[union-attr]
        assert lst._tail.prev.next is lst._tail  # type: ignore[union-attr]


class TestDoublyLinkedListAppend:
    def test_append_to_empty(self):
        lst = DoublyLinkedList()
        lst.append(1)
        assert lst._head is lst._tail
        assert lst._head.value == 1  # type: ignore[union-attr]
        assert lst._head.next is None  # type: ignore[union-attr]
        assert lst._head.prev is None  # type: ignore[union-attr]

    def test_append_updates_tail(self):
        lst = DoublyLinkedList(1, 2)
        lst.append(3)
        assert lst._tail.value == 3  # type: ignore[union-attr]
        assert lst._tail.next is None  # type: ignore[union-attr]

    def test_append_links_prev(self):
        lst = DoublyLinkedList(1)
        lst.append(2)
        assert lst._tail.prev is lst._head  # type: ignore[union-attr]

    def test_append_does_not_change_head(self):
        lst = DoublyLinkedList(1)
        lst.append(2)
        assert lst._head.value == 1  # type: ignore[union-attr]


class TestDoublyLinkedListPrepend:
    def test_prepend_to_empty(self):
        lst = DoublyLinkedList()
        lst.prepend(1)
        assert lst._head is lst._tail
        assert lst._head.value == 1  # type: ignore[union-attr]
        assert lst._head.prev is None  # type: ignore[union-attr]
        assert lst._head.next is None  # type: ignore[union-attr]

    def test_prepend_updates_head(self):
        lst = DoublyLinkedList(2, 3)
        lst.prepend(1)
        assert lst._head.value == 1  # type: ignore[union-attr]
        assert list(lst) == [1, 2, 3]

    def test_prepend_links_next(self):
        lst = DoublyLinkedList(2)
        lst.prepend(1)
        assert lst._head.next is lst._tail  # type: ignore[union-attr]
        assert lst._tail.prev is lst._head  # type: ignore[union-attr]

    def test_prepend_does_not_change_tail(self):
        lst = DoublyLinkedList(2, 3)
        lst.prepend(1)
        assert lst._tail.value == 3  # type: ignore[union-attr]


class TestDoublyLinkedListInsert:
    def test_insert_at_beginning(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.insert(0, 0)
        assert list(lst) == [0, 1, 2, 3]
        assert lst._head.value == 0  # type: ignore[union-attr]

    def test_insert_at_end(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.insert(3, 4)
        assert list(lst) == [1, 2, 3, 4]
        assert lst._tail.value == 4  # type: ignore[union-attr]

    def test_insert_in_middle(self):
        lst = DoublyLinkedList(1, 2, 4)
        lst.insert(2, 3)
        assert list(lst) == [1, 2, 3, 4]

    def test_insert_bidirectional_links(self):
        lst = DoublyLinkedList(1, 3)
        lst.insert(1, 2)
        mid = lst._head.next  # type: ignore[union-attr]
        assert mid.value == 2  # type: ignore[union-attr]
        assert mid.prev is lst._head  # type: ignore[union-attr]
        assert mid.next is lst._tail  # type: ignore[union-attr]

    def test_insert_negative_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.insert(-1, 99)
        assert list(lst) == [1, 2, 99, 3]

    def test_insert_out_of_range_raises(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst.insert(10, 99)

    def test_insert_bool_index_raises(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst.insert(True, 99)  # type: ignore[arg-type]

    def test_insert_preserves_head_prev_none(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.insert(0, 0)
        assert lst._head.prev is None  # type: ignore[union-attr]

    def test_insert_preserves_tail_next_none(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.insert(3, 4)
        assert lst._tail.next is None  # type: ignore[union-attr]


class TestDoublyLinkedListRemove:
    def test_remove_head(self):
        lst = DoublyLinkedList(1, 2, 3)
        val = lst.remove(0)
        assert val == 1
        assert list(lst) == [2, 3]
        assert lst._head.value == 2  # type: ignore[union-attr]
        assert lst._head.prev is None  # type: ignore[union-attr]

    def test_remove_tail(self):
        lst = DoublyLinkedList(1, 2, 3)
        val = lst.remove(2)
        assert val == 3
        assert list(lst) == [1, 2]
        assert lst._tail.value == 2  # type: ignore[union-attr]
        assert lst._tail.next is None  # type: ignore[union-attr]

    def test_remove_middle(self):
        lst = DoublyLinkedList(1, 2, 3)
        val = lst.remove(1)
        assert val == 2
        assert list(lst) == [1, 3]
        assert lst._head.next is lst._tail  # type: ignore[union-attr]
        assert lst._tail.prev is lst._head  # type: ignore[union-attr]

    def test_remove_only_element(self):
        lst = DoublyLinkedList(42)
        val = lst.remove(0)
        assert val == 42
        assert lst._head is None
        assert lst._tail is None
        assert len(lst) == 0

    def test_remove_negative_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        val = lst.remove(-1)
        assert val == 3
        assert list(lst) == [1, 2]

    def test_remove_from_empty_raises(self):
        lst = DoublyLinkedList()
        with pytest.raises(IndexError):
            lst.remove(0)

    def test_remove_out_of_range_raises(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst.remove(10)

    def test_remove_decrements_size(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.remove(1)
        assert len(lst) == 2


class TestDoublyLinkedListGetSetItem:
    def test_getitem_positive(self):
        lst = DoublyLinkedList(10, 20, 30)
        assert lst[0] == 10
        assert lst[1] == 20
        assert lst[2] == 30

    def test_getitem_negative(self):
        lst = DoublyLinkedList(10, 20, 30)
        assert lst[-1] == 30
        assert lst[-3] == 10

    def test_getitem_out_of_range_raises(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            _ = lst[3]

    def test_getitem_bool_index_raises(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            _ = lst[True]  # type: ignore[index]

    def test_setitem_positive(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst[1] = 99
        assert lst[1] == 99
        assert list(lst) == [1, 99, 3]

    def test_setitem_negative(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst[-1] = 99
        assert lst[2] == 99

    def test_setitem_out_of_range_raises(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst[5] = 99

    def test_setitem_does_not_change_size(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst[0] = 99
        assert len(lst) == 3


class TestDoublyLinkedListIterReversed:
    def test_iter_order(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert list(lst) == [1, 2, 3]

    def test_iter_empty(self):
        assert list(DoublyLinkedList()) == []

    def test_reversed_order(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert list(reversed(lst)) == [3, 2, 1]

    def test_reversed_empty(self):
        assert list(reversed(DoublyLinkedList())) == []

    def test_reversed_single(self):
        lst = DoublyLinkedList(42)
        assert list(reversed(lst)) == [42]

    def test_reversed_does_not_modify_list(self):
        lst = DoublyLinkedList(1, 2, 3)
        _ = list(reversed(lst))
        assert list(lst) == [1, 2, 3]


class TestDoublyLinkedListEq:
    def test_equal_lists(self):
        a = DoublyLinkedList(1, 2, 3)
        b = DoublyLinkedList(1, 2, 3)
        assert a == b

    def test_both_empty(self):
        assert DoublyLinkedList() == DoublyLinkedList()

    def test_different_middle(self):
        a = DoublyLinkedList(1, 2, 3)
        b = DoublyLinkedList(1, 9, 3)
        assert a != b

    def test_different_size(self):
        a = DoublyLinkedList(1, 2, 3)
        b = DoublyLinkedList(1, 2)
        assert a != b

    def test_different_head(self):
        a = DoublyLinkedList(1, 2, 3)
        b = DoublyLinkedList(9, 2, 3)
        assert a != b

    def test_different_tail(self):
        a = DoublyLinkedList(1, 2, 3)
        b = DoublyLinkedList(1, 2, 9)
        assert a != b

    def test_not_implemented_for_other_type(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert lst.__eq__([1, 2, 3]) is NotImplemented

    def test_with_none_values(self):
        a = DoublyLinkedList(1, None, 3)
        b = DoublyLinkedList(1, None, 3)
        assert a == b


class TestDoublyLinkedListRepr:
    def test_repr_empty(self):
        lst = DoublyLinkedList()
        assert repr(lst) == "DoublyLinkedList(size=0)[]"

    def test_repr_single(self):
        lst = DoublyLinkedList(1)
        assert repr(lst) == "DoublyLinkedList(size=1)[1]"

    def test_repr_multiple(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert repr(lst) == "DoublyLinkedList(size=3)[1 <-> 2 <-> 3]"
