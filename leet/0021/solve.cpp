#include <bits/stdc++.h>

#include <cassert>
#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        ListNode dummy_head {};
        ListNode* tail = &dummy_head;

        while (list1 or list2) {
            int choice = 0; // 1 or 2
            if (not list1) {
                choice = 2;
            } else if (not list2) {
                choice = 1;
            } else if (list2->val > list1->val) {
                choice = 1;
            } else {
                choice = 2;
            }
            // assert(choice);

            if (choice == 1) {
                // Take what is pointed by `tail` at the moment.
                // And set the `next` of it to the winner.
                tail->next = list1;
                // Update the tail to point to the last added node.
                tail = list1;
                // Go to the next node in the linked list.
                list1 = list1->next;
            } else {
                tail->next = list2;
                tail = list2;
                list2 = list2->next;
            }
        }

        return dummy_head.next;
    }
};

ListNode* vector_to_list(vector<int> vec) {
    ListNode* head = nullptr;
    ListNode* tail = nullptr;
    for (int i = 0; i < vec.size(); i++) {
        ListNode* new_node_ptr = new ListNode(vec[i]);
        if (i == 0) {
            head = new_node_ptr;
            tail = new_node_ptr;
        } else {
            tail->next = new_node_ptr;
        }
        tail = new_node_ptr;
    }
    // cout << head->val << endl;
    return head;
}

bool equivalent_listnode_ptrs(ListNode* a, ListNode* b) {
    if (a == b) {
        return true;
    }
    if (not a or not b) {
        assert(not (not a and not b));
        return false;
    }
    if (a->val != b->val) {
        return false;
    }
    return equivalent_listnode_ptrs(a->next, b->next);
}

void print_listnode(ListNode* a) {
    cout << "[";
    for (; a != nullptr; a = a->next) {
        cout << a->val << ", ";
    }
    cout << "]\n";
}


TEST_CASE("Examples") {
    auto data = GENERATE(table<vector<int>, vector<int>, vector<int>>({
            {{1,1,2,3,4,4}, {1,2,4}, {1,3,4}},
            {{}, {}, {}},
            {{0}, {}, {0}},
            {{0,1}, {}, {0,1}},
            {{0,1}, {0,1}, {}},
            {{0,1}, {0}, {1}},
    }));

    ListNode* expected = vector_to_list(get<0>(data));
    cout << "\nNew Test Case!\n";
    // cout << "HELLO" << endl;;
    ListNode* list1 = vector_to_list(get<1>(data));
    ListNode* list2 = vector_to_list(get<2>(data));
    print_listnode(expected);
    cout << "Data prepped\n\n";

    Solution *solution = new Solution();
    // REQUIRE(expected == solution->mergeTwoLists(list1, list2));
    REQUIRE(equivalent_listnode_ptrs(expected, solution->mergeTwoLists(list1, list2)));
}
