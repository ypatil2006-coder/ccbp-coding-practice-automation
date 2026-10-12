#include<bits/stdc++.h>
using namespace std;

// Two Sum II - Input Array Is Sorted (1-based indices)
// Time Complexity: O(N)
// Space Complexity: O(1)
class solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int left = 0;
        int right = numbers.size() - 1;
        while (left < right) {
            int current_sum = numbers[left] + numbers[right];
            if (current_sum == target) {
                return {left + 1, right + 1};
            } else if (current_sum < target) {
                left++;
            } else {
                right--;
            }
        }
        return {};
    }
};
