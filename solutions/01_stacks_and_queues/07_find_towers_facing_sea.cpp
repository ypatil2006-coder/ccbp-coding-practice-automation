#include<bits/stdc++.h>
using namespace std;

// Find Towers Facing Sea (Right-to-Left Running Maximum)
// Time Complexity: O(N)
// Space Complexity: O(1) Auxiliary
class solution {
public:
    int countTowers(vector<int>& arr) {
        int n = arr.size();
        if (n == 0) return 0;
        int count = 0;
        int max_h = 0;
        for (int i = n - 1; i >= 0; --i) {
            if (arr[i] > max_h) {
                count++;
                max_h = arr[i];
            }
        }
        return count;
    }
};
