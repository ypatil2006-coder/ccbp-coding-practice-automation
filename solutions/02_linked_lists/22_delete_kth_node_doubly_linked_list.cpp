#include<bits/stdc++.h>
using namespace std;

/*
class Node {
    public:
        int data;
        Node* next;
        Node* prev;
        Node(int value, Node* next_Address, Node* prev_Address){
            data = value; 
            next = next_Address; 
            prev = prev_Address;
        }
        Node(int value){
           data = value;
           next = nullptr;
           prev = nullptr;
        }
};
*/

class solution {
public:
    Node* deleteKthNode(Node* head, int k) {
        if (!head || k < 0) return head;
        if (k == 0) {
            Node* nextNode = head->next;
            if (nextNode) {
                nextNode->prev = nullptr;
            }
            delete head;
            return nextNode;
        }
        
        Node* curr = head;
        for (int i = 0; i < k && curr; ++i) {
            curr = curr->next;
        }
        
        if (!curr) return head;
        
        Node* prevNode = curr->prev;
        Node* nextNode = curr->next;
        
        if (prevNode) prevNode->next = nextNode;
        if (nextNode) nextNode->prev = prevNode;
        
        delete curr;
        return head;
    }
};
