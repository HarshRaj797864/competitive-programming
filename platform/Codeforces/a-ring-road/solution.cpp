/*
Problem: One-Way Roads (Berland)
Platform: Codeforces
URL: https://codeforces.com/problemset/problem/25/C (variant)

Approach:
- Since roads form a ring, the only two possible strongly connected orientations are:
  1. Clockwise cycle
  2. Counterclockwise cycle
- For each road, check:
  - If it matches clockwise orientation → cost = 0
  - Else must reverse → add its cost
- Same for counterclockwise orientation.
- Answer = min(clockwise_total, counterclockwise_total)

Time Complexity: O(n)
Space Complexity: O(1)
*/

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    // clockwise cost and counterclockwise cost
    int cost_cw = 0, cost_ccw = 0;

    vector<tuple<int,int,int>> roads;

    for (int i = 0; i < n; i++) {
        int a, b, c;
        cin >> a >> b >> c;
        roads.push_back({a, b, c});
    }

    // Check each road
    for (auto [a, b, c] : roads) {
        // Clockwise: edge must go from a -> b in ring order
        // Let's define clockwise as (i -> i+1), with wrap (n -> 1)
        // Counterclockwise: reverse direction
        if ((a % n) + 1 == b) {
            // matches clockwise, so reversing for CCW
            cost_ccw += c;
        } else if ((b % n) + 1 == a) {
            // matches counterclockwise, so reversing for CW
            cost_cw += c;
        }
    }

    cout << min(cost_cw, cost_ccw) << "\n";

    return 0;
}
