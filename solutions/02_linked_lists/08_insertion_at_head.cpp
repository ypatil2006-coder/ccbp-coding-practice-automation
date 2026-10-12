#include<bits/stdc++.h>
using namespace std;

// Insertion at Head - Linked List
// Time Complexity: O(1)
// Space Complexity: O(1)
/*
class Node {
public:
    int data;
    Node* next;
    Node(int val) {
        data = val;
        next = nullptr;
    }
};
*/
class solution {
public:
    Node* insertAtHead(Node* head, int val) {
        Node* newNode = new Node(val);
        newNode->next = head;
        return newNode;
    }
};
