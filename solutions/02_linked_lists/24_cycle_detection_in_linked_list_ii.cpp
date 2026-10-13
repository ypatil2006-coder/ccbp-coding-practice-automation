#include <bits/stdc++.h>
using namespace std;

/*
class Node {
    public:
        int data;
        Node* next;
        
        Node(): data(0), next(nullptr) {}
        Node(int data) : data(data), next(nullptr) {}
        Node(int data, Node* next) : data(data), next(next) {}
};
*/

class solution {
public:
    Node *detectCycle(Node *head) {
        if (!head || !head->next) return nullptr;
        
        Node* slow = head;
        Node* fast = head;
        
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) {
                // Cycle detected, find the start node
                Node* entry = head;
                while (entry != slow) {
                    entry = entry->next;
                    slow = slow->next;
                }
                return entry;
            }
        }
        
        return nullptr;
    }
};
