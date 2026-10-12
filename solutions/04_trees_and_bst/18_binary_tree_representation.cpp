#include <bits/stdc++.h>
using namespace std;

// Binary Tree Representation
// Time Complexity: O(N)
// Space Complexity: O(N)
/*
class Node {
public:
    int data;
    Node* left;
    Node* right;

    Node(int data) {
        this->data = data;
        this->left = this->right = nullptr;
    }
};
*/
class solution {
public:
    Node* buildTree(int n, int arr[]) {
        if (n <= 0) return nullptr;
        vector<Node*> nodes(n);
        for (int i = 0; i < n; ++i) {
            nodes[i] = new Node(arr[i]);
        }
        for (int i = 0; i < n; ++i) {
            if (2 * i + 1 < n) nodes[i]->left = nodes[2 * i + 1];
            if (2 * i + 2 < n) nodes[i]->right = nodes[2 * i + 2];
        }
        return nodes[0];
    }
};
