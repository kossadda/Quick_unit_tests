#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    double value_1 = atof(argv[1]);
    double value_2 = atof(argv[2]);

    long double result = pow(value_1, value_2);

    printf("%Lf", result);
    
    return 0;
}