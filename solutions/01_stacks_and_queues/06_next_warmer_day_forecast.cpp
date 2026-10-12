#include<bits/stdc++.h>
using namespace std;

// Next Warmer Day Forecast (Daily Temperatures)
// Time Complexity: O(N)
// Space Complexity: O(N)
class solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> ans(n, 0);
        stack<int> st; // stores indices
        for (int i = n - 1; i >= 0; --i) {
            while (!st.empty() && temperatures[st.top()] <= temperatures[i]) {
                st.pop();
            }
            if (!st.empty()) {
                ans[i] = st.top() - i;
            }
            st.push(i);
        }
        return ans;
    }
};
