#include <bits/stdc++.h>
#include <unordered_set>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

// Definition for a Node.
class Node {
public:
    int val;
    Node* next;
    Node* random;

    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};

class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (!head)
            return nullptr;

        vector<Node*> old_node_ptrs {};
        map<Node*, int> old_ptr_to_idx {};
        int i = 0;
        for (Node* node_ptr = head; node_ptr; node_ptr = node_ptr->next) {
            old_node_ptrs.push_back(node_ptr);
            old_ptr_to_idx[node_ptr] = i;
            i++;
        }

        int n = old_node_ptrs.size();
        vector<Node*> new_node_ptrs (n);

        for (int i = 0; i < n; i++) {
            new_node_ptrs[i] = new Node(old_node_ptrs[i]->val);
        }

        for (int i = 0; i < n - 1; i++) {
            new_node_ptrs[i]->next = new_node_ptrs[i + 1];
        }
        new_node_ptrs[n - 1]->next = nullptr;

        for (int i = 0; i < n; i++) {
            auto old_rand_ptr = old_node_ptrs[i]->random;
            new_node_ptrs[i]->random = (old_rand_ptr != nullptr) ? new_node_ptrs[old_ptr_to_idx[old_rand_ptr]] : nullptr;
        }

        return new_node_ptrs[0];
    }
};
