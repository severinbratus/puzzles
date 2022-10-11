#include <bits/stdc++.h>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    bool hasCycle(ListNode *head) {
        ListNode* slow;
        ListNode* fast;
        slow = fast = head;
        while (1) {
            if (fast == nullptr || fast->next == nullptr)
                return false;
            slow = slow->next;
            fast = fast->next->next;
            if (fast == slow) {
                return true;
            }
        }
    }
};

// O(1) memory! Idea (not mine):
// Have slow and fast pointers, latter one moving twice as fast as the former.
// If there is no cycle, the fast one will reach a null ptr.
// If there is a cycle, at some point the slow and the fast will reunite.
