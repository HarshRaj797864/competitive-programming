/*
CodeChef #15802: A Needle in the Haystack
Tags: Ad-Hoc, Hash Maps, Sliding Window, Frequency Count, String Matching
Difficulty: Medium
URL: https://www.hackerearth.com/practice/data-structures/hash-tables/basics-of-hash-tables/practice-problems/algorithm/a-needle-in-the-haystack-1/

Approach:
1. Count the frequency of each character in the pattern.
2. Use a sliding window of size equal to the pattern's length and scan the text string.
   - Track character frequencies in the current window.
   - Maintain a matched count to ensure characters are matching the pattern.
   - Shrink the window when it exceeds the pattern size, and update matched accordingly.

Time Complexity: O(n)
Space Complexity: O(1) — as character set is fixed to 26 lowercase letters

Solved: 2025-07-20
*/
#include <bits/stdc++.h>
using namespace std;

bool checkPermutation(const string &p,const string &s) {
    // I need to generate the window of size pat and scan it throughout 

    int pat_size = p.size();
    int str_size = s.size();
    if (pat_size>str_size) return false;
    unordered_map<char, int> winFrequency, patFreq;
    for (char ch : p) patFreq[ch]++;
    int left {0};
    int matched {0};
    for (int right = 0; right < str_size; right++)
    {
        char ch = s[right];
        if (patFreq[ch] != 0)
        {
            winFrequency[ch]++;
            if( winFrequency[ch] <= patFreq[ch]) matched++;
        }

        // Adjust windowsize while also fixing winFrequency count
        // This checks whether current window size is more than pat length
        // If it is then we move left forward while also decrementing the count of that left char 
        if (right - left + 1 > pat_size) {
            auto leftChar = s[left];
            // Now if this leftChar is present in p then we have to decrease it's count
            // we have to avoid decrementing those leftChar which were not incremented in the first place
            if (patFreq[leftChar] != 0)
            {
                // if we have counted this char to increment matched then we have to decrease matched
                if (winFrequency[leftChar] <= patFreq[leftChar]) matched--;
                winFrequency[leftChar]--;
            }
            left++;

        }
        if (matched == pat_size)
        {
            return true;
        }
        
        
    }
    return false;
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int T{0};
    cin >> T;
    while (T--)
    {
        
        string pat{};
        string str{};
        cin >> pat >> str;
        
        
        if (checkPermutation(pat, str))
        {
            cout << "YES" << endl;
        }
        else
        {
            cout << "NO" << endl;
        }
        
    }
    
    return 0;
}
