#!/bin/bash

compile()
{
  gcc ./c_modules/test_module.c -o test -lm
  result=$(./test ${1})
}

generate_test()
{
  echo "/// ${1} + ${2} = ${3}"
  echo "START_TEST(${FUNCTION}_${7})"
  echo "{"
  echo "    s21_decimal value_1 = ${4};"
  echo "    s21_decimal value_2 = ${5};"
  echo "    s21_decimal result = ${6};"
  echo
  echo "    ${TEST_FUNCTION}(value_1, value_2, &result);"
  echo "}"
  echo
}

generate_case()
{
  echo
  echo "/**"
  echo " * @brief ${CASE_NUMBER[$1]} set of tests"
  echo " *"
  echo " * @return Suite*"
  echo " */"
  echo "Suite *s21_${FUNCTION}_${CASE_NUMBER[$1]}_case(void)"
  echo "{"
  echo "    Suite *${SUITE_NAME} = suite_create(\"\\n${PROJECT_NAME} (s21_${FUNCTION} ${CASE_NUMBER[$1]} case)\\n\");"

  echo
  echo "    TCase *tc_${FUNCTION} = tcase_create(\"test_${FUNCTION}\");"
}

generate_tcase()
{
  echo "    tcase_add_test(tc_${FUNCTION}, s21_${FUNCTION}_${1});"
}

generate_end()
{
  echo "    suite_add_tcase(${SUITE_NAME}, tc_${FUNCTION});"
  echo
  echo "    return ${SUITE_NAME};"
  echo "}"
}

generate_list_for_header()
{
  echo "Suite *s21_${FUNCTION}_${CASE_NUMBER[$1]}_case(void);"
}

generate_array_start()
{
  echo "Suite *(*s21_${FUNCTION}[])(void) = {"
}
generate_array_end()
{
  echo "};"
}

generate_array()
{
  echo "    s21_${FUNCTION}_${CASE_NUMBER[$1]}_case,"
}

generate_num()
{
  local VALUE_1
  
  for ((i = 0; i < 28; i++)); do
    VALUE_1="${VALUE_1}$((RANDOM % 10))"

    if ((VALUE_1 == "0")); then
      VALUE_1=""
    fi

    if ((((RANDOM % 15)) == 0)); then
      break
    fi
  done

  echo -n ${VALUE_1}
}

generate_decimal_1()
{
  VALUE_1=$(generate_num)
  DECIMAL_1=$(./test_module/test_module ${VALUE_1})
}

generate_decimal_2()
{
  VALUE_2=$(generate_num)
  DECIMAL_2=$(./test_module/test_module ${VALUE_2})
}