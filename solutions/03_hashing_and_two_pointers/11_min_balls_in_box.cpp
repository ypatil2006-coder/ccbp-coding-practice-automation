#include<bits/stdc++.h>
using namespace std;

// Minimum Number of Balls in the Box
// Time Complexity: O(N)
// Space Complexity: O(N)
class solution {
public:
    int minBalls(vector<int>& arr) {
        unordered_map<int, int> freq;
        for (int x : arr) freq[x]++;
        int ans = 0;
        for (auto& p : freq) {
            ans += (p.second % 2);
        }
        return ans;
    }
};
