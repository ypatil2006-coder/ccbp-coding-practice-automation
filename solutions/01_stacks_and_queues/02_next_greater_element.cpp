#include<bits/stdc++.h>
using namespace std;

// Next Greater Element
// Time Complexity: O(N) using Monotonic Stack
// Space Complexity: O(N)
class solution {
public:
    vector<long long> nextLargerElement(vector<long long> arr, int n) {
        vector<long long> res(n, -1);
        stack<long long> st;
        for (int i = n - 1; i >= 0; --i) {
            while (!st.empty() && st.top() <= arr[i]) {
                st.pop();
            }
            if (!st.empty()) {
                res[i] = st.top();
            }
            st.push(arr[i]);
        }
        return res;
    }
};
