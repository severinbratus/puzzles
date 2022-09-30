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

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        // to be pointed at by the next node we add
        ListNode* reversed = nullptr;
        ListNode* next_node;
        for (ListNode* current_node = head; current_node != nullptr; current_node = next_node) {
            next_node = current_node->next;
            current_node->next = reversed;
            reversed = current_node;
        }
        return reversed;
    }
};

// Proud to say I *did not* mess anything up, and it worked from the first time.
// Linked lists are a weak spot of mine.
