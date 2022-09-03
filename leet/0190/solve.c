#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

uint32_t reverseBitsNaive(uint32_t n) {
    uint8_t canvas = 0;
    for (uint32_t i = 0; i < 32; i++) {
        uint8_t j = 31 - i;
        canvas ^= ((((UINT32_C(1) << i) & n) >> i) << j);
    }
    return canvas;
}

uint32_t reverseBits(uint32_t n) {
    uint32_t canvas = 0;
    uint8_t countdown = 32;
    while (countdown--) {
        canvas <<= 1; // shift the canvas before copying
        canvas |= (1 & n);
        n >>= 1;
    }
    return canvas;
}


int main(int argc, char *argv[]) {
    printf("%08x", reverseBits(atoi(argv[1])));
}
