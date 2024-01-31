#!/bin/bash

compile()
{
    # gcc ./test_module.c -o test -lm
    result=$(./test ${1})
    echo ${result}
}

# $1 - тестируемая функция
# $2 - тестируемое значение
# $3 - результат вычисления
# $4 - номер теста
print_test()
{
    echo "/// @brief \f[ ${1}(${2}) = ${3} \f]"
    echo "START_TEST(s21_${1}_${4})"
    echo "{"
    echo "    double value = ${2};"
    echo
    echo "    s21_test_${1}(value);"
    echo "}"
    echo
}



# $1 - начальное значение
# $2 - конечное значение
# $3 - шаг
# $4 - тестируемая функция
# $5 - номер кейса
# $6 - название проекта
# $7 - номер первого теста
suite_creator()
{
    local first_test=${7}

    echo
    echo "/**"
    echo " * @brief Checking values in the interval (${1};${2}) with step ${3}"
    echo
    echo " * @return Suite*"
    echo " */"
    echo "Suite *s21_${4}_case_${5}(void)"
    echo "{"
    echo "    Suite *${6} = suite_create(\"s21_${6} (s21_${4} case ${5})\");"
    echo
    echo "    TCase *tc_${4} = tcase_create("test_${4}");"
    
    for(( i = 0; i < 100; i++ )); do
        echo "    tcase_add_test(tc_${4}, s21_${4}_${first_test});"
        ((first_test++))
    done

    echo "    suite_add_tcase(${6}, tc_${4});"
    echo
    echo "    return ${6}"
    echo "}"
}

# suite_creator "0.001" "1" "0.001" "log" "623" "math"