# A Ring Road

**Platform:** Codeforces  
**Problem ID:** A  
**URL:** https://codeforces.com/problemset/problem/25/A (Ring Road variant)

---

## Problem Description
Berland has `n` cities arranged in a ring, connected by `n` roads.  
Originally, each road was two-way, but now the government introduced **one-way traffic** on all roads.  
Unfortunately, this made it impossible to travel from some cities to others.  

For each road, we know:
- Its current direction (`ai → bi`)
- The cost `ci` of reversing it  

We need to determine the **minimum cost of reversals** so that it becomes possible to travel from **any city to any other** (i.e., the graph becomes strongly connected).

---

## Approach
1. Since the roads form a cycle, the only two possible strongly connected orientations are:
   - **Clockwise cycle**
   - **Counterclockwise cycle**

2. For each road:
   - If it already matches the clockwise orientation, no cost for clockwise but cost `ci` for counterclockwise.
   - If it matches the counterclockwise orientation, no cost for counterclockwise but cost `ci` for clockwise.

3. Compute the total cost for both possible orientations:
   - `cost_cw` = cost of converting everything to clockwise
   - `cost_ccw` = cost of converting everything to counterclockwise

4. The answer is `min(cost_cw, cost_ccw)`.

---

## Complexity Analysis
- **Time Complexity:** `O(n)` — each road is checked once.  
- **Space Complexity:** `O(n)` — to store the roads.  

---

## Files
- `solution.cpp` - C++ implementation  

