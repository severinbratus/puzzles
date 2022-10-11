#include <bits/stdc++.h>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

// Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
//
// Implement the LRUCache class:
//
// `LRUCache(int capacity)` Initialize the LRU cache with positive size capacity.
// `int get(int key)` Return the value of the key if the key exists, otherwise return -1.
// `void put(int key, int value)` Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.
// The functions get and put must each run in O(1) average time complexity.

class LRUCache {
    int capacity = 0;
    int size = 0;
    unordered_map<int, int> store {};
    unordered_map<int, int> last_accessed {};

    int time = 0;
    queue<pair<int, int>> tq;

public:
    LRUCache(int _capacity) {
        capacity = _capacity;
    }

    int get(int key) {
        if (store.count(key)) {
            time++;
            tq.push(make_pair(time, key));
            last_accessed[key] = time;
            return store[key];
        }
        return -1;
    }

    void put(int key, int value) {
        time++;
        tq.push(make_pair(time, key));
        last_accessed[key] = time;

        if (store.count(key)) {
            store[key] = value;
            return;
        }

        if (size < capacity) {
            // Add
            size++;
        } else {
            // First, remove stale entries from tq:
            // last_accessed[tq.front().second] should equal tq.front().first
            // tq.front().first could be stale (less).
            while (last_accessed[tq.front().second] > tq.front().first) {
                tq.pop();
            }
            // Evict a non-stale key least recently accessed
            int key_to_evict = tq.front().second;
            tq.pop();
            store.erase(key_to_evict);
        }

        store[key] = value;
    }
};


// Input
// ["LRUCache","put","put","get","put","get","put","get","get","get"]
// [[2],       [1,1],[2,2],[1],  [3,3],[2],  [4,4],[1],  [3],  [4]]
// Output
// [null,      null, null, 1,    null, 2,    null, -1,   3,   4]
// Expected
// [null,      null, null, 1,    null, -1,   null, -1,   3,   4]

TEST_CASE("Example #1") {
    LRUCache* obj = new LRUCache(2);
    obj->put(1,1);
    obj->put(2,2);
    REQUIRE(1 == obj->get(1));
    obj->put(3,3);
    REQUIRE(-1 == obj->get(2));
}

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache* obj = new LRUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */

// NOTE:
// I know this was supposed to be solved with a doubly linked list.
// I do not care.
// I do not like doubly linked lists.
//
// Runtime: 474 ms, faster than 87.40% of C++ online submissions for LRU Cache.
// Memory Usage: 165.3 MB, less than 63.96% of C++ online submissions for LRU Cache.
