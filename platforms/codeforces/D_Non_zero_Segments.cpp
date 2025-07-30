/*
{platform} #{problem_id}: {problem_name}
Tags: {tagsCommaSeparated}
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
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N{};
    cin >> N;
    vector<int> ar(N);
    vector<int> sum(N);
    for (int i = 0; i < N; i++)
    {
        int n {};
        cin >> n;
        ar[i] = n;
        sum[i] = (i == 0 ? n : sum[i - 1] + n);
    }
    vector<int> sum2 = sum;
    
    int ct {0};
    int left{0};
    
    for (int left = 0; left < N; left++)
    {
        // ok we will be working on the window which constantly shrinks
        
        sort(sum2.begin() + left, sum2.end());
        int lo {left};
        int hi {N-1};
        int mid {};
        while (hi - lo > 1)
        {
            mid = lo + (hi - lo)/2;
            if (sum2[mid] < sum[left])
            {
                lo = mid + 1;
            }
            else
            {
                hi = mid;
            }
            
        }
        if (sum2[lo] == sum[left])
        {
            ct++;
        }
        else if (sum2[hi] == sum[left] )
        {
            ct++;
        }
        


    }
    cout << ct;
    
    
    return 0;
}
