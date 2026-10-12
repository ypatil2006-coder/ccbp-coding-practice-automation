#include<bits/stdc++.h>
using namespace std;

// Four Sum
// Time Complexity: O(N^3)
// Space Complexity: O(1) auxiliary
class solution {
public:
    vector<vector<int>> fourSum(vector<int>& arr, int target) {
        vector<vector<int>> ans;
        int n = arr.size();
        if (n < 4) return ans;
        
        sort(arr.begin(), arr.end());
        
        for (int i = 0; i < n - 3; ++i) {
            if (i > 0 && arr[i] == arr[i - 1]) continue;
            for (int j = i + 1; j < n - 2; ++j) {
                if (j > i + 1 && arr[j] == arr[j - 1]) continue;
                
                int left = j + 1;
                int right = n - 1;
                
                while (left < right) {
                    long long sum = (long long)arr[i] + arr[j] + arr[left] + arr[right];
                    if (sum == target) {
                        ans.push_back({arr[i], arr[j], arr[left], arr[right]});
                        while (left < right && arr[left] == arr[left + 1]) left++;
                        while (left < right && arr[right] == arr[right - 1]) right--;
                        left++;
                        right--;
                    } else if (sum < target) {
                        left++;
                    } else {
                        right--;
                    }
                }
            }
        }
        return ans;
    }
};
