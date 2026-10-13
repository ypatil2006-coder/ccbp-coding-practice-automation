#include <bits/stdc++.h>
using namespace std;

class solution {
    public:
    string removeInvalidParentheses(string str) {
        int n = str.length();
        vector<bool> to_remove(n, false);
        stack<int> st;
        
        for (int i = 0; i < n; ++i) {
            if (str[i] == '(') {
                st.push(i);
            } else if (str[i] == ')') {
                if (!st.empty()) {
                    st.pop();
                } else {
                    to_remove[i] = true;
                }
            }
        }
        
        while (!st.empty()) {
            to_remove[st.top()] = true;
            st.pop();
        }
        
        string res = "";
        for (int i = 0; i < n; ++i) {
            if (!to_remove[i]) {
                res += str[i];
            }
        }
        
        return res;
    }
};
