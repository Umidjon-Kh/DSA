from data_structures import BiLinearNode, LinearNode, TreeNode


class TestNodesInitialization:
    """
    Testing all nodes initialization and value storing.
    """

    def test_stores_integer(self) -> None:
        linear = LinearNode(24)
        bi_linear = BiLinearNode(56)
        tree_node = TreeNode(45)

        assert linear.value == 24
        assert bi_linear.value == 56
        assert tree_node.value == 45

    def test_stores_string(self) -> None:
        linear = LinearNode("hello")
        bi_linear = BiLinearNode("hi")
        tree_node = TreeNode("hihi")

        assert linear.value == "hello"
        assert bi_linear.value == "hi"
        assert tree_node.value == "hihi"

    def test_stores_list(self) -> None:
        linear = LinearNode([1, 2, 3])
        bi_linear = BiLinearNode([4, 5, 6])
        tree_node = TreeNode([7, 8, 9])

        assert linear.value == [1, 2, 3]
        assert bi_linear.value == [4, 5, 6]
        assert tree_node.value == [7, 8, 9]

    def test_stores_dict(self) -> None:
        linear = LinearNode({"key": "value"})
        bi_linear = BiLinearNode({"hi": "hello"})
        tree_node = TreeNode({"who": "me"})

        assert linear.value == {"key": "value"}
        assert bi_linear.value == {"hi": "hello"}
        assert tree_node.value == {"who": "me"}


class TestNodesLinking:
    """
    Testing all nodes linking and accessibility.
    """

    def test_linear_linking(self) -> None:
        node = LinearNode(42)
        next_node = LinearNode(56)

        node.next = next_node

        assert node.next is next_node
        assert node.next.value == 56
        assert node.next.next is None
        assert next_node.next is None

    def test_bi_linear_linking(self) -> None:
        node = BiLinearNode("Umidjon")
        prev_node = BiLinearNode("Hello")
        next_node = BiLinearNode("nice to meet you!")

        node.prev = prev_node
        prev_node.next = node
        node.next = next_node
        next_node.prev = node

        assert node.prev is prev_node
        assert node.prev.value == "Hello"

        assert node.next is next_node
        assert node.next.value == "nice to meet you!"

        assert next_node.prev is node
        assert next_node.prev.prev is prev_node
        assert next_node.next is None

        assert prev_node.next is node
        assert prev_node.next.next is next_node
        assert prev_node.prev is None

        assert (
            f"{node.prev.value} {node.value} {node.next.value}"
            == "Hello Umidjon nice to meet you!"
        )

    def test_tree_node_linking(self) -> None:
        node = TreeNode("Perishable")
        left_node = TreeNode("Electronics")
        right_node = TreeNode("Ordinary")
        parent_node = TreeNode("Product")

        node.parent = parent_node
        node.left = left_node
        node.right = right_node

        left_node.parent = node
        right_node.parent = node

        assert node.parent is parent_node
        assert node.parent.value == "Product"

        assert node.left is left_node
        assert node.left.value == "Electronics"

        assert node.right is right_node
        assert node.right.value == "Ordinary"

        assert left_node.parent is node
        assert right_node.parent is node

        assert left_node.left is None
        assert left_node.right is None
        assert right_node.left is None
        assert right_node.right is None


class TestNodesRepr:
    """
    Testing string representations of all nodes.
    """

    def test_linear_repr_without_next(self) -> None:
        node = LinearNode(10)
        assert repr(node) == "LinearNode(10) -> None"

    def test_linear_repr_with_next(self) -> None:
        node = LinearNode(10)
        next_node = LinearNode(20)
        node.next = next_node

        assert repr(node) == "LinearNode(10) -> 20"

    def test_bi_linear_repr_isolated(self) -> None:
        node = BiLinearNode(5)
        assert repr(node) == "None <-> BiLinearNode(5) <-> None"

    def test_bi_linear_repr_linked(self) -> None:
        prev_node = BiLinearNode(1)
        node = BiLinearNode(2)
        next_node = BiLinearNode(3)

        node.prev = prev_node
        node.next = next_node

        assert repr(node) == "1 <-> BiLinearNode(2) <-> 3"

    def test_tree_repr_isolated(self) -> None:
        node = TreeNode(10)
        assert repr(node) == "TreeNode(10) -> (L: None, R: None, P: None)"

    def test_tree_repr_linked(self) -> None:
        parent = TreeNode(20)
        left = TreeNode(5)
        right = TreeNode(15)
        node = TreeNode(10)

        node.parent = parent
        node.left = left
        node.right = right

        assert repr(node) == "TreeNode(10) -> (L: 5, R: 15, P: 20)"
