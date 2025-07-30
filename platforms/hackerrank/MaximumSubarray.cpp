#include <bits/stdc++.h>
using namespace std;
int maximumSumSubarray(vector<int>& arr, int k) {
        // code here
        // sort(arr.begin(), arr.end());
        // int sum {0};
        // auto it = arr.end() - 1; 
        // while (k--)
        // {
        //     sum += (*it);
        //     it--;  
        // }
        // return sum;
        // Time complexity:- O(nlog(n))
        // No need to store all of them
        // set<int> sums;
        uint64_t n{arr.size()};
        if (k > n) return -1;
        int maxSum {0};
        int windowSum {0};
        for(int i = 0; i < k;i++) {
            windowSum += arr[i];
        }
        maxSum = windowSum;
        
        for(int i = k; i < n; i++) {
            windowSum += arr[i] - arr[i - k];
            maxSum = max(maxSum, windowSum);
        }
        return maxSum;
        // Time Complexity:- O(k) + O(n - k) = O(n)
        // Space Complexity:- O(1)
    }

int main()
{
    vector<int> arr = {100, 200, 300, 400, 500};
    int max {maximumSumSubarray(arr, 4)};
    cout << max << endl;
    return 0;
}
