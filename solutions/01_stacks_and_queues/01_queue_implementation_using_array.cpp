#include<bits/stdc++.h>
using namespace std;

// Queue Implementation using Array
// Time Complexity: O(1) for all operations
// Space Complexity: O(K)
class MyQueue {
private:
    vector<int> arr;
    int front;
    int rear;
    int count;
    int capacity;

public:
    MyQueue(int k) {
        capacity = k;
        arr.resize(k);
        front = 0;
        rear = -1;
        count = 0;
    }

    int push(int x) {
        if (count == capacity) {
            return -1;
        }
        rear = (rear + 1) % capacity;
        arr[rear] = x;
        count++;
        return x;
    }

    int pop() {
        if (count == 0) {
            return -1;
        }
        int val = arr[front];
        front = (front + 1) % capacity;
        count--;
        return val;
    } 

    int frontElement() {
        if (count == 0) {
            return -1;
        }
        return arr[front];
    }

    int queueSize() {
        return count;
    }

    bool empty() {
        return count == 0;
    }
};
