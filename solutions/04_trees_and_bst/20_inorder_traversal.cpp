#include<bits/stdc++.h>
using namespace std;

// Inorder Traversal (Left -> Root -> Right)
// Time Complexity: O(N)
// Space Complexity: O(H) recursion stack
class solution {
public:
    void inorder(Node* root) {
        if (root == nullptr) {
            return;
        }
        inorder(root->left);
        cout << root->data << " ";
        inorder(root->right);
    }
};
