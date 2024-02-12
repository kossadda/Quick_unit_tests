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
  echo " * @brief ${CASE_NUMBER} set of tests"
  echo " *"
  echo " * @return Suite*"
  echo " */"
  echo "Suite *${PROJECT_NAME}_${CASE_NUMBER}_case(void)"
  echo "{"
  echo "    Suite *${SUITE_NAME} = suite_create(\"\\n${PROJECT_NAME} (s21_${FUNCTION} ${CASE_NUMBER} case)\\n\");"
  echo
  echo "    TCase *tc_${FUNCTION} = tcase_create("test_${FUNCTION}");"
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
