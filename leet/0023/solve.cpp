#include <algorithm>
#include <bits/stdc++.h>

#include <cassert>
#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        ListNode dummy_head {};
        ListNode* tail = &dummy_head;

        if (lists.empty()) return nullptr;

        while (true) {
            auto chosen_ptr = min_element(
                lists.begin(),
                lists.end(),
                [&lists](const ListNode* a, const ListNode* b) {
                if (a == nullptr)
                    return false;
                if (b == nullptr)
                    return true;
                return a->val < b->val;
            });

            if (*chosen_ptr == nullptr) {
                break;
            }

            // Take what is pointed by `tail` at the moment.
            // And set the `next` of it to the winner.
            tail->next = *chosen_ptr;
            // Update the tail to point to the last added node.
            tail = *chosen_ptr;
            // Go to the next node in the linked list.
            *chosen_ptr = (*chosen_ptr)->next;

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
    auto data = GENERATE(table<vector<int>, vector<vector<int>>>({
            // Test cases inherited from LC 21
            {{1,1,2,3,4,4}, {{1,2,4}, {1,3,4}}},
            {{}, {{}, {}}},
            {{0}, {{}, {0}}},
            {{0,1}, {{}, {0,1}}},
            {{0,1}, {{0,1}, {}}},
            {{0,1}, {{0}, {1}}},
            // k > 2
            {{1,2,3}, {{},{1,2,3},{}}},
            {{1,1,2,3,4,4}, {{1,2}, {1,3,4}, {4}}},
            {{1,2,3}, {{1}, {2}, {3}}},
            {{}, {{}, {}, {}}},
            {{}, {}},
    }));

    ListNode* expected = vector_to_list(get<0>(data));
    cout << endl;
    cout << "New Test Case!\n";
    int k = get<1>(data).size();
    vector<ListNode*> lists(k);
    for (int i = 0; i < k; i++) {
        lists[i] = vector_to_list(get<1>(data).at(i));
    }
    cout << "Expected:\n";
    print_listnode(expected);
    cout << "Data prepped\n\n";

    Solution *solution = new Solution();
    REQUIRE(equivalent_listnode_ptrs(expected, solution->mergeKLists(lists)));
}

// Naive solution, but it's mine ;p
// Could use a PQ for a boost in speed.
