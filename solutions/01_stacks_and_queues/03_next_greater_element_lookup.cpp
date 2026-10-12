#include<bits/stdc++.h>
using namespace std;

// Next Greater Element Lookup for Subsets
// Time Complexity: O(N + M)
// Space Complexity: O(N)
class solution {
public:
    vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
        unordered_map<int, int> nge;
        stack<int> st;
        for (int i = (int)nums2.size() - 1; i >= 0; --i) {
            while (!st.empty() && st.top() <= nums2[i]) {
                st.pop();
            }
            nge[nums2[i]] = st.empty() ? -1 : st.top();
            st.push(nums2[i]);
        }
        vector<int> ans;
        ans.reserve(nums1.size());
        for (int x : nums1) {
            ans.push_back(nge[x]);
        }
        return ans;
    }
};
