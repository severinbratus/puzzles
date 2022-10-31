#include <bits/stdc++.h>
using namespace std;

class TrieNode {
public:
    TrieNode* refs[26];
    bool isWord = false;
    TrieNode() {
        for (int i = 0; i < 26; i++) {
            refs[i] = nullptr;
        }
    }
};

class Trie {
public:
    TrieNode root {};

    Trie() {

    }

    void insert(string word) {
        TrieNode* node = &root;
        for (const char & c : word) {
            if (node->refs[c - 'a'] == nullptr) {
                node->refs[c - 'a'] = new TrieNode();
            }
            node = node->refs[c - 'a'];
        }
        node->isWord = true;
    }

    bool search(string word) {
        TrieNode* node = &root;
        for (const char & c : word) {
            if (node->refs[c - 'a'] == nullptr) {
                return false;
            }
            node = node->refs[c - 'a'];
        }
        return node->isWord;
    }

    bool startsWith(string prefix) {
        TrieNode* node = &root;
        for (const char & c : prefix) {
            if (node->refs[c - 'a'] == nullptr) {
                return false;
            }
            node = node->refs[c - 'a'];
        }
        return true;
    }
};
