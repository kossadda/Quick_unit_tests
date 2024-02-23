#!/bin/bash

source ./generate_number.sh

complex_generate_for_tests()
{
  if [[ ${TEST_TYPE} == "binary" ]]; then
    for ((i = ${TEST_BEGIN}; i < ((${NUMBER_OF_TESTS} + ${TEST_BEGIN})); i++)); do
      generate_binary_test "${i}"
    done
  else
    for ((i = ${TEST_BEGIN}; i < ((${NUMBER_OF_TESTS} + ${TEST_BEGIN})); i++)); do
      generate_non_binary_test "${i}"
    done
  fi

  echo "#############################################################################"
  echo "#############################################################################"
  echo "#############################################################################"

  generate_suite
  generate_header >> module.h
}

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
  echo "  Suite *${SUITE_NAME} = suite_create(\"\\n${PROJECT_NAME} (${FUNCTION} case №${CASE_NUMBER})\\n\");"

  echo
  echo "  TCase *tc_${FUNCTION} = tcase_create(\"${FUNCTION}_test\");"
}

generate_tcase()
{
  echo "  tcase_add_test(tc_${FUNCTION}, ${FUNCTION}_${1});"
}

generate_end()
{
  echo "  suite_add_tcase(${SUITE_NAME}, tc_${FUNCTION});"
  echo
  echo "  return ${SUITE_NAME};"
  echo "}"
}

generate_suite()
{
  local count=${TEST_BEGIN}
  i=0

  for ((i = BEGIN_CASE; end_count != TEST_END; i++)); do
    generate_case ${i}
    end_count=$((count + TESTS_IN_CASE - 1))

    if ((end_count > TEST_END)); then
      end_count=${TEST_END}
    fi

    for ((j = count; j <= end_count; j++)); do
      generate_tcase "${j}"
    done

    count=$((end_count + 1))
    generate_end
  done
}

generate_header()
{
  for ((j = BEGIN_CASE; j < i; j++)); do
    echo "Suite *${FUNCTION}_case_${j}(void);"
  done
  
  echo

  echo "Suite *(*${FUNCTION}[])(void) = {"
  for ((j = BEGIN_CASE; j < i; j++)); do
    echo "  ${FUNCTION}_${j}_case,"
  done
  echo "};"
}
