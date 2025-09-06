# C Mail Stamps

**Platform:** Codeforces  
**Problem ID:** 29C  
**URL:** [https://codeforces.com/contest/29/problem/C](https://codeforces.com/contest/29/problem/C)

---

## Problem Description
Bob received a letter with `n` postal stamps.  
Each stamp represents that the letter was sent directly between two cities `A` and `B` (either marked `A B` or `B A`).  
If a direct delivery is not possible, the letter is routed through intermediate cities.  
No city is visited more than once.  

The stamps on the envelope correspond to a valid simple path between two cities.  
Bob wants to reconstruct one of the possible routes of the letter.

**Input**  
- Integer `n` — number of stamps (`1 ≤ n ≤ 1e5`).  
- Next `n` lines: two integers — cities connected by a stamp (`1 ≤ city ≤ 1e9`).  

**Output**  
- Print one valid sequence of cities representing the route.

---

## Approach
1. Treat each stamp as an **undirected edge** between two cities.  
2. Build an adjacency list using hash maps (since city indices can be as large as `1e9`).  
3. Count the degree of each city. The **two cities with degree = 1** are the endpoints of the route.  
4. Pick one endpoint as the start and perform **DFS** (or BFS) to reconstruct the path.  
5. Print the path.  

---

## Complexity Analysis
- **Time Complexity:** `O(n)` — each edge and node visited once.  
- **Space Complexity:** `O(n)` — adjacency list and visited set.  

---

## Files
- `solution.cpp` - C++ implementation  

