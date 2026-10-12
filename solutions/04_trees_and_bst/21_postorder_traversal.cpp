#include<bits/stdc++.h>
using namespace std;

// Postorder Traversal (Left -> Right -> Root)
// Time Complexity: O(N)
// Space Complexity: O(H) recursion stack
class solution {
public:
    void postorder(Node* root) {
        if (root == nullptr) {
            return;
        }
        postorder(root->left);
        postorder(root->right);
        cout << root->data << " ";
    }
};
