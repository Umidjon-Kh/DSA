import pytest

from data_structures.graphs import EdgeListGraph

# ══════════════════════════════════════════════════════════════════════════════
# Initialization
# ══════════════════════════════════════════════════════════════════════════════


def test_init_empty() -> None:
    """Create empty undirected, unweighted graph."""
    g = EdgeListGraph()
    assert len(g) == 0
    assert not g
    assert g.get_vertices() == []
    assert g.get_edges() == []


def test_init_with_edges() -> None:
    """Create graph with edges."""
    g = EdgeListGraph((1, 2), (2, 3), (3, 1))
    assert len(g) == 3  # 3 edges
    assert sorted(g.get_vertices()) == [1, 2, 3]


def test_init_with_weighted_edges() -> None:
    """Create weighted graph with initial edges."""
    g = EdgeListGraph((1, 2, 0.5), (2, 3, 1.5), weighted=True)
    assert len(g) == 2  # 2 edges
    edges = g.get_edges()
    assert (1, 2, 0.5) in edges
    assert (2, 3, 1.5) in edges


def test_init_directed() -> None:
    """Create directed graph (edges are one-way)."""
    g = EdgeListGraph((1, 2), (2, 3), directed=True)
    assert g.has_edge(1, 2)
    assert not g.has_edge(2, 1)  # undirected would have both


def test_init_undirected() -> None:
    """Create undirected graph (edges are bidirectional)."""
    g = EdgeListGraph((1, 2), directed=False)
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)


def test_init_no_single_vertices() -> None:
    """Single-vertex tuples are not supported (vertices come from edges)."""
    with pytest.raises(ValueError, match="2 or 3 elements"):
        EdgeListGraph((1,))


def test_init_invalid_tuple_empty() -> None:
    """Empty tuples should raise ValueError."""
    with pytest.raises(ValueError, match="2 or 3 elements"):
        EdgeListGraph(())


def test_init_invalid_tuple_too_long() -> None:
    """Tuples with more than 3 elements should raise ValueError."""
    with pytest.raises(ValueError, match="2 or 3 elements"):
        EdgeListGraph((1, 2, 3, 4))


def test_init_invalid_non_tuple() -> None:
    """Non-tuple arguments should raise ValueError."""
    with pytest.raises(ValueError, match="2 or 3 elements"):
        EdgeListGraph([1, 2])  # type: ignore[test]


def test_init_weighted_without_weight_raises() -> None:
    """Weighted graph in init requires weight on all edges."""
    with pytest.raises(ValueError, match="weight must be provided"):
        EdgeListGraph((1, 2), weighted=True)


# ══════════════════════════════════════════════════════════════════════════════
# Edge Operations - Add
# ══════════════════════════════════════════════════════════════════════════════


def test_add_edge_unweighted() -> None:
    """Add unweighted edge."""
    g = EdgeListGraph()
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)
    assert len(g) == 1


def test_add_edge_directed() -> None:
    """In directed graph, edge is one-way."""
    g = EdgeListGraph(directed=True)
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_add_edge_undirected() -> None:
    """In undirected graph, edge is bidirectional."""
    g = EdgeListGraph(directed=False)
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)


def test_add_edge_weighted() -> None:
    """Add weighted edge (requires weighted=True)."""
    g = EdgeListGraph(weighted=True)
    g.add_edge(1, 2, 5.0)
    edges = g.get_edges()
    assert (1, 2, 5.0) in edges


def test_add_edge_duplicate_no_effect() -> None:
    """Adding duplicate edge does nothing."""
    g = EdgeListGraph()
    g.add_edge(1, 2)
    g.add_edge(1, 2)
    assert len(g) == 1


def test_add_edge_self_loop_raises() -> None:
    """Self-loops are not allowed."""
    g = EdgeListGraph()
    with pytest.raises(ValueError, match="Self-loops"):
        g.add_edge(1, 1)


def test_add_edge_weighted_no_weight_raises() -> None:
    """Weighted graph requires weight parameter."""
    g = EdgeListGraph(weighted=True)
    with pytest.raises(ValueError, match="weight must be provided"):
        g.add_edge(1, 2)


def test_add_edge_weighted_zero_is_valid() -> None:
    """Weight of 0 is valid (falsy but not None)."""
    g = EdgeListGraph(weighted=True)
    g.add_edge(1, 2, 0)
    edges = g.get_edges()
    assert (1, 2, 0) in edges


def test_add_edge_negative_weight() -> None:
    """Negative weights are allowed."""
    g = EdgeListGraph(weighted=True)
    g.add_edge(1, 2, -5.0)
    edges = g.get_edges()
    assert (1, 2, -5.0) in edges


def test_add_edge_string_vertices() -> None:
    """Edges can connect string vertices."""
    g = EdgeListGraph()
    g.add_edge("alice", "bob")
    assert g.has_edge("alice", "bob")


def test_add_edge_mixed_type_vertices() -> None:
    """Edges can connect vertices of different types."""
    g = EdgeListGraph()
    g.add_edge(1, "hello")
    g.add_edge("hello", (1, 2))
    assert g.has_edge(1, "hello")
    assert g.has_edge("hello", (1, 2))


def test_add_edge_increments_size() -> None:
    """Adding edges increments size."""
    g = EdgeListGraph()
    assert len(g) == 0
    g.add_edge(1, 2)
    assert len(g) == 1
    g.add_edge(2, 3)
    assert len(g) == 2
    g.add_edge(3, 4)
    assert len(g) == 3


# ══════════════════════════════════════════════════════════════════════════════
# Edge Operations - Remove
# ══════════════════════════════════════════════════════════════════════════════


def test_remove_edge_basic() -> None:
    """Remove an existing edge."""
    g = EdgeListGraph((1, 2))
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)
    assert len(g) == 0


def test_remove_edge_directed() -> None:
    """Removing directed edge only removes one direction."""
    g = EdgeListGraph((1, 2), directed=True)
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)


def test_remove_edge_undirected() -> None:
    """Removing edge in undirected graph removes it (stored once)."""
    g = EdgeListGraph((1, 2), directed=False)
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_remove_edge_undirected_reverse_direction() -> None:
    """Removing edge in undirected graph works with reverse direction."""
    g = EdgeListGraph((1, 2), directed=False)
    g.remove_edge(2, 1)  # remove in reverse
    assert not g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_remove_edge_nonexistent() -> None:
    """Removing nonexistent edge does nothing."""
    g = EdgeListGraph((1, 2))
    g.remove_edge(3, 4)  # doesn't raise
    assert len(g) == 1


def test_remove_edge_decrements_size() -> None:
    """Removing edge decrements size."""
    g = EdgeListGraph((1, 2), (2, 3), (3, 4))
    assert len(g) == 3
    g.remove_edge(2, 3)
    assert len(g) == 2


def test_remove_edge_removes_only_first_match() -> None:
    """Removing edge removes only the first matching edge."""
    g = EdgeListGraph()
    g.add_edge(1, 2)
    g.add_edge(1, 2)  # duplicate attempt (won't add)
    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)
    assert len(g) == 0


def test_remove_edge_multiple() -> None:
    """Remove multiple edges sequentially."""
    g = EdgeListGraph((1, 2), (2, 3), (3, 4))
    g.remove_edge(1, 2)
    assert len(g) == 2
    g.remove_edge(3, 4)
    assert len(g) == 1
    g.remove_edge(2, 3)
    assert len(g) == 0


# ══════════════════════════════════════════════════════════════════════════════
# Edge Operations - Query
# ══════════════════════════════════════════════════════════════════════════════


def test_has_edge_true() -> None:
    """has_edge returns True for existing edge."""
    g = EdgeListGraph((1, 2))
    assert g.has_edge(1, 2)


def test_has_edge_false() -> None:
    """has_edge returns False for non-existing edge."""
    g = EdgeListGraph((1, 2))
    assert not g.has_edge(1, 3)


def test_has_edge_directed_asymmetric() -> None:
    """In directed graph, edges are asymmetric."""
    g = EdgeListGraph((1, 2), directed=True)
    assert g.has_edge(1, 2)
    assert not g.has_edge(2, 1)


def test_has_edge_undirected_symmetric() -> None:
    """In undirected graph, has_edge is symmetric."""
    g = EdgeListGraph((1, 2), directed=False)
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)


def test_has_edge_empty_graph() -> None:
    """has_edge on empty graph returns False."""
    g = EdgeListGraph()
    assert not g.has_edge(1, 2)


def test_get_edges_empty() -> None:
    """get_edges() on empty graph returns empty list."""
    g = EdgeListGraph()
    assert g.get_edges() == []


def test_get_edges_single() -> None:
    """get_edges() returns single edge."""
    g = EdgeListGraph((1, 2))
    edges = g.get_edges()
    assert edges == [(1, 2, None)]


def test_get_edges_multiple() -> None:
    """get_edges() returns all edges."""
    g = EdgeListGraph((1, 2), (2, 3), (3, 4))
    edges = g.get_edges()
    assert len(edges) == 3
    assert (1, 2, None) in edges
    assert (2, 3, None) in edges
    assert (3, 4, None) in edges


def test_get_edges_weighted() -> None:
    """get_edges() includes weights."""
    g = EdgeListGraph((1, 2, 5.0), (2, 3, 10.0), weighted=True)
    edges = g.get_edges()
    assert (1, 2, 5.0) in edges
    assert (2, 3, 10.0) in edges


def test_get_edges_insertion_order() -> None:
    """get_edges() returns edges in insertion order."""
    g = EdgeListGraph()
    g.add_edge(3, 4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    edges = g.get_edges()
    assert edges[0] == (3, 4, None)
    assert edges[1] == (1, 2, None)
    assert edges[2] == (2, 3, None)


def test_get_vertices_empty() -> None:
    """get_vertices() on empty graph returns empty list."""
    g = EdgeListGraph()
    assert g.get_vertices() == []


def test_get_vertices_single_edge() -> None:
    """get_vertices() derives vertices from edges."""
    g = EdgeListGraph((1, 2))
    vertices = g.get_vertices()
    assert sorted(vertices) == [1, 2]


def test_get_vertices_multiple_edges() -> None:
    """get_vertices() returns all unique vertices."""
    g = EdgeListGraph((1, 2), (2, 3), (3, 4))
    vertices = g.get_vertices()
    assert sorted(vertices) == [1, 2, 3, 4]


def test_get_vertices_first_appearance_order() -> None:
    """get_vertices() ordered by first appearance."""
    g = EdgeListGraph()
    g.add_edge(3, 1)
    g.add_edge(2, 3)
    vertices = g.get_vertices()
    # 3 appears first (as v1), then 1, then 2
    assert vertices == [3, 1, 2]


def test_get_vertices_no_duplicates() -> None:
    """get_vertices() returns no duplicates."""
    g = EdgeListGraph((1, 2), (1, 3), (1, 4), (2, 3))
    vertices = g.get_vertices()
    assert len(vertices) == len(set(vertices))


def test_get_weight_unweighted() -> None:
    """get_weight() returns None for unweighted edges."""
    g = EdgeListGraph((1, 2))
    weight = g.get_weight(1, 2)
    assert weight is None


def test_get_weight_weighted() -> None:
    """get_weight() returns weight for weighted edges."""
    g = EdgeListGraph((1, 2, 5.0), weighted=True)
    weight = g.get_weight(1, 2)
    assert weight == 5.0


def test_get_weight_directed() -> None:
    """get_weight() respects direction in directed graphs."""
    g = EdgeListGraph((1, 2, 5.0), directed=True, weighted=True)
    assert g.get_weight(1, 2) == 5.0
    with pytest.raises(KeyError):
        g.get_weight(2, 1)


def test_get_weight_undirected() -> None:
    """get_weight() works both directions in undirected graphs."""
    g = EdgeListGraph((1, 2, 5.0), directed=False, weighted=True)
    assert g.get_weight(1, 2) == 5.0
    assert g.get_weight(2, 1) == 5.0


def test_get_weight_nonexistent_raises() -> None:
    """get_weight() raises KeyError for nonexistent edge."""
    g = EdgeListGraph((1, 2))
    with pytest.raises(KeyError):
        g.get_weight(1, 3)


def test_get_weight_zero() -> None:
    """get_weight() returns 0 (not falsy)."""
    g = EdgeListGraph((1, 2, 0), weighted=True)
    weight = g.get_weight(1, 2)
    assert weight == 0


def test_get_weight_negative() -> None:
    """get_weight() returns negative weights."""
    g = EdgeListGraph((1, 2, -10.5), weighted=True)
    weight = g.get_weight(1, 2)
    assert weight == -10.5


# ══════════════════════════════════════════════════════════════════════════════
# Collection Methods
# ══════════════════════════════════════════════════════════════════════════════


def test_clear_removes_all() -> None:
    """clear() removes all edges."""
    g = EdgeListGraph((1, 2), (2, 3), (3, 1))
    g.clear()
    assert len(g) == 0
    assert g.get_edges() == []
    assert g.get_vertices() == []


def test_clear_on_empty_graph() -> None:
    """clear() on empty graph does nothing."""
    g = EdgeListGraph()
    g.clear()
    assert len(g) == 0


def test_clear_resets_for_new_operations() -> None:
    """After clear(), graph is ready for new operations."""
    g = EdgeListGraph((1, 2))
    g.clear()
    g.add_edge(99, 100)
    assert len(g) == 1
    assert g.has_edge(99, 100)


def test_copy_creates_independent() -> None:
    """copy() creates independent copy."""
    g1 = EdgeListGraph((1, 2), (2, 3))
    g2 = g1.copy()

    # Modify g2
    g2.add_edge(3, 4)

    # g1 should be unchanged
    assert len(g1) == 2
    assert not g1.has_edge(3, 4)


def test_copy_preserves_directed() -> None:
    """copy() preserves directed flag."""
    g1 = EdgeListGraph((1, 2), directed=True)
    g2 = g1.copy()
    assert g2._directed == g1._directed


def test_copy_preserves_weighted() -> None:
    """copy() preserves weighted flag."""
    g1 = EdgeListGraph((1, 2, 5.0), weighted=True)
    g2 = g1.copy()
    assert g2._weighted == g1._weighted


def test_copy_preserves_edges() -> None:
    """copy() preserves all edges."""
    g1 = EdgeListGraph((1, 2), (2, 3), (3, 1))
    g2 = g1.copy()
    assert g2.has_edge(1, 2)
    assert g2.has_edge(2, 3)
    assert g2.has_edge(3, 1)


def test_copy_empty_graph() -> None:
    """copy() works on empty graph."""
    g1 = EdgeListGraph()
    g2 = g1.copy()
    assert len(g2) == 0


def test_copy_modifying_g2_does_not_affect_g1() -> None:
    """Modifications to copy don't affect original."""
    g1 = EdgeListGraph((1, 2, 5.0), weighted=True)
    g2 = g1.copy()

    g2.add_edge(2, 3, 10.0)
    g2.remove_edge(1, 2)

    assert len(g1) == 1
    assert g1.has_edge(1, 2)
    assert not g1.has_edge(2, 3)


def test_copy_is_independent_add_edge() -> None:
    """Modifying copy by adding edge does not affect original."""
    g1 = EdgeListGraph((1, 2), (2, 3))
    g2 = g1.copy()
    g2.add_edge(1, 3)
    assert g2.has_edge(1, 3)
    assert not g1.has_edge(1, 3)  # original unchanged


def test_copy_is_independent_remove_edge() -> None:
    """Modifying copy by removing edge does not affect original."""
    g1 = EdgeListGraph((1, 2), (2, 3))
    g2 = g1.copy()
    g2.remove_edge(1, 2)
    assert not g2.has_edge(1, 2)
    assert g1.has_edge(1, 2)  # original unchanged


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Size & Boolean
# ══════════════════════════════════════════════════════════════════════════════


def test_len_empty() -> None:
    """__len__() on empty graph is 0."""
    g = EdgeListGraph()
    assert len(g) == 0


def test_len_counts_edges_not_vertices() -> None:
    """__len__() returns edge count, not vertex count."""
    g = EdgeListGraph((1, 2), (1, 3), (1, 4))
    assert len(g) == 3  # 3 edges, 4 vertices


def test_len_with_edges() -> None:
    """__len__() returns edge count."""
    g = EdgeListGraph((1, 2), (2, 3), (3, 4))
    assert len(g) == 3


def test_bool_empty() -> None:
    """__bool__() on empty graph is False."""
    g = EdgeListGraph()
    assert not g


def test_bool_non_empty() -> None:
    """__bool__() with at least one edge is True."""
    g = EdgeListGraph((1, 2))
    assert g


def test_bool_multiple_edges() -> None:
    """__bool__() is True with multiple edges."""
    g = EdgeListGraph((1, 2), (2, 3))
    assert g


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Iteration
# ══════════════════════════════════════════════════════════════════════════════


def test_iter_empty() -> None:
    """__iter__() on empty graph yields nothing."""
    g = EdgeListGraph()
    assert list(g) == []


def test_iter_yields_edges_as_tuples() -> None:
    """__iter__() yields (v1, v2, weight) tuples."""
    g = EdgeListGraph((1, 2), (2, 3))
    edges = list(g)
    assert edges == [(1, 2, None), (2, 3, None)]


def test_iter_insertion_order() -> None:
    """__iter__() yields edges in insertion order."""
    g = EdgeListGraph()
    g.add_edge(3, 4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    edges = list(g)
    assert edges[0] == (3, 4, None)
    assert edges[1] == (1, 2, None)
    assert edges[2] == (2, 3, None)


def test_iter_weighted() -> None:
    """__iter__() includes weights in weighted graphs."""
    g = EdgeListGraph((1, 2, 5.0), (2, 3, 10.0), weighted=True)
    edges = list(g)
    assert (1, 2, 5.0) in edges
    assert (2, 3, 10.0) in edges


def test_reversed_empty() -> None:
    """__reversed__() on empty graph yields nothing."""
    g = EdgeListGraph()
    assert list(reversed(g)) == []


def test_reversed_order() -> None:
    """__reversed__() yields edges in reverse insertion order."""
    g = EdgeListGraph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    edges = list(reversed(g))
    assert edges[0] == (3, 4, None)
    assert edges[1] == (2, 3, None)
    assert edges[2] == (1, 2, None)


def test_reversed_single_edge() -> None:
    """__reversed__() with single edge."""
    g = EdgeListGraph((1, 2))
    edges = list(reversed(g))
    assert edges == [(1, 2, None)]


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Membership
# ══════════════════════════════════════════════════════════════════════════════


def test_contains_vertex_true() -> None:
    """__contains__() returns True for vertex in edge."""
    g = EdgeListGraph((1, 2))
    assert 1 in g
    assert 2 in g


def test_contains_vertex_false() -> None:
    """__contains__() returns False for missing vertex."""
    g = EdgeListGraph((1, 2))
    assert 3 not in g


def test_contains_empty_graph() -> None:
    """__contains__() on empty graph returns False."""
    g = EdgeListGraph()
    assert 1 not in g


def test_contains_vertex_as_v1() -> None:
    """__contains__() finds vertex as v1."""
    g = EdgeListGraph((1, 2))
    assert 1 in g


def test_contains_vertex_as_v2() -> None:
    """__contains__() finds vertex as v2."""
    g = EdgeListGraph((1, 2))
    assert 2 in g


def test_contains_multiple_edges() -> None:
    """__contains__() works with multiple edges."""
    g = EdgeListGraph((1, 2), (2, 3), (3, 4))
    assert 1 in g
    assert 2 in g
    assert 3 in g
    assert 4 in g
    assert 5 not in g


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Equality
# ══════════════════════════════════════════════════════════════════════════════


def test_eq_empty_graphs() -> None:
    """Two empty graphs are equal."""
    g1 = EdgeListGraph()
    g2 = EdgeListGraph()
    assert g1 == g2


def test_eq_same_edges() -> None:
    """Graphs with same edges are equal."""
    g1 = EdgeListGraph((1, 2), (2, 3))
    g2 = EdgeListGraph((1, 2), (2, 3))
    assert g1 == g2


def test_eq_different_edges() -> None:
    """Graphs with different edges are not equal."""
    g1 = EdgeListGraph((1, 2))
    g2 = EdgeListGraph((1, 3))
    assert g1 != g2


def test_eq_order_independent() -> None:
    """Equality is order-independent."""
    g1 = EdgeListGraph()
    g1.add_edge(1, 2)
    g1.add_edge(2, 3)

    g2 = EdgeListGraph()
    g2.add_edge(2, 3)
    g2.add_edge(1, 2)

    assert g1 == g2


def test_eq_directed_vs_undirected() -> None:
    """Directed and undirected graphs are not equal."""
    g1 = EdgeListGraph((1, 2), directed=False)
    g2 = EdgeListGraph((1, 2), directed=True)
    assert g1 != g2


def test_eq_weighted_vs_unweighted() -> None:
    """Weighted and unweighted graphs are not equal."""
    g1 = EdgeListGraph((1, 2, 5.0), weighted=True)
    g2 = EdgeListGraph((1, 2), weighted=False)
    assert g1 != g2


def test_eq_different_weights() -> None:
    """Graphs with different weights are not equal."""
    g1 = EdgeListGraph((1, 2, 5.0), weighted=True)
    g2 = EdgeListGraph((1, 2, 10.0), weighted=True)
    assert g1 != g2


def test_eq_non_graph_type() -> None:
    """Comparing with non-graph returns NotImplemented."""
    g = EdgeListGraph()
    result = g.__eq__([1, 2, 3])  # type: ignore[arg-type]
    assert result is NotImplemented


def test_eq_after_copy() -> None:
    """Copied graph equals original."""
    g1 = EdgeListGraph((1, 2, 5.0), (2, 3, 10.0), weighted=True)
    g2 = g1.copy()
    assert g1 == g2


def test_eq_different_edge_count() -> None:
    """Graphs with different number of edges are not equal."""
    g1 = EdgeListGraph((1, 2), (2, 3))
    g2 = EdgeListGraph((1, 2))
    assert g1 != g2


# ══════════════════════════════════════════════════════════════════════════════
# Dunder Methods - Representation
# ══════════════════════════════════════════════════════════════════════════════


def test_repr_format() -> None:
    """__repr__() returns correct format."""
    g = EdgeListGraph((1, 2), (2, 3), directed=True, weighted=False)
    repr_str = repr(g)
    assert "EdgeListGraph" in repr_str
    assert "edges=2" in repr_str
    assert "directed=True" in repr_str
    assert "weighted=False" in repr_str


def test_repr_empty() -> None:
    """__repr__() works on empty graph."""
    g = EdgeListGraph()
    repr_str = repr(g)
    assert "edges=0" in repr_str


def test_repr_contains_class_name() -> None:
    """__repr__() contains class name."""
    g = EdgeListGraph((1, 2))
    assert "EdgeListGraph" in repr(g)


# ══════════════════════════════════════════════════════════════════════════════
# Edge-List Specific Behavior
# ══════════════════════════════════════════════════════════════════════════════


def test_no_add_vertex_method() -> None:
    """EdgeListGraph has no add_vertex method."""
    g = EdgeListGraph()
    assert not hasattr(g, "add_vertex")


def test_no_remove_vertex_method() -> None:
    """EdgeListGraph has no remove_vertex method."""
    g = EdgeListGraph()
    assert not hasattr(g, "remove_vertex")


def test_vertices_derived_from_edges() -> None:
    """Vertices are derived from edges, not stored separately."""
    g = EdgeListGraph((1, 2), (2, 3), (3, 4))
    vertices = g.get_vertices()
    # Vertices should be exactly those in edges
    assert set(vertices) == {1, 2, 3, 4}


def test_edge_stored_once_undirected() -> None:
    """Undirected edges stored once, not both directions."""
    g = EdgeListGraph((1, 2), directed=False)
    edges = g.get_edges()
    # Should have exactly one edge (v1=1, v2=2)
    assert len(edges) == 1
    assert (1, 2, None) in edges
    # But has_edge works both ways
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)


def test_edge_list_stores_all_edges() -> None:
    """Edge list explicitly stores all edges."""
    g = EdgeListGraph((1, 2), (2, 1), directed=True)
    edges = g.get_edges()
    assert len(edges) == 2
    assert (1, 2, None) in edges
    assert (2, 1, None) in edges


def test_sparse_graph_efficient() -> None:
    """Edge list efficient for sparse graphs (no O(V²) matrix)."""
    g = EdgeListGraph()
    # Add just a few edges
    g.add_edge(1, 1000)
    g.add_edge(500, 2000)
    g.add_edge(100, 200)

    assert len(g) == 3
    assert 4 not in g


def test_large_vertex_ids() -> None:
    """Handles large vertex IDs efficiently."""
    g = EdgeListGraph()
    g.add_edge(1000000, 2000000)
    g.add_edge(2000000, 3000000)

    assert g.has_edge(1000000, 2000000)
    assert 1000000 in g


# ══════════════════════════════════════════════════════════════════════════════
# Edge Cases & Complex Scenarios
# ══════════════════════════════════════════════════════════════════════════════


def test_complex_graph_operations() -> None:
    """Sequence of complex operations."""
    g = EdgeListGraph()

    # Build edges
    edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
    for v1, v2 in edges:
        g.add_edge(v1, v2)

    # Verify
    assert len(g) == 4
    assert sorted(g.get_vertices()) == [1, 2, 3, 4]

    # Remove edge
    g.remove_edge(2, 3)
    assert not g.has_edge(2, 3)
    assert len(g) == 3

    # Add back
    g.add_edge(2, 3)
    assert g.has_edge(2, 3)
    assert len(g) == 4


def test_mixed_type_vertices() -> None:
    """Graph can contain vertices of different types."""
    g = EdgeListGraph()
    g.add_edge(42, "string")
    g.add_edge("string", (1, 2))
    g.add_edge((1, 2), 3.14)
    assert len(g) == 3
    assert 42 in g
    assert "string" in g
    assert (1, 2) in g
    assert 3.14 in g


def test_directed_cycle() -> None:
    """Build a directed cycle."""
    g = EdgeListGraph(directed=True)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)

    assert len(g) == 4
    assert g.has_edge(1, 2)
    assert g.has_edge(4, 1)
    assert not g.has_edge(2, 1)


def test_undirected_cycle() -> None:
    """Build an undirected cycle."""
    g = EdgeListGraph(directed=False)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)

    assert len(g) == 4
    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)
    assert g.has_edge(4, 1)
    assert g.has_edge(1, 4)


def test_weighted_directed_graph() -> None:
    """Weighted directed graph combination."""
    g = EdgeListGraph(directed=True, weighted=True)
    g.add_edge(1, 2, 5.0)
    g.add_edge(2, 1, 3.0)

    assert g.has_edge(1, 2)
    assert g.has_edge(2, 1)
    assert g.get_weight(1, 2) == 5.0
    assert g.get_weight(2, 1) == 3.0


def test_star_graph() -> None:
    """Star graph (all edges from center)."""
    g = EdgeListGraph()
    center = 0
    for i in range(1, 6):
        g.add_edge(center, i)

    assert len(g) == 5
    assert len(g.get_vertices()) == 6
    assert all(g.has_edge(center, i) for i in range(1, 6))


def test_path_graph() -> None:
    """Path graph (linear chain)."""
    g = EdgeListGraph()
    for i in range(5):
        g.add_edge(i, i + 1)

    assert len(g) == 5
    assert sorted(g.get_vertices()) == [0, 1, 2, 3, 4, 5]


def test_remove_all_edges() -> None:
    """Remove all edges one by one."""
    g = EdgeListGraph((1, 2), (2, 3), (3, 4))
    assert len(g) == 3

    g.remove_edge(1, 2)
    assert len(g) == 2

    g.remove_edge(2, 3)
    assert len(g) == 1

    g.remove_edge(3, 4)
    assert len(g) == 0
    assert g.get_vertices() == []


def test_add_remove_add_cycle() -> None:
    """Add, remove, then re-add edge."""
    g = EdgeListGraph()
    g.add_edge(1, 2)
    assert g.has_edge(1, 2)

    g.remove_edge(1, 2)
    assert not g.has_edge(1, 2)

    g.add_edge(1, 2)
    assert g.has_edge(1, 2)


def test_many_edges_same_vertices() -> None:
    """Cannot have multiple edges to same vertex (no multi-edges)."""
    g = EdgeListGraph()
    g.add_edge(1, 2)
    g.add_edge(1, 2)  # duplicate attempt
    assert len(g) == 1


def test_all_edge_types_combined() -> None:
    """Complex graph with various edge operations."""
    g = EdgeListGraph(directed=True, weighted=True)

    # Add weighted edges
    g.add_edge("a", "b", 1.5)
    g.add_edge("b", "c", 2.5)
    g.add_edge("c", "a", 3.5)

    assert len(g) == 3
    assert g.get_weight("a", "b") == 1.5
    assert g.get_weight("b", "c") == 2.5

    # Remove one
    g.remove_edge("b", "c")
    assert len(g) == 2

    # Add different
    g.add_edge("a", "c", 0.5)
    assert len(g) == 3
    assert g.get_weight("a", "c") == 0.5
