#!/bin/bash

compile()
{
  gcc ./c_modules/test_module.c -o test -lm
  result=$(./test ${1})
}

generate_test()
{
  echo "/// @brief \f[ ${FUNCTION}(${1}) = ${result} \f]"
  echo "START_TEST(s21_${FUNCTION}_${2})"
  echo "{"
  echo "    double value = ${1};"
  echo
  echo "    ${TEST_FUNCTION}(value);"
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
