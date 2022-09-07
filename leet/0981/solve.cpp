#include <bits/stdc++.h>
#include <vector>
using namespace std;

class TimeMap {
    unordered_map<string, map<int, string>> core {};
public:
    TimeMap() {

    }

    void set(string key, string value, int timestamp) {
        if (!core.count(key)) {
            core[key] = *new map<int, string>();
        }
        core[key][timestamp] = value;
    }

    string get(string key, int timestamp) {
        map<int, string> & core_by_key = core[key];
        // iterator to the first pair where timestamp is greater to the timestamp given.
        auto it = core_by_key.upper_bound(timestamp);
        // but we need to access the pair right before that one
        //   -- the timestamp that is less than or equal to the one given.
        if (it == core_by_key.begin()) {
            return "";
        }
        // go one pair back.
        it--;
        return (*it).second;
    }

};

/**
 * Your TimeMap object will be instantiated and called as such:
 * TimeMap* obj = new TimeMap();
 * obj->set(key,value,timestamp);
 * string param_2 = obj->get(key,timestamp);
 */

int main() {
    TimeMap* obj = new TimeMap();
    obj->set("foo", "bar", 1);
    assert(obj->get("foo", 1) == "bar");
}
