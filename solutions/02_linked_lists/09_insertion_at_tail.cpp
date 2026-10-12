#include<bits/stdc++.h>
using namespace std;

// Insertion at Tail - Linked List
// Time Complexity: O(N)
// Space Complexity: O(1)
class solution {
public:
    Node* insertAtTail(Node* head, int val) {
        Node* newNode = new Node(val);
        if (head == nullptr) {
            return newNode;
        }
        Node* curr = head;
        while (curr->next != nullptr) {
            curr = curr->next;
        }
        curr->next = newNode;
        return head;
    }
};
