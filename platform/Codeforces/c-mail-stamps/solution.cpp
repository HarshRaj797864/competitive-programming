/*
Problem: C Mail Stamps
Platform: Codeforces
Problem ID: 29C
URL: https://codeforces.com/contest/29/problem/C

Time Complexity: O(n)  
Space Complexity: O(n)  
*/

#include <bits/stdc++.h>
using namespace std;
const int N = 1e5 + 10;
const int INF = 1e9 + 7;

unordered_map<int, vector<int>> adj;
unordered_map<int, int> cnt;
unordered_map<int, bool> vis;
vector<int> path;


void dfs(int v, int p = -1) {
    vis[v] = true;
    path.push_back(v);

    for(auto ch: adj[v]) {
        if (ch == p ) continue;
        if(!vis[ch]) dfs(ch, v);
    }
}
int main()
{
    // cout << "Execution begins........\n";
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n{};
    cin >> n;
    // int cnt_1{0};
    for (int i = 0; i < n; i++)
    {
        int v1, v2;
        cin >> v1 >> v2;
        adj[v1].push_back(v2);
        adj[v2].push_back(v1);
        cnt[v1]++;
        cnt[v2]++;
        // cnt_1 = cnt[v1] == 1? v1: cnt[v2] == 1? v2: 0;
    }

    int start = -1;
    for (auto &kv : cnt) {
        if (kv.second == 1) {
            start = kv.first;
            break;
        }
    }

    dfs(start);

    for (auto city: path) {
        cout << city << " ";
    }
    
    // cout << "\nExecution Terminates......\n";
    return 0;
}
