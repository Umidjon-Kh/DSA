# Linked Lists

From-scratch implementation of singly, doubly, and circular linked lists in Python, built on top of custom `SingleNode` and `DoubleNode` classes.

---

## Structure

```
linked_lists/
├── _nodes.py              # SingleNode and DoubleNode — internal building blocks
├── single.py              # Singly linked list
├── double.py              # Doubly linked list
├── circular_single.py     # Circular singly linked list
└── circular_double.py     # Circular doubly linked list
```

---

## Classes

| Class                      | Node         | Circular | Bidirectional |
| -------------------------- | ------------ | -------- | ------------- |
| `SinglyLinkedList`         | `SingleNode` | ❌       | ❌            |
| `DoublyLinkedList`         | `DoubleNode` | ❌       | ✅            |
| `CircularSinglyLinkedList` | `SingleNode` | ✅       | ❌            |
| `CircularDoublyLinkedList` | `DoubleNode` | ✅       | ✅            |

---

## Time Complexity

| Operation      | Singly | Doubly | Circular Singly | Circular Doubly |
| -------------- | ------ | ------ | --------------- | --------------- |
| `append`       | O(1)   | O(1)   | O(1)            | O(1)            |
| `prepend`      | O(1)   | O(1)   | O(1)            | O(1)            |
| `insert`       | O(n)   | O(n/2) | O(n)            | O(n/2)          |
| `remove_head`  | O(1)   | O(1)   | O(1)            | O(1)            |
| `remove_tail`  | O(n)   | O(1)   | O(n)            | O(1)            |
| `remove`       | O(n)   | O(n/2) | O(n)            | O(n/2)          |
| `get_node`     | O(n)   | O(n/2) | O(n)            | O(n/2)          |
| `find`         | O(n)   | O(n)   | O(n)            | O(n)            |
| `copy`         | O(n)   | O(n)   | O(n)            | O(n)            |
| `__len__`      | O(1)   | O(1)   | O(1)            | O(1)            |
| `__iter__`     | O(n)   | O(n)   | O(n)            | O(n)            |
| `__reversed__` | —      | O(n)   | —               | O(n)            |

---

## Usage

```python
from data_structures.linked_lists import (
    SinglyLinkedList,
    DoublyLinkedList,
    CircularSinglyLinkedList,
    CircularDoublyLinkedList,
)

# Singly linked list
sll = SinglyLinkedList(1, 2, 3)
sll.append(4)
sll.prepend(0)
sll.insert(2, 99)
value = sll.remove_head()   # returns 0
value = sll.remove_tail()   # returns 4
value = sll.remove(1)       # returns 99
index = sll.find(2)         # returns 1
node = sll.get_node(0)      # returns SingleNode
sll.set_node(0, 42)         # replaces value at index 0
sll.set_node(len(sll), 99)  # appends new node

# Doubly linked list — same API plus __reversed__
dll = DoublyLinkedList(1, 2, 3)
dll.append(4)
values = list(reversed(dll))  # [4, 3, 2, 1]

# Circular singly linked list — tail.next always points to head
csll = CircularSinglyLinkedList(1, 2, 3)
csll.append(4)
assert csll._tail.next is csll._head  # always True

# Circular doubly linked list — tail.next → head and head.prev → tail
cdll = CircularDoublyLinkedList(1, 2, 3)
cdll.append(4)
assert cdll._tail.next is cdll._head  # always True
assert cdll._head.prev is cdll._tail  # always True
values = list(reversed(cdll))         # [4, 3, 2, 1]
```

---

## Design Decisions

**Why separate SingleNode and DoubleNode?**
`SingleNode` stores only `next` — less memory per node. `DoubleNode` stores both `next` and `prev` — enables O(1) `remove_tail` and backwards traversal. Each list uses only the node type it needs.

**Why get_node is public?**
`get_node` is used internally by `insert`, `remove`, and `set_node`. Making it public allows users to work with raw nodes when needed — useful for building higher-level structures on top of linked lists.

**Why Doubly has O(n/2) for insert/remove?**
`get_node` in `DoublyLinkedList` traverses from head if index is in the first half, from tail if in the second half — cutting traversal in half on average.

**Why Circular lists never have None in next/prev?**
In circular lists `tail.next = head` and (for doubly) `head.prev = tail` are invariants maintained after every operation. This enables continuous looping without None checks.
