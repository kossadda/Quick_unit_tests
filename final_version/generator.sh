#!/bin/bash

# Global:
#   argument - argument of the function
compile()
{
    gcc ./test_module.c -o test -lm
    result=$(./test ${argument})
    # echo ${result}
}

# Global:
#   testing_func - function name
#   argument - argument of the function
#   result - compilation result of the original function
#   comparison_func - comparison function name 
#   test_number - first test number
generate_test()
{
    echo "/// @brief \f[ ${testing_func}(${argument}) = ${result} \f]"
    echo "START_TEST(${testing_func}_${test_number})"
    echo "{"
    echo "    double value = ${argument};"
    echo
    echo "    ${comparison_func}(value);"
    echo "}"
    echo
}