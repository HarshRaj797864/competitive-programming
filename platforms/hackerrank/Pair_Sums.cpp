/*
{platform} #{problem_id}: {problem_name}
Tags: {tags}
Difficulty: {difficulty}
URL: {problem_url}

Approach:
1. {approach_point_1}
2. {approach_point_2}

Time Complexity: O({time_complexity})
Space Complexity: O({space_complexity})

Solved: {current_date}
*/


#include <bits/stdc++.h>
using namespace std;

int main()
{
    uint32_t size;
    int32_t k;
    cin >> size >> k;

    unordered_set<int32_t> s;

    for(uint32_t i = 0; i < size; i++) {
        int32_t l;
        cin >> l;
        
        int32_t complement = k - l;
        if(s.find(complement) != s.end()) {
            cout << "YES";
            return 0;
        }
        s.insert(l); // insert after checking
    }

    cout << "NO";
    return 0;
}
