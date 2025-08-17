# D. Shichikuji And Power Grid

**Platform:** Codeforces  
**Problem ID:** D  
**URL:** https://codeforces.com/contest/1245/problem/D  

## Problem Description
<!-- Add problem description here -->

## Approach
The problem is solved using **Minimum Spanning Tree (MST)** with **Kruskal’s algorithm** and **Disjoint Set Union (DSU/Union-Find)**:
- Each city can either build a power station directly (edge from virtual node `0` to the city with cost `c[i]`) or connect to another city (edge between city `i` and `j` with cost = Manhattan distance × (k[i] + k[j])).
- Build all possible edges (station edges + city-to-city edges).
- Sort edges by cost and apply Kruskal’s algorithm:
  - If the edge connects a city to `0`, that city gets a power station.
  - Otherwise, connect the two cities.
- Keep track of total cost, built stations, and connections.

This ensures the minimum cost to power all cities.

## Complexity Analysis
- **Time Complexity:** O(n² log n)  
  - O(n²) edges generated.  
  - Sorting edges costs O(n² log n).  
  - Union-Find operations are near O(1).  
- **Space Complexity:** O(n²) for storing all edges.

## Files
- `solution.cpp` - C++ implementation  
