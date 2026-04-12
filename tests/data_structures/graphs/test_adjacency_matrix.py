import pytest

from data_structures.graphs import AdjacencyMatrixGraph

# ══════════════════════════════════════════════════════════════════════════════
# Initialization
# ══════════════════════════════════════════════════════════════════════════════


def test_init_empty() -> None:
    """Create empty undirected, unweighted graph."""
    g = AdjacencyMatrixGraph()
    assert len(g) == 0
    assert not g
    assert g.get_vertices() == []


def test_init_with_vertices() -> None:
    """Create graph with individual vertices."""
    g = AdjacencyMatrixGraph((1,), (2,), (3,))
    assert len(g) == 3
    assert sorted(g.get_vertices()) == [1, 2, 3]


def test_init_with_edges() -> None:
    """Create graph with edges (vertices created automatically)."""
    g = AdjacencyMatrixGraph((1, 2), (2, 3), (3, 1))
    assert len(g) == 3
    assert sorted(g.get_vertices()) == [1, 2, 3]


def test_init_with_weighted_edges() -> None:
    """Create weighted graph with initial edges."""
    g = AdjacencyMatrixGraph((1, 2, 0.5), (2, 3, 1.5), weighted=True)
    assert len(g) == 3
    assert g.has_edge(1, 2)
    neighbors = g.get_neighbors(1)
    assert (2, 0.5) in neighbors


def test_init_directed() -> None:
    """Create directed graph (edges are one-way)."""
    g = AdjacencyMatrixGraph((1, 2), (2, 3), directed=True)
    assert g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_init_undirected() -> None:
    """Create undirected graph (edges are bidirectional)."""
    g = AdjacencyMatrixGraph((1, 2), directed=False)
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)


def test_init_mixed_vertices_and_edges() -> None:
    """Initialize with both individual vertices and edges."""
    g = AdjacencyMatrixGraph((1,), (2, 3), (3, 4), (5,))
    assert len(g) == 5
    assert sorted(g.get_vertices()) == [1, 2, 3, 4, 5]


def test_init_invalid_tuple_empty() -> None:
    """Empty tuples should raise ValueError."""
    with pytest.raises(ValueError, match="non-empty tuple"):
        AdjacencyMatrixGraph(())


def test_init_invalid_tuple_too_long() -> None:
    """Tuples with more than 3 elements should raise ValueError."""
    with pytest.raises(ValueError, match="1, 2, or 3 elements"):
        AdjacencyMatrixGraph((1, 2, 3, 4))


def test_init_invalid_non_tuple() -> None:
    """Non-tuple arguments should raise ValueError."""
    with pytest.raises(ValueError, match="non-empty tuple"):
        AdjacencyMatrixGraph([1, 2])  # type: ignore[test]


def test_init_weighted_with_tuple_weight() -> None:
    """Weighted graph stores tuple weights if provided."""
    g = AdjacencyMatrixGraph((1, 2, (3, 4)), weighted=True)
    neighbors = g.get_neighbors(1)
    assert (2, (3, 4)) in neighbors


def test_matrix_initialized_empty() -> None:
    """Matrix starts empty when graph is empty."""
    g = AdjacencyMatrixGraph()
    assert len(g._matrix) == 0


def test_matrix_initialized_with_vertices() -> None:
    """Matrix has correct size when vertices added."""
    g = AdjacencyMatrixGraph((1,), (2,), (3,))
    assert len(g._matrix) == 3
    for row in g._matrix:
        assert len(row) == 3


# ══════════════════════════════════════════════════════════════════════════════
# Vertex Operations - Add
# ══════════════════════════════════════════════════════════════════════════════


def test_add_vertex_single() -> None:
    """Add a single vertex to empty graph."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    assert len(g) == 1
    assert 1 in g


def test_add_vertex_multiple() -> None:
    """Add multiple vertices."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    assert len(g) == 3
    assert 1 in g and 2 in g and 3 in g


def test_add_vertex_duplicate_no_effect() -> None:
    """Adding duplicate vertex does nothing."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    g.add_vertex(1)
    assert len(g) == 1


def test_add_vertex_mixed_types() -> None:
    """Vertices can be of mixed types."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    g.add_vertex("a")
    g.add_vertex((1, 2))
    assert len(g) == 3


def test_add_vertex_expands_matrix() -> None:
    """Adding vertex expands matrix correctly."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    assert len(g._matrix) == 1
    assert len(g._matrix[0]) == 1

    g.add_vertex(2)
    assert len(g._matrix) == 2
    assert len(g._matrix[0]) == 2
    assert len(g._matrix[1]) == 2

    g.add_vertex(3)
    assert len(g._matrix) == 3
    for row in g._matrix:
        assert len(row) == 3


def test_add_vertex_string() -> None:
    """String vertices work."""
    g = AdjacencyMatrixGraph()
    g.add_vertex("hello")
    g.add_vertex("world")
    assert "hello" in g
    assert "world" in g


def test_add_vertex_expansion_preserves_edges() -> None:
    """Expanding matrix preserves existing edges."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    # Verify edge exists
    assert g.has_edge(1, 2)

    # Add new vertex
    g.add_vertex(3)

    # Original edge still exists
    assert g.has_edge(1, 2)
    assert not g.has_edge(1, 3)
    assert not g.has_edge(2, 3)


# ══════════════════════════════════════════════════════════════════════════════
# Vertex Operations - Remove
# ══════════════════════════════════════════════════════════════════════════════


def test_remove_vertex_single() -> None:
    """Remove a single vertex."""
    g = AdjacencyMatrixGraph((1,), (2,), (3,))
    g.remove_vertex(2)
    assert len(g) == 2
    assert 2 not in g


def test_remove_vertex_with_edges() -> None:
    """Removing vertex removes all its edges."""
    g = AdjacencyMatrixGraph((1, 2), (1, 3), (2, 3))
    g.remove_vertex(1)
    assert len(g) == 2
    assert not g.has_edge(1, 2)
    assert not g.has_edge(1, 3)
    assert g.has_edge(2, 3)


def test_remove_vertex_nonexistent() -> None:
    """Removing nonexistent vertex does nothing."""
    g = AdjacencyMatrixGraph((1,))
    g.remove_vertex(99)
    assert len(g) == 1


def test_remove_vertex_rebuilds_matrix() -> None:
    """Removing vertex rebuilds matrix correctly."""
    g = AdjacencyMatrixGraph()
    g.add_vertex("a")
    g.add_vertex("b")
    g.add_vertex("c")
    assert len(g._matrix) == 3

    g.remove_vertex("b")
    assert len(g._matrix) == 2
    assert len(g._matrix[0]) == 2
    assert len(g._matrix[1]) == 2


def test_remove_vertex_updates_mappings() -> None:
    """Removing vertex updates internal mappings."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)

    g.remove_vertex(2)
    # Check that remaining vertices are correctly mapped
    assert g._get_index(1) is not None
    assert g._get_index(2) is None
    assert g._get_index(3) is not None


def test_remove_vertex_directed() -> None:
    """Removing vertex removes outgoing and incoming edges."""
    g = AdjacencyMatrixGraph((1, 2), (2, 3), (3, 1), directed=True)
    g.remove_vertex(2)
    assert not g.has_edge(1, 2)
    assert not g.has_edge(2, 3)
    assert g.has_edge(3, 1)


def test_remove_vertex_preserves_remaining_edges() -> None:
    """Removing vertex preserves edges between other vertices."""
    g = AdjacencyMatrixGraph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(1, 4)

    g.remove_vertex(2)

    assert g.has_edge(3, 4)
    assert g.has_edge(1, 4)
    assert not g.has_edge(1, 2)
    assert not g.has_edge(2, 3)


def test_remove_first_vertex() -> None:
    """Remove first vertex in matrix."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.remove_vertex(1)
    assert 1 not in g
    assert 2 in g
    assert 3 in g


def test_remove_last_vertex() -> None:
    """Remove last vertex in matrix."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.remove_vertex(3)
    assert 3 not in g
    assert 1 in g
    assert 2 in g


# ══════════════════════════════════════════════════════════════════════════════
# Vertex Operations - Query
# ══════════════════════════════════════════════════════════════════════════════


def test_get_vertices_empty() -> None:
    """get_vertices() on empty graph returns empty list."""
    g = AdjacencyMatrixGraph()
    assert g.get_vertices() == []


def test_get_vertices_returns_list() -> None:
    """get_vertices() returns list of all vertices."""
    g = AdjacencyMatrixGraph((1,), (2,), (3,))
    vertices = g.get_vertices()
    assert sorted(vertices) == [1, 2, 3]


def test_get_vertices_single() -> None:
    """get_vertices() with single vertex."""
    g = AdjacencyMatrixGraph((1,))
    vertices = g.get_vertices()
    assert vertices == [1]


def test_get_vertices_insertion_order() -> None:
    """get_vertices() returns vertices in insertion order."""
    g = AdjacencyMatrixGraph()
    g.add_vertex("a")
    g.add_vertex("b")
    g.add_vertex("c")
    vertices = g.get_vertices()
    assert vertices == ["a", "b", "c"]


# ══════════════════════════════════════════════════════════════════════════════
# Edge Operations - Add
# ══════════════════════════════════════════════════════════════════════════════


def test_add_edge_creates_vertices() -> None:
    """Adding edge creates vertices if they don't exist."""
    g = AdjacencyMatrixGraph()
    g.add_edge(1, 2)
    assert len(g) == 2
    assert 1 in g and 2 in g


def test_add_edge_unweighted() -> None:
    """Add unweighted edge."""
    g = AdjacencyMatrixGraph()
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)
    neighbors = g.get_neighbors(1)
    assert (2, None) in neighbors


def test_add_edge_directed() -> None:
    """In directed graph, edge is one-way."""
    g = AdjacencyMatrixGraph(directed=True)
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_add_edge_undirected() -> None:
    """In undirected graph, edge is bidirectional."""
    g = AdjacencyMatrixGraph(directed=False)
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)


def test_add_edge_weighted() -> None:
    """Add weighted edge (requires weighted=True)."""
    g = AdjacencyMatrixGraph(weighted=True)
    g.add_edge(1, 2, 5.0)
    neighbors = g.get_neighbors(1)
    assert (2, 5.0) in neighbors


def test_add_edge_duplicate_no_effect() -> None:
    """Adding duplicate edge does nothing."""
    g = AdjacencyMatrixGraph()
    g.add_edge(1, 2)
    neighbors_before = len(g.get_neighbors(1))
    g.add_edge(1, 2)
    neighbors_after = len(g.get_neighbors(1))
    assert neighbors_before == neighbors_after


def test_add_edge_self_loop_raises() -> None:
    """Self-loops are not allowed."""
    g = AdjacencyMatrixGraph()
    with pytest.raises(ValueError, match="Self-loops"):
        g.add_edge(1, 1)


def test_add_edge_weighted_no_weight_raises() -> None:
    """Weighted graph requires weight parameter."""
    g = AdjacencyMatrixGraph(weighted=True)
    with pytest.raises(ValueError, match="weight must be provided"):
        g.add_edge(1, 2)


def test_add_edge_weighted_zero_is_valid() -> None:
    """Weight of 0 is valid (falsy but not None)."""
    g = AdjacencyMatrixGraph(weighted=True)
    g.add_edge(1, 2, 0)
    neighbors = g.get_neighbors(1)
    assert (2, 0) in neighbors


def test_add_edge_negative_weight() -> None:
    """Negative weights are allowed."""
    g = AdjacencyMatrixGraph(weighted=True)
    g.add_edge(1, 2, -5.0)
    neighbors = g.get_neighbors(1)
    assert (2, -5.0) in neighbors


def test_add_edge_stores_as_true_unweighted() -> None:
    """Unweighted edges stored as True in matrix."""
    g = AdjacencyMatrixGraph()
    g.add_edge(1, 2)
    # Matrix cell should contain True
    idx_1 = g._get_index(1)
    idx_2 = g._get_index(2)
    assert g._matrix[idx_1][idx_2] is True  # type: ignore[comparison-overlap]


def test_add_edge_stores_weight_weighted() -> None:
    """Weighted edges store numeric weight in matrix."""
    g = AdjacencyMatrixGraph(weighted=True)
    g.add_edge(1, 2, 7.5)
    idx_1 = g._get_index(1)
    idx_2 = g._get_index(2)
    assert g._matrix[idx_1][idx_2] == 7.5  # type: ignore[union-attr]


# ══════════════════════════════════════════════════════════════════════════════
# Edge Operations - Remove & Query
# ══════════════════════════════════════════════════════════════════════════════


def test_remove_edge_basic() -> None:
    """Remove an existing edge."""
    g = AdjacencyMatrixGraph((1, 2))
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)


def test_remove_edge_directed() -> None:
    """Removing directed edge only removes one direction."""
    g = AdjacencyMatrixGraph((1, 2), directed=True)
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)


def test_remove_edge_undirected() -> None:
    """Removing edge in undirected graph removes both directions."""
    g = AdjacencyMatrixGraph((1, 2), directed=False)
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_remove_edge_nonexistent() -> None:
    """Removing nonexistent edge does nothing."""
    g = AdjacencyMatrixGraph((1,), (2,))
    g.remove_edge(1, 2)  # doesn't raise
    assert len(g) == 2


def test_remove_edge_missing_vertex() -> None:
    """Removing edge with missing vertex does nothing."""
    g = AdjacencyMatrixGraph((1, 2))
    g.remove_edge(1, 99)
    assert len(g) == 2


def test_remove_edge_sets_to_none() -> None:
    """Removing edge sets matrix cell to None."""
    g = AdjacencyMatrixGraph((1, 2))
    g.remove_edge(1, 2)
    idx_1 = g._get_index(1)
    idx_2 = g._get_index(2)
    assert g._matrix[idx_1][idx_2] is None  # type: ignore[union-attr]


def test_has_edge_constant_time() -> None:
    """has_edge is O(1) - direct matrix lookup."""
    g = AdjacencyMatrixGraph(directed=True)
    # Add many vertices
    for i in range(100):
        g.add_vertex(i)
    # Check specific edge (should be fast)
    g.add_edge(0, 99)
    assert g.has_edge(0, 99)
    assert not g.has_edge(99, 0)


def test_has_edge_true() -> None:
    """has_edge returns True for existing edge."""
    g = AdjacencyMatrixGraph((1, 2))
    assert g.has_edge(1, 2)


def test_has_edge_false() -> None:
    """has_edge returns False for non-existing edge."""
    g = AdjacencyMatrixGraph((1,), (2,))
    assert not g.has_edge(1, 2)


def test_has_edge_directed_asymmetric() -> None:
    """In directed graph, edges are asymmetric."""
    g = AdjacencyMatrixGraph((1, 2), directed=True)
    assert g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_has_edge_undirected_symmetric() -> None:
    """In undirected graph, edges are symmetric."""
    g = AdjacencyMatrixGraph((1, 2), directed=False)
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)


def test_has_edge_missing_vertex() -> None:
    """has_edge returns False if vertex missing."""
    g = AdjacencyMatrixGraph((1,))
    assert not g.has_edge(1, 99)
    assert not g.has_edge(99, 1)


# ══════════════════════════════════════════════════════════════════════════════
# Neighbors & Weights
# ══════════════════════════════════════════════════════════════════════════════


def test_get_neighbors_single() -> None:
    """get_neighbors returns list with one neighbor."""
    g = AdjacencyMatrixGraph((1, 2))
    neighbors = g.get_neighbors(1)
    assert neighbors == [(2, None)]


def test_get_neighbors_multiple() -> None:
    """get_neighbors returns all neighbors."""
    g = AdjacencyMatrixGraph((1, 2), (1, 3), (1, 4))
    neighbors = g.get_neighbors(1)
    neighbors_set = set(neighbors)
    assert (2, None) in neighbors_set
    assert (3, None) in neighbors_set
    assert (4, None) in neighbors_set
    assert len(neighbors) == 3


def test_get_neighbors_empty() -> None:
    """get_neighbors returns empty list for isolated vertex."""
    g = AdjacencyMatrixGraph((1,))
    neighbors = g.get_neighbors(1)
    assert neighbors == []


def test_get_neighbors_weighted() -> None:
    """get_neighbors includes weights in weighted graph."""
    g = AdjacencyMatrixGraph((1, 2, 5.0), (1, 3, 10.0), weighted=True)
    neighbors = g.get_neighbors(1)
    neighbors_set = set(neighbors)
    assert (2, 5.0) in neighbors_set
    assert (3, 10.0) in neighbors_set


def test_get_neighbors_nonexistent_raises() -> None:
    """get_neighbors raises KeyError for nonexistent vertex."""
    g = AdjacencyMatrixGraph()
    with pytest.raises(KeyError):
        g.get_neighbors(99)


def test_get_neighbors_directed_asymmetric() -> None:
    """Neighbors differ by direction in directed graph."""
    g = AdjacencyMatrixGraph((1, 2), (2, 1), directed=True)
    neighbors_1 = g.get_neighbors(1)
    neighbors_2 = g.get_neighbors(2)
    assert (2, None) in neighbors_1
    assert (1, None) in neighbors_2
    assert (1, None) not in neighbors_1
    assert (2, None) not in neighbors_2


def test_get_neighbors_scans_row() -> None:
    """get_neighbors scans entire row."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)

    g.add_edge(1, 2)
    g.add_edge(1, 4)

    neighbors = g.get_neighbors(1)
    assert len(neighbors) == 2
    neighbor_set = set(neighbors)
    assert (2, None) in neighbor_set
    assert (4, None) in neighbor_set
    assert (3, None) not in neighbor_set


# ══════════════════════════════════════════════════════════════════════════════
# Collection Methods
# ══════════════════════════════════════════════════════════════════════════════


def test_clear_removes_all() -> None:
    """clear() removes all vertices and edges."""
    g = AdjacencyMatrixGraph((1, 2), (2, 3), (3, 1))
    g.clear()
    assert len(g) == 0
    assert g.get_vertices() == []


def test_clear_on_empty_graph() -> None:
    """clear() on empty graph does nothing."""
    g = AdjacencyMatrixGraph()
    g.clear()
    assert len(g) == 0


def test_clear_resets_matrix() -> None:
    """clear() resets matrix to empty."""
    g = AdjacencyMatrixGraph((1, 2), (2, 3))
    g.clear()
    assert len(g._matrix) == 0


def test_copy_creates_independent() -> None:
    """copy() creates independent copy."""
    g1 = AdjacencyMatrixGraph((1, 2), (2, 3))
    g2 = g1.copy()

    # Modify g2
    g2.add_vertex(4)
    g2.add_edge(1, 3)

    # g1 should be unchanged
    assert len(g1) == 3
    assert 4 not in g1
    assert not g1.has_edge(1, 3)


def test_copy_preserves_directed() -> None:
    """copy() preserves directed flag."""
    g1 = AdjacencyMatrixGraph((1, 2), directed=True)
    g2 = g1.copy()
    assert g2._directed == g1._directed


def test_copy_preserves_weighted() -> None:
    """copy() preserves weighted flag."""
    g1 = AdjacencyMatrixGraph((1, 2, 5.0), weighted=True)
    g2 = g1.copy()
    assert g2._weighted == g1._weighted


def test_copy_preserves_edges() -> None:
    """copy() preserves all edges."""
    g1 = AdjacencyMatrixGraph((1, 2), (2, 3), (3, 1))
    g2 = g1.copy()
    assert g2.has_edge(1, 2)
    assert g2.has_edge(2, 3)
    assert g2.has_edge(3, 1)


def test_copy_empty_graph() -> None:
    """copy() works on empty graph."""
    g1 = AdjacencyMatrixGraph()
    g2 = g1.copy()
    assert len(g2) == 0


def test_copy_copies_matrix() -> None:
    """copy() creates independent matrix."""
    g1 = AdjacencyMatrixGraph((1, 2))
    g1.add_edge(1, 2)
    g2 = g1.copy()

    # Modify g2's matrix
    g2.add_edge(1, 2)  # should already exist, so no change

    # Add new edge to g1
    g1.add_vertex(3)
    g1.add_edge(1, 3)

    # g2 should not have vertex 3
    assert 3 not in g2


def test_copy_is_independent_add_edge() -> None:
    """Modifying copy by adding edge does not affect original."""
    g1 = AdjacencyMatrixGraph((1, 2), (2, 3))
    g2 = g1.copy()
    g2.add_edge(1, 3)
    assert g2.has_edge(1, 3)
    assert not g1.has_edge(1, 3)  # original unchanged


def test_copy_is_independent_remove_edge() -> None:
    """Modifying copy by removing edge does not affect original."""
    g1 = AdjacencyMatrixGraph((1, 2), (2, 3))
    g2 = g1.copy()
    g2.remove_edge(1, 2)
    assert not g2.has_edge(1, 2)
    assert g1.has_edge(1, 2)  # original unchanged


def test_copy_is_independent_add_vertex() -> None:
    """Modifying copy by adding vertex does not affect original."""
    g1 = AdjacencyMatrixGraph((1, 2))
    g2 = g1.copy()
    g2.add_vertex(3)
    assert 3 in g2
    assert 3 not in g1  # original unchanged


def test_copy_is_independent_remove_vertex() -> None:
    """Modifying copy by removing vertex does not affect original."""
    g1 = AdjacencyMatrixGraph((1,), (2,), (3,))
    g2 = g1.copy()
    g2.remove_vertex(3)
    assert 3 not in g2
    assert 3 in g1  # original unchanged


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Size & Boolean
# ══════════════════════════════════════════════════════════════════════════════


def test_len_empty() -> None:
    """__len__() on empty graph is 0."""
    g = AdjacencyMatrixGraph()
    assert len(g) == 0


def test_len_with_vertices() -> None:
    """__len__() returns vertex count."""
    g = AdjacencyMatrixGraph((1,), (2,), (3,))
    assert len(g) == 3


def test_len_with_edges_only() -> None:
    """__len__() counts vertices, not edges."""
    g = AdjacencyMatrixGraph((1, 2), (1, 3), (1, 4))
    assert len(g) == 4


def test_bool_empty() -> None:
    """__bool__() on empty graph is False."""
    g = AdjacencyMatrixGraph()
    assert not g


def test_bool_non_empty() -> None:
    """__bool__() on non-empty graph is True."""
    g = AdjacencyMatrixGraph((1,))
    assert g


def test_bool_with_edges_only() -> None:
    """__bool__() is True if graph has edges (vertices exist)."""
    g = AdjacencyMatrixGraph((1, 2))
    assert g


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Iteration
# ══════════════════════════════════════════════════════════════════════════════


def test_iter_empty() -> None:
    """__iter__() on empty graph yields nothing."""
    g = AdjacencyMatrixGraph()
    assert list(g) == []


def test_iter_yields_all_vertices() -> None:
    """__iter__() yields all vertices."""
    g = AdjacencyMatrixGraph((1,), (2,), (3,))
    vertices = list(g)
    assert sorted(vertices) == [1, 2, 3]


def test_iter_insertion_order() -> None:
    """__iter__() yields vertices in insertion order."""
    g = AdjacencyMatrixGraph()
    g.add_vertex("a")
    g.add_vertex("b")
    g.add_vertex("c")
    vertices = list(g)
    assert vertices == ["a", "b", "c"]


def test_reversed_empty() -> None:
    """__reversed__() on empty graph yields nothing."""
    g = AdjacencyMatrixGraph()
    assert list(reversed(g)) == []


def test_reversed_order() -> None:
    """__reversed__() yields vertices in reverse."""
    g = AdjacencyMatrixGraph()
    g.add_vertex("a")
    g.add_vertex("b")
    g.add_vertex("c")
    vertices = list(reversed(g))
    assert vertices == ["c", "b", "a"]


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Membership
# ══════════════════════════════════════════════════════════════════════════════


def test_contains_true() -> None:
    """__contains__() returns True for existing vertex."""
    g = AdjacencyMatrixGraph((1,))
    assert 1 in g


def test_contains_false() -> None:
    """__contains__() returns False for missing vertex."""
    g = AdjacencyMatrixGraph((1,))
    assert 2 not in g


def test_contains_empty_graph() -> None:
    """__contains__() on empty graph returns False."""
    g = AdjacencyMatrixGraph()
    assert 1 not in g


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Equality
# ══════════════════════════════════════════════════════════════════════════════


def test_eq_empty_graphs() -> None:
    """Two empty graphs are equal."""
    g1 = AdjacencyMatrixGraph()
    g2 = AdjacencyMatrixGraph()
    assert g1 == g2


def test_eq_same_vertices() -> None:
    """Graphs with same vertices are equal."""
    g1 = AdjacencyMatrixGraph((1,), (2,), (3,))
    g2 = AdjacencyMatrixGraph((1,), (2,), (3,))
    assert g1 == g2


def test_eq_same_edges() -> None:
    """Graphs with same edges are equal."""
    g1 = AdjacencyMatrixGraph((1, 2), (2, 3))
    g2 = AdjacencyMatrixGraph((1, 2), (2, 3))
    assert g1 == g2


def test_eq_different_vertices() -> None:
    """Graphs with different vertices are not equal."""
    g1 = AdjacencyMatrixGraph((1,), (2,))
    g2 = AdjacencyMatrixGraph((1,), (3,))
    assert g1 != g2


def test_eq_different_edges() -> None:
    """Graphs with different edges are not equal."""
    g1 = AdjacencyMatrixGraph((1, 2))
    g2 = AdjacencyMatrixGraph((1, 3))
    assert g1 != g2


def test_eq_directed_vs_undirected() -> None:
    """Directed and undirected graphs are not equal."""
    g1 = AdjacencyMatrixGraph((1, 2), directed=False)
    g2 = AdjacencyMatrixGraph((1, 2), directed=True)
    assert g1 != g2


def test_eq_weighted_vs_unweighted() -> None:
    """Weighted and unweighted graphs are not equal."""
    g1 = AdjacencyMatrixGraph((1, 2, 5.0), weighted=True)
    g2 = AdjacencyMatrixGraph((1, 2), weighted=False)
    assert g1 != g2


def test_eq_different_weights() -> None:
    """Graphs with different weights are not equal."""
    g1 = AdjacencyMatrixGraph((1, 2, 5.0), weighted=True)
    g2 = AdjacencyMatrixGraph((1, 2, 10.0), weighted=True)
    assert g1 != g2


def test_eq_non_graph_type() -> None:
    """Comparing with non-graph returns NotImplemented."""
    g = AdjacencyMatrixGraph()
    result = g.__eq__([1, 2, 3])  # type: ignore[arg-type]
    assert result is NotImplemented


def test_eq_after_copy() -> None:
    """Copied graph equals original."""
    g1 = AdjacencyMatrixGraph((1, 2, 5.0), (2, 3, 10.0), weighted=True)
    g2 = g1.copy()
    assert g1 == g2


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Representation
# ══════════════════════════════════════════════════════════════════════════════


def test_repr_format() -> None:
    """__repr__() returns correct format."""
    g = AdjacencyMatrixGraph((1,), (2,), directed=True, weighted=True)
    repr_str = repr(g)
    assert "AdjacencyMatrixGraph" in repr_str
    assert "vertices=2" in repr_str
    assert "directed=True" in repr_str
    assert "weighted=True" in repr_str


def test_repr_empty() -> None:
    """__repr__() works on empty graph."""
    g = AdjacencyMatrixGraph()
    repr_str = repr(g)
    assert "vertices=0" in repr_str


def test_repr_contains_class_name() -> None:
    """__repr__() contains class name."""
    g = AdjacencyMatrixGraph((1,))
    assert "AdjacencyMatrixGraph" in repr(g)


# ══════════════════════════════════════════════════════════════════════════════
# Matrix-Specific Behavior
# ══════════════════════════════════════════════════════════════════════════════


def test_matrix_always_square() -> None:
    """Matrix is always square (n x n)."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    assert len(g._matrix) == len(g._matrix[0])

    g.add_vertex(2)
    assert len(g._matrix) == len(g._matrix[0])
    assert len(g._matrix) == 2

    g.add_vertex(3)
    assert len(g._matrix) == 3
    for row in g._matrix:
        assert len(row) == 3


def test_undirected_matrix_symmetric() -> None:
    """In undirected graph, matrix is symmetric."""
    g = AdjacencyMatrixGraph(directed=False)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    idx_1 = g._get_index(1)
    idx_2 = g._get_index(2)
    idx_3 = g._get_index(3)

    # Symmetry check
    assert g._matrix[idx_1][idx_2] == g._matrix[idx_2][idx_1]  # type: ignore[union-attr]
    assert g._matrix[idx_2][idx_3] == g._matrix[idx_3][idx_2]  # type: ignore[union-attr]


def test_directed_matrix_not_symmetric() -> None:
    """In directed graph, matrix may not be symmetric."""
    g = AdjacencyMatrixGraph(directed=True)
    g.add_edge(1, 2)
    g.add_edge(3, 2)

    idx_1 = g._get_index(1)
    idx_2 = g._get_index(2)
    # idx_3 = g._get_index(3)

    # Not symmetric
    assert g._matrix[idx_1][idx_2] is not None  # type: ignore[union-attr]
    assert g._matrix[idx_2][idx_1] is None  # type: ignore[union-attr]


def test_diagonal_always_none() -> None:
    """Diagonal elements always None (no self-loops)."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)

    idx_1 = g._get_index(1)
    idx_2 = g._get_index(2)
    idx_3 = g._get_index(3)

    assert g._matrix[idx_1][idx_1] is None  # type: ignore[union-attr]
    assert g._matrix[idx_2][idx_2] is None  # type: ignore[union-attr]
    assert g._matrix[idx_3][idx_3] is None  # type: ignore[union-attr]


def test_vertex_removal_compacts_matrix() -> None:
    """Vertex removal shrinks matrix."""
    g = AdjacencyMatrixGraph()
    for i in range(10):
        g.add_vertex(i)

    initial_size = len(g._matrix)
    g.remove_vertex(5)
    assert len(g._matrix) == initial_size - 1


def test_multiple_removals_compact() -> None:
    """Multiple vertex removals progressively compact matrix."""
    g = AdjacencyMatrixGraph()
    for i in range(5):
        g.add_vertex(i)

    assert len(g._matrix) == 5

    g.remove_vertex(0)
    assert len(g._matrix) == 4

    g.remove_vertex(1)
    assert len(g._matrix) == 3

    g.remove_vertex(2)
    assert len(g._matrix) == 2


# ══════════════════════════════════════════════════════════════════════════════
# Edge Cases & Complex Scenarios
# ══════════════════════════════════════════════════════════════════════════════


def test_complex_graph_operations() -> None:
    """Sequence of complex operations."""
    g = AdjacencyMatrixGraph()

    # Build a small network
    for v in range(1, 5):
        g.add_vertex(v)

    edges = [(1, 2), (1, 3), (2, 3), (3, 4), (2, 4)]
    for v1, v2 in edges:
        g.add_edge(v1, v2)

    # Verify
    assert len(g) == 4
    assert len(g.get_neighbors(1)) == 2
    assert len(g.get_neighbors(2)) == 3
    assert len(g.get_neighbors(3)) == 3
    assert len(g.get_neighbors(4)) == 2

    # Remove edge
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)
    assert len(g.get_neighbors(1)) == 1

    # Remove vertex (triggers matrix rebuild)
    g.remove_vertex(3)
    assert 3 not in g
    assert len(g) == 3


def test_mixed_type_vertices() -> None:
    """Graph can contain vertices of different types."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(42)
    g.add_vertex("string")
    g.add_vertex((1, 2))
    g.add_vertex(3.14)
    assert len(g) == 4


def test_large_matrix_graph() -> None:
    """Matrix graphs work with larger sizes."""
    g = AdjacencyMatrixGraph()

    # Add 50 vertices (not too large to avoid memory issues in testing)
    for i in range(50):
        g.add_vertex(i)

    # Add edges in a chain
    for i in range(49):
        g.add_edge(i, i + 1)

    assert len(g) == 50
    for i in range(49):
        assert g.has_edge(i, i + 1)


def test_directed_complete_graph() -> None:
    """Build a complete directed graph."""
    g = AdjacencyMatrixGraph(directed=True)

    vertices = [1, 2, 3, 4]
    for v1 in vertices:
        for v2 in vertices:
            if v1 != v2:
                g.add_edge(v1, v2)

    # Each vertex should have 3 outgoing edges
    for v in vertices:
        assert len(g.get_neighbors(v)) == 3


def test_undirected_complete_graph() -> None:
    """Build a complete undirected graph."""
    g = AdjacencyMatrixGraph(directed=False)

    vertices = [1, 2, 3, 4]
    for v1 in vertices:
        for v2 in vertices:
            if v1 < v2:
                g.add_edge(v1, v2)

    # Complete graph K4: each vertex has degree 3
    for v in vertices:
        assert len(g.get_neighbors(v)) == 3


def test_isolated_vertices() -> None:
    """Isolated vertices have no neighbors."""
    g = AdjacencyMatrixGraph()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(3, 4)

    assert len(g.get_neighbors(1)) == 0
    assert len(g.get_neighbors(2)) == 0
    assert len(g.get_neighbors(3)) == 1


def test_remove_and_readd_edge() -> None:
    """Remove and re-add edge."""
    g = AdjacencyMatrixGraph((1, 2))
    assert g.has_edge(1, 2)
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)


def test_remove_all_vertices_one_by_one() -> None:
    """Remove all vertices one by one."""
    g = AdjacencyMatrixGraph((1,), (2,), (3,))
    assert len(g) == 3
    g.remove_vertex(1)
    assert len(g) == 2
    g.remove_vertex(2)
    assert len(g) == 1
    g.remove_vertex(3)
    assert len(g) == 0
    assert len(g._matrix) == 0
