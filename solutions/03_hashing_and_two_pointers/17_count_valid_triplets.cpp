#include<bits/stdc++.h>
using namespace std;

// Count Valid Triplets: (i < j < k) such that (arr[i] + arr[j] + arr[k]) % m == 0
// Time Complexity: O(K^2) where K = min(N, m) <= 2000
// Space Complexity: O(K)
class solution {
    struct Rem {
        long long val;
        long long count;
        bool operator<(const Rem& o) const { return val < o.val; }
    };

public:
    int countTriplets(vector<long long>& arr, int m) {
        unordered_map<long long, long long> freq;
        for (long long x : arr) {
            long long r = (x % m + m) % m;
            freq[r]++;
        }
        
        vector<Rem> rems;
        rems.reserve(freq.size());
        for (const auto& p : freq) {
            rems.push_back({p.first, p.second});
        }
        sort(rems.begin(), rems.end());
        
        int K = rems.size();
        long long ans = 0;
        
        // Case 1: 3 elements with same remainder
        for (const auto& r : rems) {
            if ((3 * r.val) % m == 0 && r.count >= 3) {
                long long c = r.count;
                ans += c * (c - 1) * (c - 2) / 6;
            }
        }
        
        // Case 2: 2 elements with remainder u, 1 with v (u != v)
        for (const auto& r : rems) {
            if (r.count >= 2) {
                long long v = (m - (2 * r.val) % m) % m;
                if (v != r.val) {
                    auto it = lower_bound(rems.begin(), rems.end(), Rem{v, 0});
                    if (it != rems.end() && it->val == v) {
                        long long c = r.count;
                        ans += (c * (c - 1) / 2) * it->count;
                    }
                }
            }
        }
        
        // Case 3: 3 distinct remainders u < v < w
        for (int i = 0; i < K; ++i) {
            long long u_val = rems[i].val;
            long long u_cnt = rems[i].count;
            for (int j = i + 1; j < K; ++j) {
                long long v_val = rems[j].val;
                long long v_cnt = rems[j].count;
                long long w = (m - (u_val + v_val) % m) % m;
                if (w > v_val) {
                    auto it = lower_bound(rems.begin() + j + 1, rems.end(), Rem{w, 0});
                    if (it != rems.end() && it->val == w) {
                        ans += u_cnt * v_cnt * it->count;
                    }
                }
            }
        }
        
        return (int)ans;
    }
};
