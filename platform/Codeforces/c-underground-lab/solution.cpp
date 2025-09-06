/*
Problem: C Underground Lab
Platform: Codeforces
Problem ID: C
URL: https://codeforces.com/problem/C

Time Complexity: O()
Space Complexity: O()
*/

#include <bits/stdc++.h>
using namespace std;


vector<vector<int>> adjlist;
vector<bool> vis;
vector<int> path;

void dfs(int v, int p = -1) {
    vis[v] = true;
    path.push_back(v);

    for(auto child: adjlist[v]) {
        if (child == p) continue;
        if (!vis[child]) dfs(child, v);
        // path.push_back(v);
    }
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, k;
    cin >> n >> m >> k;

    adjlist.resize(n + 1);
    vis.resize(n + 1, false);
    for (int i = 0; i < m; i++)
    {
        int v1, v2;
        cin >> v1 >> v2;
        adjlist[v1].push_back(v2);
        if (v1 != v2) adjlist[v2].push_back(v1);



    }
    
    // here we will store euler route of the spanning tree so that every node is visited in smallest possible path 
    dfs(1, -1);

    // the constraint of 2*n/k suggests that we have to use euler route to get the desired path
    int path_size = path.size();
    int base_size = path_size / k;
    int remainder = path_size % k;

    int idx{0};
    
    for (int i = 0; i < k; i++)
    {
        int cur_size = base_size;
        if (i < remainder) {
            cur_size++;
        }
        cur_size = min(cur_size, path_size - idx);

        if (cur_size > 0)
        {
            cout << cur_size << " ";
            for (int j = idx; j < idx + cur_size; j++)
            {
                cout << path[j] << " ";
            }
            cout << endl;
            idx += cur_size;
            
        }
        else
        {
            cout << "1 1\n";
        }
        
        
    }
    


    
    return 0;
}
