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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        return helper(l1, l2, 0);
    }

    ListNode* helper(ListNode* l1, ListNode* l2, bool carry) {
        if (l2 == nullptr && l1 == nullptr) {
            if (!carry)
                return nullptr;
            else
                return new ListNode(1);
        }
        int v1 = l1 != nullptr ? l1->val : 0;
        int v2 = l2 != nullptr ? l2->val : 0;
        ListNode* n1 = l1 != nullptr ? l1->next : nullptr;
        ListNode* n2 = l2 != nullptr ? l2->next : nullptr;
        int sum = v1 + v2 + carry;
        return new ListNode(sum % 10, helper(n1, n2, sum / 10));
    }
};
