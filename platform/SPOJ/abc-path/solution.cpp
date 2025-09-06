/*
Problem: Abc Path
Platform: SPOJ
Problem ID: ABCPATH
URL: https://www.spoj.com/problems/ABCPATH/

Time Complexity: O(H * W * 8) = O(H * W)
Space Complexity: O(H * W) for visited matrix and recursion stack
*/

#include <bits/stdc++.h>
using namespace std;
const int N = 55;
vector<vector<char>> mat(N, vector<char>(N, '0'));
vector<vector<bool>> vis(N, vector<bool>(N));
int max_ct{0};
void reset(int h, int w)
{
    max_ct = 0;
    for (int i = 1; i <= h; i++)
    {
        for (int j = 1; j <= w; j++)
        {

            vis[i][j] = false;
        }
    }
}

const vector<pair<int, int>> movements = {
    {-1, 1}, {0, 1}, {1, 1}, {-1, 0}, {1, 0}, {-1, -1}, {0, -1}, {1, -1}};

void dfs(int i, int j, int h, int w, int count)
{
    if (i <= 0 || j <= 0)
        return;
    if (i > h || j > w)
        return;
    if (mat[i][j] == '0' || vis[i][j])
        return;
    max_ct = max(max_ct, count);
    vis[i][j] = true;
    char next_ch = mat[i][j] + 1;
    for (auto mov : movements)
    {
        int ni = i + mov.first;
        int nj = j + mov.second;
        if (ni >= 1 && ni <= h && nj >= 1 && nj <= w)
        {

            if (mat[ni][nj] == next_ch && !vis[ni][nj])
            {
                dfs(ni, nj, h, w, count + 1);
            }
        }
    }
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int test_case = 1;
    while (true)
    {
        int h, w;
        cin >> h >> w;
        if (h == 0 || w == 0)
            break;
        reset(h, w);
        for (int i = 1; i <= h; i++)
        {
            for (int j = 1; j <= w; j++)
            {
                cin >> mat[i][j];
            }
        }

        for (int i = 1; i <= h; i++)
        {
            for (int j = 1; j <= w; j++)
            {
                if (mat[i][j] == 'A' && !vis[i][j])
                    dfs(i, j, h, w, 1);
            }
        }
        cout << "Case " << test_case++ << ": " << max_ct << endl;
    }

    return 0;
}
