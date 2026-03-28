# Changelog

All notable changes to the **DSA Library** project will be documented in this file.

## [Unreleased]

### 💡 Planned Architectural Changes (Next Steps)

- **Implement Comparison Strategy Pattern**:
    - Refactor `BaseHeap` and `BasePriorityQueue` to accept a `comparator` function or a `_compare` abstract method.
    - **Goal**: Eliminate code duplication between `MinHeap` and `MaxHeap`.
    - **Logic**: Instead of hardcoding `a < b` or `a > b`, the core algorithms (`sift_up`, `sift_down`) will call a single comparison interface.
    - **Benefit**: This allows the core "engine" of the data structure to remain unchanged while only the sorting logic is swapped.

### 🏗 In Progress

- Developing `StaticTypedMinHeap` with $O(n)$ `heapify` (Floyd's Algorithm).
- Setting up the **Facade** interface for the `data_structures.arrays` module to simplify class instantiation.
- Integrating `StaticTypedArray` as the primary back-end for bounded structures.

## [0.1.0] - 2024-05-20 (Example Date)

### Added

- Initial project structure with `_base` and `_tools` modules.
- `StaticTypedMinHeap` implementation with `push`, `pop`, and `peek` operations.
- `validate_capacity` and `validate_value_type` utility helpers.
- `__slots__` optimization for all core data structures to reduce memory footprint.

### Changed

- Refactored `heapify` to support adding elements to an existing heap without overwriting current data.
