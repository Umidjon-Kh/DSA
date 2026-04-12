# Graphs

Three graph implementations split along one axis: **representation type** (adjacency list, adjacency matrix, or edge list). Each supports directed/undirected and weighted/unweighted variants.

```
graphs/
├── adjacency_list.py      # Hash map of DynamicUniversalArrays
├── adjacency_matrix.py    # 2D matrix backed by nested DynamicUniversalArrays
└── edge_list.py           # Flat DynamicUniversalArray of (v1, v2, weight) tuples
```

---

## What is a Graph?

A **graph** is a collection of **vertices** (also called nodes) connected by **edges** (also called links).

```
     1 --- 2        Vertices: 1, 2, 3, 4
    / \     \       Edges: (1,2), (1,3), (2,3), (3,4)
   3 --- 4

Undirected: edges work both ways → 1---2 means you can go 1→2 or 2→1
Directed:   edges work one way → 1→2 means you can go 1→2 only
Weighted:   edges have values → (1→2, weight=5)
```

---

## Quick Reference: When to Use Each?

| Class                | Best For                          | has_edge | add_vertex | add_edge | Space        |
| -------------------- | --------------------------------- | -------- | ---------- | -------- | ------------ |
| `AdjacencyListGraph` | **General use**, sparse graphs    | O(deg)   | O(1)       | O(1)     | O(V + E)     |
| `AdjacencyMatrixGraph` | **Dense graphs**, many queries   | O(1)     | O(V)       | O(1)     | O(V²)        |
| `EdgeListGraph`      | **Simple, edge-centric queries** | O(E)     | —          | O(E)     | O(E)         |

**Sparse graph**: few edges (E ≈ V) → prefer AdjacencyListGraph
**Dense graph**: many edges (E ≈ V²) → prefer AdjacencyMatrixGraph
**Edge-only**: no separate vertex operations → prefer EdgeListGraph

---

## Classes

### `AdjacencyListGraph(*args, directed=False, weighted=False)`

A graph backed by a hash map where each vertex points to an array of its neighbors.

**Ideal for**: most applications, especially sparse graphs.
**Trade-off**: checking if an edge exists requires scanning a neighbor list.

```python
g = AdjacencyListGraph()                           # empty
g = AdjacencyListGraph((1,), (2,), (3,))          # 3 isolated vertices
g = AdjacencyListGraph((1, 2), (2, 3))            # 1→2, 2→3
g = AdjacencyListGraph((1, 2, 5), weighted=True)  # 1→2 weight=5
g = AdjacencyListGraph((1, 2), directed=True)     # directed: 1→2 only

# Vertex operations
g.add_vertex(4)                          # add isolated vertex 4
g.remove_vertex(2)                       # remove vertex 2 and all its edges
v = g.get_vertices()                     # [1, 2, 3, 4]
4 in g                                   # True

# Edge operations
g.add_edge(1, 2)                         # add undirected edge 1-2
g.add_edge(2, 3, weight=10)              # weighted edge
g.remove_edge(1, 2)
g.has_edge(1, 2)                         # False
neighbors = g.get_neighbors(1)           # [(2, weight), (3, weight), ...]

# Collection operations
len(g)                                   # number of vertices
bool(g)                                  # True if graph is not empty
list(g)                                  # all vertices
copy = g.copy()
g.clear()
```

---

### `AdjacencyMatrixGraph(*args, directed=False, weighted=False)`

A graph backed by a 2D matrix where `matrix[i][j]` represents the edge from vertex i to vertex j.

**Ideal for**: dense graphs or frequent "is there an edge?" queries.
**Trade-off**: adding/removing vertices is O(V) or O(V²), uses O(V²) space always.

```python
g = AdjacencyMatrixGraph()
g = AdjacencyMatrixGraph((1,), (2,), (3,))        # 3 isolated vertices
g = AdjacencyMatrixGraph((1, 2), (2, 3))
g = AdjacencyMatrixGraph((1, 2, 5), weighted=True)
g = AdjacencyMatrixGraph((1, 2), directed=True)

# Vertex operations — same as AdjacencyListGraph
g.add_vertex(4)
g.remove_vertex(2)
v = g.get_vertices()
4 in g

# Edge operations — same interface as AdjacencyListGraph
g.add_edge(1, 2)
g.add_edge(2, 3, weight=10)
g.remove_edge(1, 2)
g.has_edge(1, 2)                         # O(1) — just a matrix lookup!
neighbors = g.get_neighbors(1)

# Collection operations
len(g)
bool(g)
list(g)
copy = g.copy()
g.clear()
```

**Key difference**: `has_edge()` is O(1) instead of O(degree).

---

### `EdgeListGraph(*args, directed=False, weighted=False)`

A graph backed by a flat list of edges. Vertices are derived from edges — there's no separate vertex registration.

**Ideal for**: algorithms that operate on edges directly (Kruskal's, Bellman-Ford).
**Trade-off**: checking if an edge exists scans the entire edge list. No `add_vertex()` or `remove_vertex()`.

```python
g = EdgeListGraph()
g = EdgeListGraph((1, 2), (2, 3))                   # 2 edges, 3 vertices derived
g = EdgeListGraph((1, 2, 5), weighted=True)
g = EdgeListGraph((1, 2), directed=True)

# Edge operations only — no separate vertex management
g.add_edge(1, 2)
g.add_edge(2, 3, weight=10)
g.remove_edge(1, 2)
g.has_edge(1, 2)                         # O(E) — must scan all edges
edges = g.get_edges()                    # [(1, 2, weight), ...]
vertices = g.get_vertices()              # derived from edges: [1, 2, 3]
w = g.get_weight(1, 2)                   # weight of edge (1, 2)

# NO add_vertex() or remove_vertex() — vertices exist only as edge endpoints

# Collection operations
len(g)                                   # number of EDGES (not vertices)
bool(g)
for v1, v2, weight in g:                 # iterates over edges
    print(v1, v2, weight)
copy = g.copy()
g.clear()
```

---

## Key Concepts

### Directed vs Undirected

```python
# Undirected (default)
g = AdjacencyListGraph((1, 2))
g.has_edge(1, 2)                         # True
g.has_edge(2, 1)                         # True — works both ways!

# Directed
g = AdjacencyListGraph((1, 2), directed=True)
g.has_edge(1, 2)                         # True
g.has_edge(2, 1)                         # False — one-way only
```

### Weighted vs Unweighted

```python
# Unweighted (default)
g = AdjacencyListGraph((1, 2))
neighbors = g.get_neighbors(1)
# → [(2, None)]                          weight is None

# Weighted
g = AdjacencyListGraph((1, 2, 10), weighted=True)
neighbors = g.get_neighbors(1)
# → [(2, 10)]                            weight is 10
```

### Self-loops

Self-loops (edge from a vertex to itself) are **not allowed**:

```python
g = AdjacencyListGraph()
g.add_edge(1, 1)                         # ValueError: Self-loops are not supported.
```

---

## Supported Operations

### `AdjacencyListGraph` and `AdjacencyMatrixGraph`

| Operation            | AdjacencyList | AdjacencyMatrix | Notes                              |
| -------------------- | ------------- | --------------- | ---------------------------------- |
| `add_vertex`         | O(1)          | O(V)            | AMG must resize matrix             |
| `remove_vertex`      | O(V + E)      | O(V²)           | AMG rebuilds entire matrix         |
| `add_edge`           | O(1)          | O(1) *          | only if vertices already exist     |
| `remove_edge`        | O(deg)        | O(1)            | degree of source vertex            |
| `has_edge`           | O(deg)        | O(1)            | **key difference**                 |
| `get_neighbors`      | O(deg)        | O(V)            | ALG scans array, AMG scans matrix  |
| `get_vertices`       | O(V)          | O(V)            |
| `clear`              | O(1)          | O(1)            |
| `copy`               | O(V + E)      | O(V²)           |
| `__len__`            | O(1)          | O(1)            | number of vertices                 |
| `__iter__`           | O(V)          | O(V)            | iterate over vertices              |
| `__contains__`       | O(1) avg      | O(1) avg        | checks if vertex exists            |
| `__eq__`             | O(V + E)      | O(V²)           |

* `add_edge` on AdjacencyMatrixGraph is O(V) if vertex doesn't exist yet (calls `add_vertex`).

### `EdgeListGraph`

| Operation       | EdgeListGraph | Notes                                    |
| --------------- | ------------- | ---------------------------------------- |
| `add_edge`      | O(E)          | duplicate check scans all edges          |
| `remove_edge`   | O(E)          |
| `has_edge`      | O(E)          |
| `get_edges`     | O(E)          |
| `get_vertices`  | O(E)          | derived from all edges                   |
| `get_weight`    | O(E)          | returns weight of specific edge          |
| `clear`         | O(1)          |
| `copy`          | O(E)          |
| `__len__`       | O(1)          | number of **edges** (not vertices)       |
| `__iter__`      | O(E)          | yields (v1, v2, weight) tuples           |
| `__contains__`  | O(E)          | checks if vertex appears in any edge     |
| `__eq__`        | O(E²)         | checks if edge sets match                 |

---

## Design Decisions

### No `add_vertex()` in EdgeListGraph

The edge list is fundamentally edge-centric. Vertices have no independent existence — they are derived from edges. If you need separate vertex management, use `AdjacencyListGraph` or `AdjacencyMatrixGraph`.

### Undirected edges stored once

In undirected graphs, each edge is stored **once** internally (not bidirectionally in EdgeListGraph):

```python
g = EdgeListGraph((1, 2))              # stored as (1, 2)
g.has_edge(1, 2)                       # True
g.has_edge(2, 1)                       # True — checked by flipping
```

In AdjacencyListGraph and AdjacencyMatrixGraph, undirected edges are stored in **both directions** for O(1) access in either direction.

### Tuples as Edge Specifications

All constructors accept tuples to specify vertices and edges:

```python
(v,)              # add isolated vertex (ALG/AMG only, not EdgeListGraph)
(v1, v2)          # add unweighted edge
(v1, v2, weight)  # add weighted edge (only if weighted=True)
```

This design is consistent with Arrays and Stacks for familiar initialization.

### Weight Handling

- **Unweighted**: edges stored with `weight=None`. `get_weight()` raises `KeyError` if edge doesn't exist.
- **Weighted**: edges stored with numeric weight. Creating a weighted graph without providing weights on every edge raises `ValueError`.

### `__repr__` Formats

```
AdjacencyListGraph(vertices=3, directed=False, weighted=True)
AdjacencyMatrixGraph(vertices=3, directed=False, weighted=True)
EdgeListGraph(edges=5, directed=False, weighted=True)
```

---

## Examples: Choosing the Right Implementation

### Sparse Social Network (1M users, 10M friendships)

V = 10⁶, E = 10⁷. A matrix would require 10¹² cells — not feasible.

```python
g = AdjacencyListGraph(directed=False)
for user_id, friend_id in friendship_pairs:
    g.add_edge(user_id, friend_id)
```

### Dense Weighted Road Network (50 cities, all connected)

V = 50, E ≈ 50² = 2500. A matrix is practical and O(1) edge lookups are useful.

```python
g = AdjacencyMatrixGraph(weighted=True)
for city_a, city_b, distance in city_distances:
    g.add_edge(city_a, city_b, distance)
# Later: O(1) check if direct road exists
if g.has_edge("NYC", "Boston"):
    ...
```

### Kruskal's Algorithm (minimum spanning tree)

Process edges in sorted order by weight. EdgeListGraph is ideal:

```python
g = EdgeListGraph(weighted=True)
edges = g.get_edges()
edges.sort(key=lambda e: e[2])  # sort by weight
for v1, v2, weight in edges:
    # Add to MST if it doesn't create a cycle
    ...
```

---

## Type Safety Notes

- All implementations accept `Any` Python object as a vertex — integers, strings, tuples, custom objects.
- Edges are compared by value (not identity) using `==`.
- The `directed` and `weighted` flags determine the **entire** graph behaviour — they cannot be changed after construction.
- Two graphs are equal only if they have identical vertices, edges, and constructor flags.

---

## Common Patterns

### Check if vertices are connected

```python
g = AdjacencyListGraph((1, 2), (2, 3), (3, 4))
print(g.has_edge(1, 2))    # True
print(g.has_edge(1, 3))    # False
```

### Get all neighbors of a vertex

```python
neighbors = g.get_neighbors(2)  # [(1, None), (3, None)]
for neighbor, weight in neighbors:
    print(neighbor)
```

### Iterate over all edges

```python
for v1, v2, w in g:           # EdgeListGraph yields (v1, v2, w)
    print(v1, "->", v2)
```

For AdjacencyListGraph or AdjacencyMatrixGraph, manually iterate:

```python
for vertex in g:
    for neighbor, weight in g.get_neighbors(vertex):
        print(vertex, "->", neighbor)
```

### Copy a graph

```python
original = AdjacencyListGraph((1, 2), (2, 3))
copy = original.copy()
copy.add_edge(3, 1)
len(original)   # 3 (unchanged)
len(copy)       # 3 (has new edge but same vertex count)
```
