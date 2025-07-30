/*
CodeChef #11376: Little Jhool and the Magical Jewels
Tags: Strings, Frequency Count, Hash Maps
Difficulty: Easy
URL: https://www.hackerearth.com/practice/data-structures/hash-tables/basics-of-hash-tables/practice-problems/algorithm/little-jhool-and-the-magical-jewels/

Approach:
1. Count the frequency of characters in the given string using an unordered_map.
2. The number of complete "ruby" strings that can be formed is the minimum count among characters {'r', 'u', 'b', 'y'}.
3. For each test case, output this minimum count.

Time Complexity: O(N) per test case, where N is the length of the string.
Space Complexity: O(1), as we only store frequency of lowercase letters.

Solved: 2025-07-17
*/

#include <bits/stdc++.h>
using namespace std;

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int T{};
    cin >> T;
    while (T--)
    {
        string s{};
        cin >> s;
        unordered_map<char, int> hash;
        for(auto ch: s) {
            hash[ch]++;
        }
        int ct{0};

        while (hash['r'] != 0 && hash['u'] != 0 && hash['b'] != 0 && hash['y'] != 0)
        {
            ct++;
            string S = "ruby";
            for(auto ch: S) {
                hash[ch]--;
            }
        }
        cout << ct << endl;
        
    }
    
    return 0;
}
