#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define max(a, b) ((a) > (b) ? (a) : (b))
#define min(a, b) ((a) < (b) ? (a) : (b))

int get_bit_len(uint);

/* straight-forward implementation */
int getSum(int a, int b){
    /* int len_a = get_bit_len(a); */
    /* int len_b = get_bit_len(b); */
    /* int len = max(len_a, len_b); */
    ulong sum = 0;
    ulong carry = 0;
    ulong xor_a_b = a ^ b;
    ulong and_a_b = a & b;

    for (ulong shift = 1; shift < (1UL << 32); shift <<= 1) {
        sum ^= (xor_a_b ^ carry) & shift;
        carry ^= ((and_a_b | (carry & b) | (carry & a)) << 1) & (shift << 1);
        /* printf("idx: %d\n", i); */
        /* printf("car: %08x\n", carry); */
        /* printf("  a: %08x %d\n", a, get_bit_len(a)); */
        /* printf("  b: %08x %d\n", b, get_bit_len(b)); */
        /* printf("sum: %08x\n", sum); */
        /* printf("\n"); */
    }
    return sum;
}


/* better implemntation (not mine) */
int getSumSuperb(int base, int carry){
    int xorred;
    while (carry) {
        xorred = base ^ carry;
        carry = (unsigned)(base & carry) << 1;
        base = xorred;
    }
    return base;
}


int get_bit_len(uint num) {
    int len = 0;
    while (num) {
        num >>= 1;
        len++;
    }
    return len;
}

int main(int argc, char *argv[]) {
    if (argc == 3) {
        int a = atoi(argv[1]);
        int b = atoi(argv[2]);
        printf("%d\n", getSum(a, b));
    } else {
        printf("Invalid usage.\n");
    }
}
