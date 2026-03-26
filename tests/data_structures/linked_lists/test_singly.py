import pytest

from data_structures import SinglyLinkedList


class TestSinglyLinkedListInit:
    def test_empty_list(self):
        lst = SinglyLinkedList()
        assert len(lst) == 0
        assert lst._head is None
        assert lst._tail is None

    def test_single_element(self):
        lst = SinglyLinkedList(42)
        assert len(lst) == 1
        assert lst._head is lst._tail
        assert lst._head.value == 42  # type: ignore[union-attr]
        assert lst._head.next is None  # type: ignore[union-attr]

    def test_multiple_elements(self):
        lst = SinglyLinkedList(1, 2, 3)
        assert len(lst) == 3
        assert list(lst) == [1, 2, 3]

    def test_head_and_tail_on_single(self):
        lst = SinglyLinkedList(99)
        assert lst._head is lst._tail

    def test_head_and_tail_on_multiple(self):
        lst = SinglyLinkedList(1, 2, 3)
        assert lst._head.value == 1  # type: ignore[union-attr]
        assert lst._tail.value == 3  # type: ignore[union-attr]
        assert lst._tail.next is None  # type: ignore[union-attr]


class TestSinglyLinkedListAppend:
    def test_append_to_empty(self):
        lst = SinglyLinkedList()
        lst.append(1)
        assert len(lst) == 1
        assert lst._head.value == 1  # type: ignore[union-attr]
        assert lst._tail.value == 1  # type: ignore[union-attr]
        assert lst._head is lst._tail

    def test_append_updates_tail(self):
        lst = SinglyLinkedList(1, 2)
        lst.append(3)
        assert lst._tail.value == 3  # type: ignore[union-attr]
        assert lst._tail.next is None  # type: ignore[union-attr]

    def test_append_does_not_change_head(self):
        lst = SinglyLinkedList(1)
        lst.append(2)
        assert lst._head.value == 1  # type: ignore[union-attr]

    def test_append_links_correctly(self):
        lst = SinglyLinkedList()
        lst.append(1)
        lst.append(2)
        assert lst._head.next is lst._tail  # type: ignore[union-attr]

    def test_append_none(self):
        lst = SinglyLinkedList()
        lst.append(None)
        assert lst._head.value is None  # type: ignore[union-attr]
        assert len(lst) == 1

    def test_append_multiple_increments_size(self):
        lst = SinglyLinkedList()
        for i in range(5):
            lst.append(i)
        assert len(lst) == 5
        assert list(lst) == [0, 1, 2, 3, 4]


class TestSinglyLinkedListPrepend:
    def test_prepend_to_empty(self):
        lst = SinglyLinkedList()
        lst.prepend(1)
        assert len(lst) == 1
        assert lst._head is lst._tail
        assert lst._head.value == 1  # type: ignore[union-attr]

    def test_prepend_updates_head(self):
        lst = SinglyLinkedList(2, 3)
        lst.prepend(1)
        assert lst._head.value == 1  # type: ignore[union-attr]
        assert list(lst) == [1, 2, 3]

    def test_prepend_does_not_change_tail(self):
        lst = SinglyLinkedList(2, 3)
        lst.prepend(1)
        assert lst._tail.value == 3  # type: ignore[union-attr]

    def test_prepend_links_correctly(self):
        lst = SinglyLinkedList(2)
        lst.prepend(1)
        assert lst._head.next is lst._tail  # type: ignore[union-attr]

    def test_prepend_none(self):
        lst = SinglyLinkedList(1)
        lst.prepend(None)
        assert lst._head.value is None  # type: ignore[union-attr]
        assert list(lst) == [None, 1]


class TestSinglyLinkedListInsert:
    def test_insert_at_beginning(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.insert(0, 0)
        assert list(lst) == [0, 1, 2, 3]
        assert lst._head.value == 0  # type: ignore[union-attr]

    def test_insert_at_end(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.insert(3, 4)
        assert list(lst) == [1, 2, 3, 4]
        assert lst._tail.value == 4  # type: ignore[union-attr]

    def test_insert_in_middle(self):
        lst = SinglyLinkedList(1, 2, 4)
        lst.insert(2, 3)
        assert list(lst) == [1, 2, 3, 4]

    def test_insert_negative_index(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.insert(-1, 99)
        assert list(lst) == [1, 2, 99, 3]

    def test_insert_increments_size(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.insert(1, 99)
        assert len(lst) == 4

    def test_insert_into_empty_via_index_zero(self):
        lst = SinglyLinkedList()
        lst.insert(0, 42)
        assert list(lst) == [42]
        assert lst._head is lst._tail

    def test_insert_out_of_range_raises(self):
        lst = SinglyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst.insert(10, 99)

    def test_insert_bool_index_raises(self):
        lst = SinglyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst.insert(True, 99)  # type: ignore[arg-type]

    def test_insert_float_index_raises(self):
        lst = SinglyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst.insert(1.0, 99)  # type: ignore[arg-type]

    def test_insert_preserves_tail_next_none(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.insert(3, 4)
        assert lst._tail.next is None  # type: ignore[union-attr]


class TestSinglyLinkedListRemove:
    def test_remove_head(self):
        lst = SinglyLinkedList(1, 2, 3)
        val = lst.remove(0)
        assert val == 1
        assert list(lst) == [2, 3]
        assert lst._head.value == 2  # type: ignore[union-attr]

    def test_remove_tail(self):
        lst = SinglyLinkedList(1, 2, 3)
        val = lst.remove(2)
        assert val == 3
        assert list(lst) == [1, 2]
        assert lst._tail.value == 2  # type: ignore[union-attr]
        assert lst._tail.next is None  # type: ignore[union-attr]

    def test_remove_middle(self):
        lst = SinglyLinkedList(1, 2, 3)
        val = lst.remove(1)
        assert val == 2
        assert list(lst) == [1, 3]

    def test_remove_negative_index(self):
        lst = SinglyLinkedList(1, 2, 3)
        val = lst.remove(-1)
        assert val == 3
        assert list(lst) == [1, 2]

    def test_remove_only_element(self):
        lst = SinglyLinkedList(42)
        val = lst.remove(0)
        assert val == 42
        assert len(lst) == 0
        assert lst._head is None
        assert lst._tail is None

    def test_remove_decrements_size(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.remove(0)
        assert len(lst) == 2

    def test_remove_from_empty_raises(self):
        lst = SinglyLinkedList()
        with pytest.raises(IndexError):
            lst.remove(0)

    def test_remove_out_of_range_raises(self):
        lst = SinglyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst.remove(10)

    def test_remove_bool_index_raises(self):
        lst = SinglyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst.remove(True)  # type: ignore[arg-type]

    def test_remove_head_updates_head(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.remove(0)
        assert lst._head.value == 2  # type: ignore[union-attr]

    def test_remove_tail_tail_next_is_none(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.remove(-1)
        assert lst._tail.next is None  # type: ignore[union-attr]


class TestSinglyLinkedListGetSetItem:
    def test_getitem_positive(self):
        lst = SinglyLinkedList(10, 20, 30)
        assert lst[0] == 10
        assert lst[1] == 20
        assert lst[2] == 30

    def test_getitem_negative(self):
        lst = SinglyLinkedList(10, 20, 30)
        assert lst[-1] == 30
        assert lst[-3] == 10

    def test_getitem_out_of_range_raises(self):
        lst = SinglyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            _ = lst[3]

    def test_getitem_bool_index_raises(self):
        lst = SinglyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            _ = lst[True]  # type: ignore[index]

    def test_setitem_positive(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst[1] = 99
        assert lst[1] == 99
        assert list(lst) == [1, 99, 3]

    def test_setitem_negative(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst[-1] = 99
        assert lst[2] == 99

    def test_setitem_out_of_range_raises(self):
        lst = SinglyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst[5] = 99

    def test_setitem_does_not_change_size(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst[0] = 99
        assert len(lst) == 3


class TestSinglyLinkedListIterReversed:
    def test_iter_order(self):
        lst = SinglyLinkedList(1, 2, 3)
        assert list(lst) == [1, 2, 3]

    def test_iter_empty(self):
        lst = SinglyLinkedList()
        assert list(lst) == []

    def test_reversed_order(self):
        lst = SinglyLinkedList(1, 2, 3)
        assert list(reversed(lst)) == [3, 2, 1]

    def test_reversed_empty(self):
        lst = SinglyLinkedList()
        assert list(reversed(lst)) == []

    def test_reversed_single(self):
        lst = SinglyLinkedList(42)
        assert list(reversed(lst)) == [42]

    def test_reversed_does_not_modify_list(self):
        lst = SinglyLinkedList(1, 2, 3)
        _ = list(reversed(lst))
        assert list(lst) == [1, 2, 3]


class TestSinglyLinkedListEq:
    def test_equal_lists(self):
        a = SinglyLinkedList(1, 2, 3)
        b = SinglyLinkedList(1, 2, 3)
        assert a == b

    def test_both_empty(self):
        assert SinglyLinkedList() == SinglyLinkedList()

    def test_different_middle(self):
        a = SinglyLinkedList(1, 2, 3)
        b = SinglyLinkedList(1, 9, 3)
        assert a != b

    def test_different_size(self):
        a = SinglyLinkedList(1, 2, 3)
        b = SinglyLinkedList(1, 2)
        assert a != b

    def test_different_head(self):
        a = SinglyLinkedList(1, 2, 3)
        b = SinglyLinkedList(9, 2, 3)
        assert a != b

    def test_different_tail(self):
        a = SinglyLinkedList(1, 2, 3)
        b = SinglyLinkedList(1, 2, 9)
        assert a != b

    def test_not_implemented_for_other_type(self):
        lst = SinglyLinkedList(1, 2, 3)
        assert lst.__eq__([1, 2, 3]) is NotImplemented

    def test_single_element_equal(self):
        assert SinglyLinkedList(1) == SinglyLinkedList(1)

    def test_single_element_not_equal(self):
        assert SinglyLinkedList(1) != SinglyLinkedList(2)

    def test_with_none_values(self):
        a = SinglyLinkedList(1, None, 3)
        b = SinglyLinkedList(1, None, 3)
        assert a == b


class TestSinglyLinkedListRepr:
    def test_repr_empty(self):
        lst = SinglyLinkedList()
        assert repr(lst) == "SinglyLinkedList(size=0)[]"

    def test_repr_single(self):
        lst = SinglyLinkedList(1)
        assert repr(lst) == "SinglyLinkedList(size=1)[1]"

    def test_repr_multiple(self):
        lst = SinglyLinkedList(1, 2, 3)
        assert repr(lst) == "SinglyLinkedList(size=3)[1 -> 2 -> 3]"

    def test_repr_with_strings(self):
        lst = SinglyLinkedList("a", "b")
        assert repr(lst) == "SinglyLinkedList(size=2)['a' -> 'b']"
