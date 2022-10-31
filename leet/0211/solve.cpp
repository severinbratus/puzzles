#define CATCH_CONFIG_MAIN
#include "../../leet/hpp/catch.hpp"
#include "../../leet/hpp/prettyprint.hpp"

#include <bits/stdc++.h>
using namespace std;

class TrieNode {
public:
    map<char, TrieNode*> refs {};
    bool isWord = false;
    TrieNode() {
    }
};

class WordDictionary {
    TrieNode root {};
    unordered_set<string> store {};
public:
    WordDictionary() {
    }

    void addWord(string word) {
        store.insert(word);
        TrieNode* node = &root;
        for (const char & c : word) {
            if (!node->refs.count(c - 'a')) {
                node->refs[c - 'a'] = new TrieNode();
            }
            node = node->refs[c - 'a'];
        }
        node->isWord = true;
    }

    bool search(string word) {
        return store.count(word) or search(word, 0, &root);
    }

    bool search(string word, int index, TrieNode* node) {
        if (index == word.size())
            return node->isWord;
        char c = word[index];
        if (c != '.') {
            // literal match
            return node->refs.count(c - 'a') and search(word, index + 1, node->refs[c - 'a']);
        } else {
            // wildcard match
            for (const auto kv : node->refs) {
                auto k = kv.first;
                auto v = kv.second;
                if (search(word, index + 1, v)) {
                    return true;
                }
            }
            return false;
        }
    }
};

TEST_CASE("#1") {
    WordDictionary wd {};
    wd.addWord("hello");
    REQUIRE(wd.search("hello"));
    REQUIRE(wd.search(".ello"));
    REQUIRE(wd.search("h.llo"));
    REQUIRE(wd.search("..llo"));
    REQUIRE(wd.search("...lo"));
}
