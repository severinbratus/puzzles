#include <bits/stdc++.h>
#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

void print() {
    cout << '\n';
}

template<typename T, typename ...TAIL>
void print(const T &t, TAIL... tail)
{
    cout << t << ' ';
    print(tail...);
}

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

vector<int> list_to_vector(ListNode* head);

class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        int size = findSize(head);
        int num_groups = size / k;
        ListNode result_dummy_head {};
        ListNode* result_tail = &result_dummy_head;

        for (int g_idx = 0; g_idx < num_groups; g_idx++) {

            // reverse the group of k elements
            ListNode* group_reversed = nullptr;
            ListNode* next_node;
            ListNode* current_node = head;
            for (int i = 0; i < k; i++) {
                next_node = current_node->next;
                current_node->next = group_reversed;
                group_reversed = current_node;
                current_node = next_node;
            }

            // join the reversed group to the result
            result_tail->next = group_reversed;
            result_tail = head;
            // update the head to be what was left unreversed
            head = current_node;

        }

        // join the left-over part
        result_tail->next = head;

        return result_dummy_head.next;
    }

    int findSize(ListNode* head) {
        return (head == nullptr) ? 0 : findSize(head->next) + 1;
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
            {{1}, {1}, 1},
            {{1, 2}, {1, 2}, 1},
            {{2, 1}, {1, 2}, 2},
            {{2, 1, 4, 3, 5}, {1, 2, 3, 4, 5}, 2},
            {{3, 2, 1, 4, 5}, {1, 2, 3, 4, 5}, 3},
            {{3, 2, 1, 6, 5, 4}, {1, 2, 3, 4, 5, 6}, 3},
    }));

    Solution *solution = new Solution();

    ListNode * expected = vector_to_list(get<0>(data));
    ListNode * head = vector_to_list(get<1>(data));
    int k = get<2>(data);

    ListNode * observed = solution->reverseKGroup(head, k);

    REQUIRE(list_to_vector(expected) == list_to_vector(observed));
}
