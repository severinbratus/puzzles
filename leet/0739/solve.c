#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* dailyTemperatures(int* temperatures, int temperatures_size, int* answer_size_ptr){
    *answer_size_ptr = temperatures_size;
    int* answer = (int*) malloc(sizeof(int) * temperatures_size);
    /* memset(answer, 0, sizeof(int) * temperatures_size); */
    int n = temperatures_size;
    int stack[temperatures_size];
    int stack_size = 0;
    for (int index = 0; index < n; index++) {
        int new_value = temperatures[index];
        // pop all those values lesser than the new value
        while (stack_size != 0) {
            if (temperatures[stack[stack_size - 1]] < new_value) {
                int top_index = stack[stack_size - 1];
                answer[top_index] = index - top_index;
                stack_size--;
            } else {
                break;
            }
        }
        // add this index to the stack to be cleared later
        stack[stack_size] = index;
        stack_size++;
    }
    // for those temperatures still in the stack, write 0
    for (int j = 0; j < stack_size; j++) {
        answer[stack[j]] = 0;
    }
    return answer;
}

int main(int argc, char *argv[]) {
    int input_size = argc - 1;
    int input[input_size];
    for (int arg_idx = 1; arg_idx < argc; arg_idx++) {
        input[arg_idx - 1] = atoi(argv[arg_idx]);
    }
    int * answer_result_ptr = malloc(sizeof(int));
    int * answer = dailyTemperatures(input, input_size, answer_result_ptr);
    assert(*answer_result_ptr == input_size);
    for (int i = 0; i < *answer_result_ptr; i++) {
        printf("%d ", answer[i]);
    }
    printf("\n");
    free(answer_result_ptr);
}

// so... uhm.... apparently this solution is slower than 94% of solutions on LC, but uses less memory than 91% of solutions on LC.
