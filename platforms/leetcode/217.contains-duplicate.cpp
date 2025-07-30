/*
 #ID: Problem Name
Tags: Arrays
Difficulty: Easy
URL: https://...

Approach:
1. Key step
2. Next step

Time Complexity: O()
Space Complexity: O()

Solved: 2025-07-17
"""
*/
#include <bits/stdc++.h>
using namespace std;

bool containsDuplicate(vector<int>& nums) {
    unordered_set<int> seen;
    for (int val : nums) {
        if (seen.count(val)) return true;
        seen.insert(val);
    }
    return false;
}

int main() {

    vector<int> num = {1, 2, 3 , 4,};
    bool result {containsDuplicate(num)};
    cout << boolalpha;
    cout << result << endl;
    return 0;

}
