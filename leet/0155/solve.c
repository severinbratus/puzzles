#include <stdlib.h>
#include <assert.h>

#define MAX_CALLS (3 * 10000)
#define max(x, y) ((x) < (y) ? (y) : (x))
#define min(x, y) ((x) > (y) ? (y) : (x))

typedef struct {
    int size;
    int stack[MAX_CALLS];
    int mins[MAX_CALLS];
} MinStack;

MinStack* minStackCreate() {
    MinStack* minstack_ptr = (MinStack*) malloc(sizeof(MinStack));
    minstack_ptr->size = 0;
    return minstack_ptr;
}

void minStackPush(MinStack* obj, int val) {
    obj->stack[obj->size] = val;
    obj->mins[obj->size] = obj-> size > 0 ? min(val, obj->mins[obj->size - 1]) : val;
    obj->size++;
}

void minStackPop(MinStack* obj) {
    if (obj->size > 0)
        obj->size--;
}

int minStackTop(MinStack* obj) {
    return obj->size > 0 ? obj->stack[obj->size - 1] : 0;
}

int minStackGetMin(MinStack* obj) {
    return obj->size > 0 ? obj->mins[obj->size - 1] : 0;
}

void minStackFree(MinStack* obj) {
    free(obj);
}

/**
 * Your MinStack struct will be instantiated and called as such:
 *
 * MinStack* obj = minStackCreate();
 * ...
 * minStackFree(obj);
 *
 * At most 3 * 10^4 calls will be made to push, pop, top, and getMin.
*/

void test_1(void);
void test_2(void);

int main() {
    test_1();
    test_2();
}

void test_1(void) {
    MinStack* obj = minStackCreate();

    minStackPush(obj, 4);
    assert(minStackTop(obj) == 4);
    assert(minStackGetMin(obj) == 4);
    // [4]

    minStackPush(obj, 3);
    assert(minStackTop(obj) == 3);
    assert(minStackGetMin(obj) == 3);
    // [4, 3]

    minStackPush(obj, 2);
    assert(minStackTop(obj) == 2);
    assert(minStackGetMin(obj) == 2);
    // [4, 3, 2]

    minStackPush(obj, 5);
    assert(minStackTop(obj) == 5);
    assert(minStackGetMin(obj) == 2);
    // [4, 3, 2, 5]


    minStackPush(obj, 1);
    assert(minStackTop(obj) == 1);
    assert(minStackGetMin(obj) == 1);
    // [4, 3, 2, 5, 1]

    minStackPop(obj);
    assert(minStackTop(obj) == 5);
    assert(minStackGetMin(obj) == 2);
    // [4, 3, 2, 5]

    minStackFree(obj);
}

void test_2() {
    MinStack* obj = minStackCreate();
    // Input: ["MinStack","push -2","push 0","push -1","getMin","top","pop","getMin"]
    // Output: [null,null,null,null,-1,-1,null,-2]
    // Expected: [null,null,null,null,-2,-1,null,-2]
    minStackPush(obj, -2);
    minStackPush(obj, 0);
    minStackPush(obj, -1);
    assert(minStackGetMin(obj) == -2);
    minStackFree(obj);
}
