#include <bits/stdc++.h>

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

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        int size = findSize(head);
        return removeNthFromStartZeroBased(head, size - n, n);
    }

    int findSize(ListNode* head) {
        int size = 0;
        for (ListNode* node_ptr = head; node_ptr != nullptr; node_ptr = node_ptr->next) {
            size++;
        }
        return size;
    }

    ListNode* removeNthFromStartZeroBased(ListNode* head, int n, int size) {
        if (n == 0)
            return head->next;
        ListNode* node_ptr = head->next;
        ListNode* prev_node_ptr = head;
        for (int i = 1; i < n; i++) {
            prev_node_ptr = node_ptr;
            node_ptr = node_ptr->next;
        }
        prev_node_ptr->next = node_ptr->next;
        return head;
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
    return head;
}

vector<int> list_to_vector(ListNode* head) {
    vector<int> result {};
    int c = 50; // sanity check
    for (ListNode* node_ptr = head; node_ptr != nullptr; node_ptr = node_ptr->next) {
        result.push_back(node_ptr->val);
        if (!(c--)) break;
    }
    return result;
}

TEST_CASE("Examples") {
    auto data = GENERATE(table<vector<int>, vector<int>, int>({
            {{1, 2, 3, 5}, {1, 2, 3, 4, 5}, 2},
            {{}, {1}, 1},
            {{1}, {1, 2}, 1},
    }));

    Solution *solution = new Solution();

    ListNode * expected = vector_to_list(get<0>(data));
    ListNode * head = vector_to_list(get<1>(data));
    int n = get<2>(data);

    ListNode * observed = solution->removeNthFromEnd(head, n);

    REQUIRE(list_to_vector(expected) == list_to_vector(observed));
}

// Input: head = [1,2,3,4,5], n = 2
// Output: [1,2,3,5]
//
// Example 2:
// Input: head = [1], n = 1
// Output: []
//
// Example 3:
// Input: head = [1,2], n = 1
// Output: [1]
