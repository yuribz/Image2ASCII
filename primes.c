#include <stdio.h>
#include <stdbool.h>
#include <math.h>

int bound = 10000000;

int count = 0;

int i = 2;



int main(int argc, char *argv[]){
    while (i <= bound){
        bool is_prime = true;
        for (int j = 2; j < pow(i, 0.5); j++) {
            if (i % j == 0) {
                is_prime = false;
                break;
            }
        }
        if (is_prime) {
            count++;
        }
        i++;
    }

    printf("Found %d primes!\n", count);
}