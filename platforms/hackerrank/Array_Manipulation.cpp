/*
HackerRank #Array Manipulation: Array Manipulation
Tags: prefix sum, difference array, range update
Difficulty: Medium
URL: https://www.hackerrank.com/challenges/crush/problem

Approach:
1. Use a difference array to apply range additions in O(1) time.
2. Use prefix sum traversal to reconstruct the final array and find the maximum.

Time Complexity: O(n + q)
Space Complexity: O(n)

Solved: 2025-07-20
*/
#include <bits/stdc++.h>
using namespace std;
const int64_t N = 1e7 + 10;
vector<int64_t> ar(N);

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int32_t n, q;
    cin >> n >> q;

    while (q--)
    {
        int32_t a, b, k;
        cin >> a >> b >> k;
        ar[a] += k;
        if (b + 1 < N)
        {
            ar[b + 1] -= k;
        }
    }
    for (int i = 1; i <= n; i++)
    {
        ar[i] += ar[i - 1];
    }
    cout << *max_element(ar.begin() + 1, ar.begin() + n + 1);

    return 0;
}
