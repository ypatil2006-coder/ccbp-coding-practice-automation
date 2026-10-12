#include<bits/stdc++.h>
using namespace std;

// Count Subarrays with Target Sum
// Time Complexity: O(N)
// Space Complexity: O(N)
class solution {
public:
    int countSubarrays(vector<int>& arr, int target) {
        unordered_map<long long, int> freq;
        freq[0] = 1;
        long long current_sum = 0;
        int count = 0;
        for (int x : arr) {
            current_sum += x;
            if (freq.find(current_sum - target) != freq.end()) {
                count += freq[current_sum - target];
            }
            freq[current_sum]++;
        }
        return count;
    }
};
