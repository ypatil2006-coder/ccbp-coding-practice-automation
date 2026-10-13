#include <bits/stdc++.h>
using namespace std;

class solution {
  public:
    bool isValidParentheses(string parenStr, string isLocked) {
        int n = parenStr.length();
        if (n % 2 != 0) return false;
        
        int open = 0, flex = 0;
        for (int i = 0; i < n; ++i) {
            if (isLocked[i] == '0') {
                flex++;
            } else if (parenStr[i] == '(') {
                open++;
            } else {
                if (open > 0) {
                    open--;
                } else if (flex > 0) {
                    flex--;
                } else {
                    return false;
                }
            }
        }
        
        int close = 0;
        flex = 0;
        for (int i = n - 1; i >= 0; --i) {
            if (isLocked[i] == '0') {
                flex++;
            } else if (parenStr[i] == ')') {
                close++;
            } else {
                if (close > 0) {
                    close--;
                } else if (flex > 0) {
                    flex--;
                } else {
                    return false;
                }
            }
        }
        
        return true;
    }  
};
