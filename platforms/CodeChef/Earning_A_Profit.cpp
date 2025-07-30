/*
CodeChef ICL1905: Earning A Profit
Tags: prefix sum, brute force, subarrays
Difficulty: Medium
URL: https://www.codechef.com/problems/ICL1905

Approach:
1. Build a prefix sum array over fuel costs to compute total cost for any subsegment [L,R] in O(1).
2. For each subsegment [L,R] (nested loops), maintain and update minimum and maximum difficulty to compute gap penalty = (max_d - min_d)².
3. Calculate profit = (length * A) – (fuel_total) – gap_penalty, and keep track of the maximum profit.

Time Complexity: O(T * N²)
Space Complexity: O(N)

Solved: 2025-07-17
*/


#include <bits/stdc++.h>
using namespace std;





void getMaxProfit(const uint64_t N, const uint64_t A, const vector<uint64_t> &diff,const vector<uint64_t> &prefix, uint64_t &maxProfit) {
    
    // getting a variable sliding window to solve this
    
    
    for (uint64_t i = 1; i <= N; i++)
    {
        
        uint64_t min_d = diff[i], max_d = diff[i];   
        for(uint64_t j = i; j <= N; j++) {
            min_d = min(min_d, diff[j]);
            max_d = max(max_d, diff[j]);
            uint64_t profit = (j - i + 1)*A - (prefix[j] - prefix[i-1]);
            uint64_t gap = static_cast<uint64_t>((max_d - min_d))*(max_d - min_d);
            profit -= gap;
            maxProfit = max(maxProfit, profit);
        }
    }
    
}

int main()
{
    // T test cases
    // N planets, A coins per visitation
    // N lines containing Ci(fuel coins) and Di(difficulty) respectively
    // Ok my understanding:- 
    // I have N planets , I have to earn max profit by choosing a consecutive sub segment of planets
    // Eg:- 1 to 3:- 1->2, 1->2->3, 2->3
    // Now for each segment:- lets say going from l to r, then Profit:- (A - Ci) of l + (A - Ci) of l+1 + .... + (A) of R - gap(l, r) coins
    uint32_t T {};
    cin >> T;
    while (T--)
    {
        uint64_t N, A;
        cin >> N >> A;
        vector<uint64_t> fuelCost(N+1);
        vector<uint64_t> difficulty(N+1);
        // Pre-computation
        vector<uint64_t> prefix(N+1);
        fuelCost[0] = 0;
        difficulty[0] = 0;
        prefix[0] = 0;
        for (uint64_t i = 1; i <= N; i++)
        {
            cin >> fuelCost[i] >> difficulty[i];
            //Pre-computing sum of consecutive elements
            prefix[i] = prefix[i-1] + fuelCost[i];
        }
        // max profit is zero in case there is no visitation to other planets
        uint64_t maxProfit {0};
        // Now calculate profit for each case , and compare it to max  
        getMaxProfit(N, A, difficulty, prefix, maxProfit);
        // compare it to max profit
        cout << maxProfit << endl; 
        
    }
    return 0;
}
