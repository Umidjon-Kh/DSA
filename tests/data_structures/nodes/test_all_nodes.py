import pytest

from data_structures import BiLinearNode, LinearNode, TreeNode


class TestNodesInit:
    """
    Testing all Nodes init methods.
    """

    def test_stores_integer(self) -> None:
        linear = LinearNode(24)
        bi_linear = BiLinearNode(48)
        tree_node = TreeNode(72)

        assert linear.value == 24
        assert bi_linear.value == 48
        assert tree_node.value == 72

    def test_stores_str(self) -> None:
        linear = LinearNode("Hello")
        bi_linear = BiLinearNode("Hi")
        tree_node = TreeNode("Hello there")

        assert linear.value == "Hello"
        assert bi_linear.value == "Hi"
        assert tree_node.value == "Hello there"

    def test_stores_dict(self) -> None:
        linear = LinearNode({"next": None})
        bi_linear = BiLinearNode({"prev": None, "next": None})
        tree_node = TreeNode({"parent": None, "left": None, "right": None})

        assert linear.value == {"next": None}
        assert bi_linear.value == {"prev": None, "next": None}
        assert tree_node.value == {"parent": None, "left": None, "right": None}

    def test_other_attrs_default_none(self) -> None:
        linear = LinearNode(24)
        bi_linear = BiLinearNode(48)
        tree_node = TreeNode(72)

        assert linear.next is None
        assert bi_linear.next is None and bi_linear.prev is None
        assert (
            tree_node.parent is None
            and tree_node.left is None
            and tree_node.right is None
        )


class TestNodesLinking:
    """
    Testing linking in all nodes.
    """

    def test_linear_linking(self) -> None:
        node = LinearNode(23)
        next_node = LinearNode(45)
        last_node = LinearNode(55)
        node.next = next_node
        next_node.next = last_node

        # Knowing about next node
        assert node.next is next_node
        assert next_node.next is last_node
        assert last_node.next is None
        # Acces to next node attrs
        assert node.next.value == 45
        assert node.next.next is last_node
        assert node.next.next.value == 55  # type: ignore[union-attr]
        assert node.next.next.next is None  # type: ignore[union-attr]

    def test_bilinear_linking(self) -> None:
        node = BiLinearNode(1)
        prev_node = BiLinearNode(0)
        next_node = BiLinearNode(2)
        node.prev = prev_node
        prev_node.next = node
        node.next = next_node
        next_node.prev = node

        # Knowing about next and prev pointers
        assert node.prev is prev_node
        assert node.next is next_node
        assert next_node.prev is node and next_node.next is None
        assert prev_node.next is node and prev_node.prev is None

        # Acces to next and prev node attrs
        assert node.next.value == 2
        assert node.prev.value == 0
        assert node.prev.next is node
        assert node.next.prev is node
        assert prev_node.next.next is next_node
        assert next_node.prev.prev is prev_node

    def test_tree_node_linking(self) -> None:
        parent_node = TreeNode(50)
        left_node = TreeNode(25)
        right_node = TreeNode(75)

        parent_node.left = left_node
        parent_node.right = right_node
        left_node.parent = parent_node
        right_node.parent = parent_node

        # Knowing about left and right childrens
        assert parent_node.left is left_node
        assert left_node.left is None and left_node.right is None
        assert right_node.left is None and right_node.right is None

        # Acces to childrens node attrs
        assert parent_node.left.value == 25 == left_node.value
        assert parent_node.right.value == 75 == right_node.value
        assert parent_node.right.right is None
        assert parent_node.right.parent is parent_node
        assert parent_node.left.parent is parent_node


class TestNodesRepr:
    """
    Testing nodes representation methods.
    """

    def test_linear_repr(self) -> None:
        node = LinearNode(45)
        assert repr(node) == "LinearNode(45) -> None"
        node.next = LinearNode(89)
        assert repr(node) == "LinearNode(45) -> 89"

    def test_bi_linear_repr(self) -> None:
        node = BiLinearNode(24)
        assert repr(node) == "None <-> BiLinearNode(24) <-> None"
        node.next = BiLinearNode(48)
        assert repr(node) == "None <-> BiLinearNode(24) <-> 48"
        node.prev = BiLinearNode(12)
        assert repr(node) == "12 <-> BiLinearNode(24) <-> 48"

    def test_tree_node_repr(self) -> None:
        node = TreeNode(50)
        assert repr(node) == "TreeNode(50) -> (L: None, R: None, P: None)"
        node.left = TreeNode(25)
        assert repr(node) == "TreeNode(50) -> (L: 25, R: None, P: None)"
        node.right = TreeNode(75)
        assert repr(node) == "TreeNode(50) -> (L: 25, R: 75, P: None)"
        node.parent = TreeNode(100)
        assert repr(node) == "TreeNode(50) -> (L: 25, R: 75, P: 100)"
