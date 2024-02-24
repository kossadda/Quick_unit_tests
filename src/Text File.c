static void s21_test_add(s21_decimal value_1, s21_decimal value_2,
                         s21_decimal result, int code, char *text, int count) {
  s21_decimal implement_result = {{0x0}};
  int implement_code = s21_add(value_1, value_2, &implement_result);
  int res = (implement_code == code);

  if (res) {
    res += s21_is_equal(result, implement_result);
  }
#ifdef DEBUG
#ifndef ERRORS
  if(res == 2) {
#endif // ERRORS
  printf("Test №%d: %s\n%s%s\n", count, GREEN"TEST_PASSED", RESET"Subformul:   ", text);
#ifdef ERRORS
  }
#endif // ERRORS

  if(res != 2) {
    printf("Test №%d: %s\n%s%s\n", count, RED"TEST_FAILED", RESET"Subformul:   ", text);
    if (res == 0) {
      printf("Implementation code = %s%d%s\nOriginal funcs code = %s%d%s\n\n", RED, implement_code, RESET, RED, code, RESET);
    }
    both_decimal_bits(implement_result, result);
    printf("\n");
  }
#endif // DEBUG

  ck_assert_int_eq(res, 2);
}
