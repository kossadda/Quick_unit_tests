#!/bin/bash

source ./generate_number.sh

generate_binary_test()
{
  echo "START_TEST(${FUNCTION}_${1})"
  echo "{"
  ./dist/decimal_calc/decimal_calc $(generate_float_decimal) "${OPERATION}" $(generate_float_decimal)
  echo
  echo "  ${TEST_FUNCTION}(value_1, value_2, result, code);"
  echo "}"
  echo
}

generate_non_binary_test()
{
  local value="0"

  if [[ ${OPERATION} == "int_to_decimal" ]]; then
    value=$(generate_int)
  else
    value=$(generate_float_decimal)
  fi

  echo "START_TEST(${FUNCTION}_${1})"
  echo "{"
  ./dist/decimal_calc/decimal_calc ${value} "${OPERATION}"
  echo
  echo "  ${TEST_FUNCTION}(value_1, result, code);"
  echo "}"
  echo
}

generate_case()
{
  CASE_NUMBER=$1
  echo
  echo "/**"
  echo " * @brief Set №${CASE_NUMBER} of ${SUITE_NAME} tests"
  echo " *"
  echo " * @return Suite*"
  echo " */"
  echo "Suite *${FUNCTION}_case_${CASE_NUMBER}(void)"
  echo "{"
  echo "    Suite *${SUITE_NAME} = suite_create(\"\\n${PROJECT_NAME} (${FUNCTION} case №${CASE_NUMBER})\\n\");"

  echo
  echo "    TCase *tc_${FUNCTION} = tcase_create(\"${FUNCTION}_test\");"
}

generate_tcase()
{
  echo "    tcase_add_test(tc_${FUNCTION}, ${FUNCTION}_${1});"
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

