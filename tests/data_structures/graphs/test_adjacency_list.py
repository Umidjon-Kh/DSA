import pytest

from data_structures.graphs import AdjacencyListGraph

# ══════════════════════════════════════════════════════════════════════════════
# Initialization
# ══════════════════════════════════════════════════════════════════════════════


def test_init_empty() -> None:
    """Create empty undirected, unweighted graph."""
    g = AdjacencyListGraph()
    assert len(g) == 0
    assert not g
    assert g.get_vertices() == []


def test_init_with_vertices() -> None:
    """Create graph with individual vertices."""
    g = AdjacencyListGraph((1,), (2,), (3,))
    assert len(g) == 3
    assert sorted(g.get_vertices()) == [1, 2, 3]


def test_init_with_edges() -> None:
    """Create graph with edges (vertices created automatically)."""
    g = AdjacencyListGraph((1, 2), (2, 3), (3, 1))
    assert len(g) == 3
    assert sorted(g.get_vertices()) == [1, 2, 3]


def test_init_with_weighted_edges() -> None:
    """Create weighted graph with initial edges."""
    g = AdjacencyListGraph((1, 2, 0.5), (2, 3, 1.5), weighted=True)
    assert len(g) == 3
    assert g.has_edge(1, 2)
    neighbors = g.get_neighbors(1)
    assert (2, 0.5) in neighbors


def test_init_directed() -> None:
    """Create directed graph (edges are one-way)."""
    g = AdjacencyListGraph((1, 2), (2, 3), directed=True)
    assert g.has_edge(1, 2)
    assert not g.has_edge(2, 1)  # undirected would have both


def test_init_undirected() -> None:
    """Create undirected graph (edges are bidirectional)."""
    g = AdjacencyListGraph((1, 2), directed=False)
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)


def test_init_mixed_vertices_and_edges() -> None:
    """Initialize with both individual vertices and edges."""
    g = AdjacencyListGraph((1,), (2, 3), (3, 4), (5,))
    assert len(g) == 5
    assert sorted(g.get_vertices()) == [1, 2, 3, 4, 5]


def test_init_invalid_tuple_empty() -> None:
    """Empty tuples should raise ValueError."""
    with pytest.raises(ValueError, match="non-empty tuple"):
        AdjacencyListGraph(())


def test_init_invalid_tuple_too_long() -> None:
    """Tuples with more than 3 elements should raise ValueError."""
    with pytest.raises(ValueError, match="1, 2, or 3 elements"):
        AdjacencyListGraph((1, 2, 3, 4))


def test_init_invalid_non_tuple() -> None:
    """Non-tuple arguments should raise ValueError."""
    with pytest.raises(ValueError, match="non-empty tuple"):
        AdjacencyListGraph([1, 2])  # type: ignore[test]


def test_init_weighted_with_tuple_weight() -> None:
    """Weighted graph stores tuple weights if provided."""
    g = AdjacencyListGraph((1, 2, (3, 4)), weighted=True)
    neighbors = g.get_neighbors(1)
    assert (2, (3, 4)) in neighbors


# ══════════════════════════════════════════════════════════════════════════════
# Vertex Operations - Add
# ══════════════════════════════════════════════════════════════════════════════


def test_add_vertex_single() -> None:
    """Add a single vertex to empty graph."""
    g = AdjacencyListGraph()
    g.add_vertex(1)
    assert len(g) == 1
    assert 1 in g


def test_add_vertex_multiple() -> None:
    """Add multiple vertices."""
    g = AdjacencyListGraph()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    assert len(g) == 3
    assert 1 in g and 2 in g and 3 in g


def test_add_vertex_duplicate_no_effect() -> None:
    """Adding duplicate vertex does nothing."""
    g = AdjacencyListGraph()
    g.add_vertex(1)
    g.add_vertex(1)
    assert len(g) == 1


def test_add_vertex_mixed_types() -> None:
    """Vertices can be of mixed types."""
    g = AdjacencyListGraph()
    g.add_vertex(1)
    g.add_vertex("a")
    g.add_vertex((1, 2))
    assert len(g) == 3


def test_add_vertex_string() -> None:
    """String vertices work."""
    g = AdjacencyListGraph()
    g.add_vertex("hello")
    g.add_vertex("world")
    assert "hello" in g
    assert "world" in g


def test_add_vertex_tuple_type() -> None:
    """Tuple can be a vertex (hashable)."""
    g = AdjacencyListGraph()
    g.add_vertex((1, 2))
    g.add_vertex((3, 4))
    assert (1, 2) in g


# ══════════════════════════════════════════════════════════════════════════════
# Vertex Operations - Remove
# ══════════════════════════════════════════════════════════════════════════════


def test_remove_vertex_single() -> None:
    """Remove a single vertex."""
    g = AdjacencyListGraph((1,), (2,), (3,))
    g.remove_vertex(2)
    assert len(g) == 2
    assert 2 not in g


def test_remove_vertex_with_edges() -> None:
    """Removing vertex removes all its edges."""
    g = AdjacencyListGraph((1, 2), (1, 3), (2, 3))
    g.remove_vertex(1)
    assert len(g) == 2
    assert not g.has_edge(1, 2)
    assert not g.has_edge(1, 3)
    assert g.has_edge(2, 3)  # this edge unaffected


def test_remove_vertex_nonexistent() -> None:
    """Removing nonexistent vertex does nothing."""
    g = AdjacencyListGraph((1,))
    g.remove_vertex(99)
    assert len(g) == 1


def test_remove_vertex_updates_adjacency() -> None:
    """After removal, removed vertex no longer in neighbor lists."""
    g = AdjacencyListGraph((1, 2), (2, 3), directed=False)
    g.remove_vertex(2)
    neighbors = g.get_neighbors(1)
    assert all(n[0] != 2 for n in neighbors)


def test_remove_vertex_directed() -> None:
    """Removing vertex removes outgoing and incoming edges in directed graph."""
    g = AdjacencyListGraph((1, 2), (2, 3), (3, 1), directed=True)
    g.remove_vertex(2)
    assert not g.has_edge(1, 2)
    assert not g.has_edge(2, 3)
    assert g.has_edge(3, 1)


def test_remove_vertex_from_empty() -> None:
    """Removing from empty graph is safe."""
    g = AdjacencyListGraph()
    g.remove_vertex(1)
    assert len(g) == 0


# ══════════════════════════════════════════════════════════════════════════════
# Vertex Operations - Query
# ══════════════════════════════════════════════════════════════════════════════


def test_get_vertices_empty() -> None:
    """get_vertices() on empty graph returns empty list."""
    g = AdjacencyListGraph()
    assert g.get_vertices() == []


def test_get_vertices_returns_list() -> None:
    """get_vertices() returns list of all vertices."""
    g = AdjacencyListGraph((1,), (2,), (3,))
    vertices = g.get_vertices()
    assert sorted(vertices) == [1, 2, 3]


def test_get_vertices_single() -> None:
    """get_vertices() with single vertex."""
    g = AdjacencyListGraph((1,))
    vertices = g.get_vertices()
    assert vertices == [1]


def test_get_vertices_from_edges() -> None:
    """get_vertices() includes vertices from edges."""
    g = AdjacencyListGraph((1, 2), (3, 4))
    vertices = sorted(g.get_vertices())
    assert vertices == [1, 2, 3, 4]


# ══════════════════════════════════════════════════════════════════════════════
# Edge Operations - Add
# ══════════════════════════════════════════════════════════════════════════════


def test_add_edge_creates_vertices() -> None:
    """Adding edge creates vertices if they don't exist."""
    g = AdjacencyListGraph()
    g.add_edge(1, 2)
    assert len(g) == 2
    assert 1 in g and 2 in g


def test_add_edge_unweighted() -> None:
    """Add unweighted edge."""
    g = AdjacencyListGraph()
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)
    neighbors = g.get_neighbors(1)
    assert (2, None) in neighbors


def test_add_edge_directed() -> None:
    """In directed graph, edge is one-way."""
    g = AdjacencyListGraph(directed=True)
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_add_edge_undirected() -> None:
    """In undirected graph, edge is bidirectional."""
    g = AdjacencyListGraph(directed=False)
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)


def test_add_edge_weighted() -> None:
    """Add weighted edge (requires weighted=True)."""
    g = AdjacencyListGraph(weighted=True)
    g.add_edge(1, 2, 5.0)
    neighbors = g.get_neighbors(1)
    assert (2, 5.0) in neighbors


def test_add_edge_duplicate_no_effect() -> None:
    """Adding duplicate edge does nothing."""
    g = AdjacencyListGraph()
    g.add_edge(1, 2)
    neighbors_before = len(g.get_neighbors(1))
    g.add_edge(1, 2)
    neighbors_after = len(g.get_neighbors(1))
    assert neighbors_before == neighbors_after


def test_add_edge_self_loop_raises() -> None:
    """Self-loops are not allowed."""
    g = AdjacencyListGraph()
    with pytest.raises(ValueError, match="Self-loops"):
        g.add_edge(1, 1)


def test_add_edge_weighted_no_weight_raises() -> None:
    """Weighted graph requires weight parameter."""
    g = AdjacencyListGraph(weighted=True)
    with pytest.raises(ValueError, match="weight must be provided"):
        g.add_edge(1, 2)


def test_add_edge_weighted_zero_is_valid() -> None:
    """Weight of 0 is valid (falsy but not None)."""
    g = AdjacencyListGraph(weighted=True)
    g.add_edge(1, 2, 0)
    neighbors = g.get_neighbors(1)
    assert (2, 0) in neighbors


def test_add_edge_negative_weight() -> None:
    """Negative weights are allowed."""
    g = AdjacencyListGraph(weighted=True)
    g.add_edge(1, 2, -5.0)
    neighbors = g.get_neighbors(1)
    assert (2, -5.0) in neighbors


def test_add_edge_string_vertices() -> None:
    """Edges can connect string vertices."""
    g = AdjacencyListGraph()
    g.add_edge("alice", "bob")
    assert g.has_edge("alice", "bob")


def test_add_edge_mixed_type_vertices() -> None:
    """Edges can connect vertices of different types."""
    g = AdjacencyListGraph()
    g.add_edge(1, "hello")
    g.add_edge("hello", (1, 2))
    assert g.has_edge(1, "hello")
    assert g.has_edge("hello", (1, 2))


# ══════════════════════════════════════════════════════════════════════════════
# Edge Operations - Remove & Query
# ══════════════════════════════════════════════════════════════════════════════


def test_remove_edge_basic() -> None:
    """Remove an existing edge."""
    g = AdjacencyListGraph((1, 2))
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)


def test_remove_edge_directed() -> None:
    """Removing directed edge only removes one direction."""
    g = AdjacencyListGraph((1, 2), directed=True)
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)


def test_remove_edge_undirected() -> None:
    """Removing edge in undirected graph removes both directions."""
    g = AdjacencyListGraph((1, 2), directed=False)
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_remove_edge_nonexistent() -> None:
    """Removing nonexistent edge does nothing."""
    g = AdjacencyListGraph((1,), (2,))
    g.remove_edge(1, 2)  # doesn't raise
    assert len(g) == 2


def test_remove_edge_missing_vertex() -> None:
    """Removing edge with missing vertex does nothing."""
    g = AdjacencyListGraph((1, 2))
    g.remove_edge(1, 99)
    assert len(g) == 2


def test_remove_edge_weighted() -> None:
    """Removing weighted edge works."""
    g = AdjacencyListGraph((1, 2, 5.0), weighted=True)
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)


def test_has_edge_true() -> None:
    """has_edge returns True for existing edge."""
    g = AdjacencyListGraph((1, 2))
    assert g.has_edge(1, 2)


def test_has_edge_false() -> None:
    """has_edge returns False for non-existing edge."""
    g = AdjacencyListGraph((1,), (2,))
    assert not g.has_edge(1, 2)


def test_has_edge_directed_asymmetric() -> None:
    """In directed graph, edges are asymmetric."""
    g = AdjacencyListGraph((1, 2), directed=True)
    assert g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_has_edge_undirected_symmetric() -> None:
    """In undirected graph, edges are symmetric."""
    g = AdjacencyListGraph((1, 2), directed=False)
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)


def test_has_edge_missing_vertex() -> None:
    """has_edge returns False if vertex missing."""
    g = AdjacencyListGraph((1,))
    assert not g.has_edge(1, 99)
    assert not g.has_edge(99, 1)


def test_has_edge_self() -> None:
    """has_edge returns False for self-loops (not allowed)."""
    g = AdjacencyListGraph((1,))
    assert not g.has_edge(1, 1)


# ══════════════════════════════════════════════════════════════════════════════
# Neighbors & Weights
# ══════════════════════════════════════════════════════════════════════════════


def test_get_neighbors_single() -> None:
    """get_neighbors returns list with one neighbor."""
    g = AdjacencyListGraph((1, 2))
    neighbors = g.get_neighbors(1)
    assert neighbors == [(2, None)]


def test_get_neighbors_multiple() -> None:
    """get_neighbors returns all neighbors."""
    g = AdjacencyListGraph((1, 2), (1, 3), (1, 4))
    neighbors = g.get_neighbors(1)
    neighbors_set = set(neighbors)
    assert (2, None) in neighbors_set
    assert (3, None) in neighbors_set
    assert (4, None) in neighbors_set
    assert len(neighbors) == 3


def test_get_neighbors_empty() -> None:
    """get_neighbors returns empty list for isolated vertex."""
    g = AdjacencyListGraph((1,))
    neighbors = g.get_neighbors(1)
    assert neighbors == []


def test_get_neighbors_weighted() -> None:
    """get_neighbors includes weights in weighted graph."""
    g = AdjacencyListGraph((1, 2, 5.0), (1, 3, 10.0), weighted=True)
    neighbors = g.get_neighbors(1)
    neighbors_set = set(neighbors)
    assert (2, 5.0) in neighbors_set
    assert (3, 10.0) in neighbors_set


def test_get_neighbors_nonexistent_raises() -> None:
    """get_neighbors raises KeyError for nonexistent vertex."""
    g = AdjacencyListGraph()
    with pytest.raises(KeyError):
        g.get_neighbors(99)


def test_get_neighbors_directed_asymmetric() -> None:
    """Neighbors differ by direction in directed graph."""
    g = AdjacencyListGraph((1, 2), (2, 1), directed=True)
    neighbors_1 = g.get_neighbors(1)
    neighbors_2 = g.get_neighbors(2)
    assert (2, None) in neighbors_1
    assert (1, None) in neighbors_2
    assert (1, None) not in neighbors_1
    assert (2, None) not in neighbors_2


def test_get_neighbors_zero_weight() -> None:
    """get_neighbors with zero weight."""
    g = AdjacencyListGraph((1, 2, 0), weighted=True)
    neighbors = g.get_neighbors(1)
    assert (2, 0) in neighbors


def test_get_neighbors_mixed_weights() -> None:
    """get_neighbors with mixed positive and negative weights."""
    g = AdjacencyListGraph((1, 2, -5.0), (1, 3, 0), (1, 4, 10.5), weighted=True)
    neighbors = set(g.get_neighbors(1))
    assert (2, -5.0) in neighbors
    assert (3, 0) in neighbors
    assert (4, 10.5) in neighbors


# ══════════════════════════════════════════════════════════════════════════════
# Collection Methods
# ══════════════════════════════════════════════════════════════════════════════


def test_clear_removes_all() -> None:
    """clear() removes all vertices and edges."""
    g = AdjacencyListGraph((1, 2), (2, 3), (3, 1))
    g.clear()
    assert len(g) == 0
    assert g.get_vertices() == []


def test_clear_on_empty_graph() -> None:
    """clear() on empty graph does nothing."""
    g = AdjacencyListGraph()
    g.clear()
    assert len(g) == 0


def test_clear_resets_for_new_operations() -> None:
    """After clear(), graph is ready for new operations."""
    g = AdjacencyListGraph((1, 2))
    g.clear()
    g.add_vertex(99)
    assert 99 in g
    assert len(g) == 1


def test_copy_preserves_directed() -> None:
    """copy() preserves directed flag."""
    g1 = AdjacencyListGraph((1, 2), directed=True)
    g2 = g1.copy()
    assert g2._directed == g1._directed


def test_copy_preserves_weighted() -> None:
    """copy() preserves weighted flag."""
    g1 = AdjacencyListGraph((1, 2, 5.0), weighted=True)
    g2 = g1.copy()
    assert g2._weighted == g1._weighted


def test_copy_preserves_edges() -> None:
    """copy() preserves all edges."""
    g1 = AdjacencyListGraph((1, 2), (2, 3), (3, 1))
    g2 = g1.copy()
    assert g2.has_edge(1, 2)
    assert g2.has_edge(2, 3)
    assert g2.has_edge(3, 1)


def test_copy_empty_graph() -> None:
    """copy() works on empty graph."""
    g1 = AdjacencyListGraph()
    g2 = g1.copy()
    assert len(g2) == 0


def test_copy_large_graph() -> None:
    """copy() works on large graphs."""
    g1 = AdjacencyListGraph()
    for i in range(50):
        g1.add_vertex(i)
    for i in range(49):
        g1.add_edge(i, i + 1)

    g2 = g1.copy()
    assert len(g2) == 50
    for i in range(49):
        assert g2.has_edge(i, i + 1)


def test_copy_is_independent_add_edge() -> None:
    """Modifying copy by adding edge does not affect original."""
    g1 = AdjacencyListGraph((1, 2), (2, 3))
    g2 = g1.copy()
    g2.add_edge(1, 3)
    assert g2.has_edge(1, 3)
    assert not g1.has_edge(1, 3)  # original unchanged


def test_copy_is_independent_remove_edge() -> None:
    """Modifying copy by removing edge does not affect original."""
    g1 = AdjacencyListGraph((1, 2), (2, 3))
    g2 = g1.copy()
    g2.remove_edge(1, 2)
    assert not g2.has_edge(1, 2)
    assert g1.has_edge(1, 2)  # original unchanged


def test_copy_is_independent_add_vertex() -> None:
    """Modifying copy by adding vertex does not affect original."""
    g1 = AdjacencyListGraph((1, 2))
    g2 = g1.copy()
    g2.add_vertex(3)
    assert 3 in g2
    assert 3 not in g1  # original unchanged


def test_copy_is_independent_remove_vertex() -> None:
    """Modifying copy by removing vertex does not affect original."""
    g1 = AdjacencyListGraph((1,), (2,), (3,))
    g2 = g1.copy()
    g2.remove_vertex(3)
    assert 3 not in g2
    assert 3 in g1  # original unchanged


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Size & Boolean
# ══════════════════════════════════════════════════════════════════════════════


def test_len_empty() -> None:
    """__len__() on empty graph is 0."""
    g = AdjacencyListGraph()
    assert len(g) == 0


def test_len_with_vertices() -> None:
    """__len__() returns vertex count."""
    g = AdjacencyListGraph((1,), (2,), (3,))
    assert len(g) == 3


def test_len_with_edges_only() -> None:
    """__len__() counts vertices, not edges."""
    g = AdjacencyListGraph((1, 2), (1, 3), (1, 4))
    assert len(g) == 4


def test_bool_empty() -> None:
    """__bool__() on empty graph is False."""
    g = AdjacencyListGraph()
    assert not g


def test_bool_non_empty() -> None:
    """__bool__() on non-empty graph is True."""
    g = AdjacencyListGraph((1,))
    assert g


def test_bool_with_edges_only() -> None:
    """__bool__() is True if graph has edges (vertices exist)."""
    g = AdjacencyListGraph((1, 2))
    assert g


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Iteration
# ══════════════════════════════════════════════════════════════════════════════


def test_iter_empty() -> None:
    """__iter__() on empty graph yields nothing."""
    g = AdjacencyListGraph()
    assert list(g) == []


def test_iter_yields_all_vertices() -> None:
    """__iter__() yields all vertices."""
    g = AdjacencyListGraph((1,), (2,), (3,))
    vertices = list(g)
    assert sorted(vertices) == [1, 2, 3]


def test_iter_single_vertex() -> None:
    """__iter__() with single vertex."""
    g = AdjacencyListGraph((1,))
    vertices = list(g)
    assert vertices == [1]


def test_reversed_empty() -> None:
    """__reversed__() on empty graph yields nothing."""
    g = AdjacencyListGraph()
    assert list(reversed(g)) == []


def test_reversed_order() -> None:
    """__reversed__() yields vertices in reverse."""
    g = AdjacencyListGraph()
    for i in [1, 2, 3]:
        g.add_vertex(i)
    vertices = list(reversed(g))
    assert set(vertices) == {1, 2, 3}


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Membership
# ══════════════════════════════════════════════════════════════════════════════


def test_contains_true() -> None:
    """__contains__() returns True for existing vertex."""
    g = AdjacencyListGraph((1,))
    assert 1 in g


def test_contains_false() -> None:
    """__contains__() returns False for missing vertex."""
    g = AdjacencyListGraph((1,))
    assert 2 not in g


def test_contains_empty_graph() -> None:
    """__contains__() on empty graph returns False."""
    g = AdjacencyListGraph()
    assert 1 not in g


def test_contains_various_types() -> None:
    """__contains__() works with various types."""
    g = AdjacencyListGraph()
    g.add_vertex("hello")
    g.add_vertex((1, 2))
    assert "hello" in g
    assert (1, 2) in g


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Equality
# ══════════════════════════════════════════════════════════════════════════════


def test_eq_empty_graphs() -> None:
    """Two empty graphs are equal."""
    g1 = AdjacencyListGraph()
    g2 = AdjacencyListGraph()
    assert g1 == g2


def test_eq_same_vertices() -> None:
    """Graphs with same vertices are equal."""
    g1 = AdjacencyListGraph((1,), (2,), (3,))
    g2 = AdjacencyListGraph((1,), (2,), (3,))
    assert g1 == g2


def test_eq_same_edges() -> None:
    """Graphs with same edges are equal."""
    g1 = AdjacencyListGraph((1, 2), (2, 3))
    g2 = AdjacencyListGraph((1, 2), (2, 3))
    assert g1 == g2


def test_eq_different_vertices() -> None:
    """Graphs with different vertices are not equal."""
    g1 = AdjacencyListGraph((1,), (2,))
    g2 = AdjacencyListGraph((1,), (3,))
    assert g1 != g2


def test_eq_different_edges() -> None:
    """Graphs with different edges are not equal."""
    g1 = AdjacencyListGraph((1, 2))
    g2 = AdjacencyListGraph((1, 3))
    assert g1 != g2


def test_eq_directed_vs_undirected() -> None:
    """Directed and undirected graphs are not equal."""
    g1 = AdjacencyListGraph((1, 2), directed=False)
    g2 = AdjacencyListGraph((1, 2), directed=True)
    assert g1 != g2


def test_eq_weighted_vs_unweighted() -> None:
    """Weighted and unweighted graphs are not equal."""
    g1 = AdjacencyListGraph((1, 2, 5.0), weighted=True)
    g2 = AdjacencyListGraph((1, 2), weighted=False)
    assert g1 != g2


def test_eq_different_weights() -> None:
    """Graphs with different weights are not equal."""
    g1 = AdjacencyListGraph((1, 2, 5.0), weighted=True)
    g2 = AdjacencyListGraph((1, 2, 10.0), weighted=True)
    assert g1 != g2


def test_eq_non_graph_type() -> None:
    """Comparing with non-graph returns NotImplemented."""
    g = AdjacencyListGraph()
    result = g.__eq__([1, 2, 3])  # type: ignore[arg-type]
    assert result is NotImplemented


def test_eq_after_copy() -> None:
    """Copied graph equals original."""
    g1 = AdjacencyListGraph((1, 2, 5.0), (2, 3, 10.0), weighted=True)
    g2 = g1.copy()
    assert g1 == g2


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Representation
# ══════════════════════════════════════════════════════════════════════════════


def test_repr_format() -> None:
    """__repr__() returns correct format."""
    g = AdjacencyListGraph((1,), (2,), directed=True, weighted=True)
    repr_str = repr(g)
    assert "AdjacencyListGraph" in repr_str
    assert "vertices=2" in repr_str
    assert "directed=True" in repr_str
    assert "weighted=True" in repr_str


def test_repr_empty() -> None:
    """__repr__() works on empty graph."""
    g = AdjacencyListGraph()
    repr_str = repr(g)
    assert "vertices=0" in repr_str


def test_repr_contains_class_name() -> None:
    """__repr__() contains class name."""
    g = AdjacencyListGraph((1,))
    assert "AdjacencyListGraph" in repr(g)


# ══════════════════════════════════════════════════════════════════════════════
# Edge Cases & Complex Scenarios
# ══════════════════════════════════════════════════════════════════════════════


def test_complex_graph_operations() -> None:
    """Sequence of complex operations."""
    g = AdjacencyListGraph()

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

    # Remove vertex
    g.remove_vertex(3)
    assert 3 not in g
    assert len(g) == 3


def test_mixed_type_vertices() -> None:
    """Graph can contain vertices of different types."""
    g = AdjacencyListGraph()
    g.add_vertex(42)
    g.add_vertex("string")
    g.add_vertex((1, 2))
    g.add_vertex(3.14)
    assert len(g) == 4


def test_large_graph() -> None:
    """Can create and operate on larger graphs."""
    g = AdjacencyListGraph()

    # Add 100 vertices
    for i in range(100):
        g.add_vertex(i)

    # Add edges in a chain
    for i in range(99):
        g.add_edge(i, i + 1)

    assert len(g) == 100
    for i in range(99):
        assert g.has_edge(i, i + 1)


def test_directed_complete_graph() -> None:
    """Build a complete directed graph."""
    g = AdjacencyListGraph(directed=True)

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
    g = AdjacencyListGraph(directed=False)

    vertices = [1, 2, 3, 4]
    for v1 in vertices:
        for v2 in vertices:
            if v1 < v2:  # avoid duplicates
                g.add_edge(v1, v2)

    # Complete graph K4: each vertex has degree 3
    for v in vertices:
        assert len(g.get_neighbors(v)) == 3


def test_isolated_vertices() -> None:
    """Isolated vertices have no neighbors."""
    g = AdjacencyListGraph()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(3, 4)

    assert len(g.get_neighbors(1)) == 0
    assert len(g.get_neighbors(2)) == 0
    assert len(g.get_neighbors(3)) == 1


def test_multiple_edges_to_same_vertex() -> None:
    """Cannot add multiple edges to same vertex (no multi-edges)."""
    g = AdjacencyListGraph()
    g.add_edge(1, 2)
    g.add_edge(1, 2)  # duplicate
    assert len(g.get_neighbors(1)) == 1


def test_weighted_directed_graph() -> None:
    """Weighted directed graph combinations."""
    g = AdjacencyListGraph(directed=True, weighted=True)
    g.add_edge(1, 2, 5.0)
    g.add_edge(2, 1, 3.0)

    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)
    neighbors_1 = dict(g.get_neighbors(1))
    neighbors_2 = dict(g.get_neighbors(2))
    assert neighbors_1[2] == 5.0
    assert neighbors_2[1] == 3.0


def test_remove_and_readd_edge() -> None:
    """Remove and re-add edge."""
    g = AdjacencyListGraph((1, 2))
    assert g.has_edge(1, 2)
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)


def test_remove_all_vertices_one_by_one() -> None:
    """Remove all vertices one by one."""
    g = AdjacencyListGraph((1,), (2,), (3,))
    assert len(g) == 3
    g.remove_vertex(1)
    assert len(g) == 2
    g.remove_vertex(2)
    assert len(g) == 1
    g.remove_vertex(3)
    assert len(g) == 0
