/*
CodeChef #XYZ123: Make Strings Anagram
Tags: Strings, Hashing, Frequency Count, Anagrams
Difficulty: Easy
URL: https://www.codechef.com/problems/MAKEPAL (replace with actual)

Approach:
1. Count the frequency of each character in both strings S and T using hash maps.
2. For each character, compute the difference in frequencies and sum the absolute differences.
   - This corresponds to additions (if S needs more of a character) or deletions (if T has extras).

Time Complexity: O(N + M), where N = length of S, M = length of T
Space Complexity: O(1) (constant space for 26 lowercase letters)

Solved: 2025-07-17
*/


#include <bits/stdc++.h>
using namespace std;

int main()
{
    
    ios_base::sync_with_stdio(false);
	cin.tie(nullptr);
    // Inputs
    uint32_t Q{};
    cin >> Q;
    while (Q--)
    {
        string S{}, T{};
        cin >> S;
        cin >> T;
        // pre-compute the hash maps for both s and t
        unordered_map<char, uint64_t> Hash_s;
        unordered_map<char, uint64_t> Hash_t;
        // O(length(S))
        for(auto ch: S) {
            Hash_s[ch]++;
        }
        for(auto ch: T) {
            Hash_t[ch]++;
        }
        uint64_t op{0};
        // comparing s and t
        // To iterate over a pair do the following:-
        for(auto & [ch, count_s]: Hash_s) {
            uint64_t count_t = Hash_t[ch];
            if (count_s > count_t)
            {
                op += count_s - count_t;
            }
            else if(count_t > count_s) {
                op += count_t - count_s;
            }
            Hash_t.erase(ch);
        }
        for(auto &[ch, count_t]: Hash_t) {
            op += count_t;
        }
        cout << op << endl;


    }
    return 0;
}
