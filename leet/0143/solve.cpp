#include <bits/stdc++.h>
#include <unordered_set>

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

int next(int i, int n) {
    // equilibrium point: `i` right in the middle
    if (n % 2 == 1 and n / 2 == i)
        return i;
    // otherwise, reflect, and perhaps increment
    int j = n - 1 - i;
    if (i < n / 2)
        return j;
    else
        return j + 1;
}

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
    void reorderList(ListNode* head) {
        vector<ListNode*> whole {};
        for (ListNode* node_ptr = head; node_ptr != nullptr; node_ptr = node_ptr->next) {
            whole.push_back(node_ptr);
        }
        int n = whole.size();
        int c = n;
        int a, b;
        a = 0;
        for (int i = 0; i < n; i++) {
            b = next(a, n);
            whole[a]->next = whole[b];
            a = b;
        }
        whole[a]->next = nullptr;
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
    auto data = GENERATE(table<vector<int>, vector<int>>({
                {{1}, {1}},
                {{1, 2}, {1, 2}},
                {{1, 3, 2}, {1, 2, 3}},
                {{1, 4, 2, 3}, {1, 2, 3, 4}},
                {{1, 5, 2, 4, 3}, {1, 2, 3, 4, 5}},
    }));

    Solution *solution = new Solution();

    ListNode * expected = vector_to_list(get<0>(data));
    ListNode * observed = vector_to_list(get<1>(data));

    solution->reorderList(observed);

    REQUIRE(list_to_vector(expected) == list_to_vector(observed));
}

// Not a big fan of linked lists.
