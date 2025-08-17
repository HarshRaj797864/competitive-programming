/*
Problem: D Shichikuji And Power Grid
Platform: Codeforces
Problem ID: D
URL: https://codeforces.com/contest/1245/problem/D

Time Complexity: O(n^2 log(n))
Space Complexity: O(n^2)
*/

#include <bits/stdc++.h>
using namespace std;
const int N = 2e3 + 10;

vector<int> parent(N);
vector<int> Size(N);

void make(int v) {
    parent[v] = v;
    Size[v] = 1;
}
int find(int v) {
    if(parent[v] == v) return v;
    return (parent[v] = find(parent[v]));
}
void Union(int a, int b) {
    a = find(a);
    b = find(b);
    if (a != b) {
        if (Size[a] < Size[b]) {
            swap(a, b);
        }
        parent[b] = a;
        Size[a] += Size[b];
    }

}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n{};
    cin >> n;
    vector<pair<int, int>> cities(n + 1);
    for (int i = 1; i <= n; i++)
    {
        cin >> cities[i].first >> cities[i].second;
    }
    for (int i = 0; i <= n; i++) {
        make(i);
    }
    vector<int> c(n+1), k(n+1);
    for (int i = 1; i <= n; i++)
    {
        cin >> c[i];
    }
    for (int i = 1; i <= n; i++)
    {
        cin >> k[i];
    }
    vector<pair<int64_t, pair<int, int>>> edges;
    for (int i = 1; i <= n; i++)
    {
        edges.push_back({c[i], {0, i}});
    }
    for (int i = 1; i <= n; i++)
    {
        for (int j = i + 1; j <= n; j++)
        {
            int64_t dist = abs(cities[i].first - cities[j].first) + abs(cities[i].second - cities[j].second); 
            int64_t cost = dist * (k[i] + k[j]);
            edges.push_back({cost, {i, j}});
        }
    }
    sort(edges.begin(), edges.end());
    int64_t yen{0};
    vector<int> pow_stations;
    vector<pair<int, int>> connections;
    for(auto &edge: edges) {
        int wt = edge.first;
        int v1 = edge.second.first;
        int v2 = edge.second.second;
        if(find(v1) == find(v2)) continue;
        if(v1 == 0 || v2 == 0) {
            pow_stations.push_back(max(v1, v2));
        }
        else
        {
            connections.push_back({v1, v2});
        }
        
        Union(v1, v2);
        

        yen += wt;
    }
    cout << yen  << endl;
    cout << pow_stations.size() << endl;
    for(auto st: pow_stations) {
        cout << st << " ";
    }
    cout << endl;
    cout << connections.size() << endl;
    for(auto &pairs: connections) {
        cout << pairs.first << " " << pairs.second << endl;
    }
    return 0;
}
