#include<bits/stdc++.h>
using namespace std;

// Insertion Before a Node with Value X - Linked List
// Time Complexity: O(N)
// Space Complexity: O(1)
class solution {
public:
    Node* insertBeforeX(Node* head, int val, int x) {
        Node* newNode = new Node(val);
        if (head == nullptr) {
            return head;
        }
        if (head->data == x) {
            newNode->next = head;
            return newNode;
        }
        Node* curr = head;
        while (curr->next != nullptr && curr->next->data != x) {
            curr = curr->next;
        }
        if (curr->next != nullptr) {
            newNode->next = curr->next;
            curr->next = newNode;
        }
        return head;
    }
};
