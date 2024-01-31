#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    double value = atof(argv[1]);

    long double result = log(value);

    printf("%Lf", result);
    
    return 0;
}