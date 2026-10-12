#include<bits/stdc++.h>
using namespace std;

// Nearest Smaller Element
// Time Complexity: O(N)
// Space Complexity: O(N)
class solution {
public:
    vector<int> prevSmaller(vector<int>& A) {
        int n = A.size();
        vector<int> G(n, -1);
        stack<int> st;
        for (int i = 0; i < n; ++i) {
            while (!st.empty() && st.top() >= A[i]) {
                st.pop();
            }
            if (!st.empty()) {
                G[i] = st.top();
            }
            st.push(A[i]);
        }
        return G;
    }
};
