/*
 * We establish the lower and upper bounds for the search for some value of a parameter (k),
 *   such that k is minimal and has a certain property P(x).
 * Code speaks louder than words:
 *   [lower_k, ..., upper_k].map(P) === [false, ..., true]
 * We have to find the value of `k` between `lower_k` and `upper_k` right when P(k) *becomes* `true`.
 */

int minEatingSpeed(int* piles, int piles_size, int allowed_hours){
    long sum = 0;
    int max_pile = INT32_MIN;
    for (int i = 0; i < piles_size; i++) {
        int pile = piles[i];
        sum += pile;
        if (pile > max_pile)
            max_pile = pile;
    }
    int lower_k = sum / allowed_hours;
    int upper_k = max_pile;
    int mid_k, hours;
    while (lower_k <= upper_k) {
        mid_k = (lower_k + upper_k) / 2;
        // this is an edge-case where mid_k was one, but devolved into zero.
        // if left unchecked, will cause division by zero (SIGFPE).
        if (mid_k == 0)
            return 1;
        // now check if the time it takes for koko to eat all the bananas is less than the allowed time.
        hours = 0;
        for (int i = 0; i < piles_size; i++) {
            // ceiled division
            hours += piles[i] / mid_k;
            if (piles[i] % mid_k)
                hours++;
        }
        if (hours <= allowed_hours) {
            // possible w/ speed = mid_k, but may not be the minimal solution.
            // move left.
            upper_k = mid_k - 1;
        } else {
            // move right
            lower_k = mid_k + 1;
        }
    }
    if (hours <= allowed_hours)
        return mid_k;
    else
        return mid_k + 1;
}
