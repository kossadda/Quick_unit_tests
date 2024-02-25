import sys
import numpy as np
from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_HALF_EVEN, ROUND_FLOOR

# Convert operation "decimal_to_float".
def decimal_to_float(func):
  num = Decimal(sys.argv[1])
  res = 0.0
  code = 0

  hex_num = decimal_to_hex_string(num, "value")
  res = np.float32(num)
  res = '{:.6f}'.format(res)

  print("  char *example = \"", func, "(", num, ") = ", res, "\";", sep="")
  print(hex_num)
  print("  float result = ", res, ";", sep="")
  print("  int code = ", code, ";", sep="")

# Convert operation "decimal_to_int".
def decimal_to_int(func):
  num = Decimal(sys.argv[1])
  res = 0
  code = 0
  temp = 0

  hex_num = decimal_to_hex_string(num, "value")
  num = num.quantize(Decimal('1'), rounding=ROUND_DOWN)
  
  if num > 2147483647 or num < -2147483648:
    code = 1
  else:
    res = num

  print("  char *example = \"", func, "(", sys.argv[1], ") = ", res, "\";", sep="")
  print(hex_num)
  print("  int result = ", res, ";", sep="")
  print("  int code = ", code, ";", sep="")

# Convert "int_to_decimal".
def int_to_decimal(func):
  num = Decimal(sys.argv[1])
  res = 0
  code = 0
  temp = 0

  if num > 2147483647 or num < -2147483648:
    code = 1
    hex_res = "  s21_decimal result = {{0x0, 0x0, 0x0, 0x0}};"
  else:
    res = num
    hex_res, temp = decimal_to_hex_string(res, "result")

  print("  char *example = \"", func, "(", num, ") = ", res, "\";", sep="")
  print("  int value = ", num, ";", sep="")
  print(hex_res)
  print("  int code = ", code, ";", sep="")

# Convert operation "float_to_decimal".
def float_to_decimal(func):
  num = Decimal(sys.argv[1])
  res = num
  integer_part = len(str(abs(num)).split('.')[0])

  if abs(res) < 1:
    res = res.normalize()
    res = res.quantize(Decimal('1e-{}'.format(8)), rounding=ROUND_DOWN)
    res = res.quantize(Decimal('1e-{}'.format(7)), rounding=ROUND_HALF_EVEN)
  elif integer_part >= 8:
    sign = 1
    
    if res < 0:
      sign = -1
    
    str_res = str(abs(res))
    str_res = str_res[:8]
    res = Decimal(str_res) / 10
    res = res.quantize(Decimal('1e-{}'.format(0)), rounding=ROUND_HALF_EVEN)
  else:
    res = res.normalize()
    res = res.quantize(Decimal('1e-{}'.format(8 - integer_part)), rounding=ROUND_DOWN)
    res = res.quantize(Decimal('1e-{}'.format(7 - integer_part)), rounding=ROUND_HALF_EVEN)

  hex_res, code = decimal_to_hex_string(res, "result")

  print("  char *example = \"", func, "(", num, ") = ", res, "\";", sep="")
  print("  float value = ", num, ";", sep="")
  print(hex_res)
  print("  int code = ", code, ";", sep="")

# Round operations ("round", "floor", "truncate", "negate").
def round_operations(func):
  getcontext().prec = 29

  num = Decimal(sys.argv[1])
  res = 0

  if func == "round":
    res = num.quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)
  elif func == "floor":
    res = num.quantize(Decimal('1'), rounding=ROUND_FLOOR)
  elif func == "truncate":
    res = num.quantize(Decimal('1'), rounding=ROUND_DOWN)
  elif func == "negate":
    res = num * (-1)

  hex_res, code = decimal_to_hex_string(res, "result")
  hex = decimal_to_hex_string(num, "value")

  print("  char *example = \"", func, "(", num, ") = ", res, "\";", sep="")
  print(hex)
  print(hex_res)
  print("  int code = ", code, ";", sep="")

# Arithmetic & comparisons (common function for call).
def binary_operations(func):
  getcontext().prec = 60

  num1 = Decimal(sys.argv[1])
  num2 = Decimal(sys.argv[3])
  res = 0
  math = 0

  if func == "+":
    res = num1 + num2
    math = 1
  elif func == "-":
    res = num1 - num2
    math = 1
  elif func == "*":
    res = num1 * num2
    math = 1
  elif func == "/":
    if num2 != 0:
      res = num1 / num2
    math = 1
  elif func == "%":
    res = num1 % num2
    math = 1

  if math:
    arithmetic(num1, num2, res, func)
  else:
    if func == "==" or func == "!=" or func == "<" or func == "<=" or func == ">" or func == ">=":
      comparison(num1, num2, func)

# Comparisons ("==", "!=", "<", "<=", ">", ">=").
def comparison(num1, num2, func):
  getcontext().prec = 28

  code = 0

  if func == "==":
    code = num1 == num2
  elif func == "!=":
    code = num1 != num2
  elif func == "<":
    code = num1 < num2
  elif func == "<=":
    code = num1 <= num2
  elif func == ">":
    code = num1 > num2
  elif func == ">=":
    code = num1 >= num2

  hex1 = decimal_to_hex_string(num1, "value_1")
  hex2 = decimal_to_hex_string(num2, "value_2")

  print("  char *example = \"( ", num1, " ", func, " ", num2, " ) = ", code, "\";", sep="")
  code *= 1
  print(hex1)
  print(hex2)
  print("  int code = ", code, ";", sep="")

# Arithmetic ("+", "-", "*", "/", "%").
def arithmetic(num1, num2, res, func):
  hex1 = decimal_to_hex_string(num1, "value_1")
  hex2 = decimal_to_hex_string(num2, "value_2")
  if num2 == 0 and func == "/":
    hex_res = "  s21_decimal result = {{0x0, 0x0, 0x0, 0x0}};"
    code = 3
  elif num1 != 0 and res < 1e-28:
    res.quantize(Decimal('1e-{}'.format(28)), rounding=ROUND_HALF_EVEN)
    if res == 0:
      hex_res = "  s21_decimal result = {{0x0, 0x0, 0x0, 0x1C0000}};"
      code = 2
    else:
      hex_res, code = decimal_to_hex_string(res, "result")
  else:
    hex_res, code = decimal_to_hex_string(res, "result")

  print("  char *example = \"", num1, " ", func, " ", num2, " = ", res, "\";", sep="")
  print(hex1)
  print(hex2)
  print(hex_res)
  print("  int code = ", code, ";", sep="")

# Converting from py_decimal to structural view of hex massive.
def decimal_to_hex_string(decimal_value, val):
  exponent = 0
  is_negative = decimal_value < 0
  if is_negative:
    decimal_value = -decimal_value
  
  if val == "result" and decimal_value > 79228162514264337593543950335:
    if is_negative:
      return "  s21_decimal result = {{0x0, 0x0, 0x0, 0x0}};", "2"
    else:
      return "  s21_decimal result = {{0x0, 0x0, 0x0, 0x0}};", "1"

  while not (decimal_value == decimal_value.to_integral_value()):
    decimal_value *= 10
    exponent += 1
    
  num_binary = bin(int(decimal_value))[2:]
    
  while len(num_binary) > 96 or exponent >= 28:
    decimal_value /= 10
    exponent -= 1
    num_binary = bin(int(decimal_value))[2:]
    #if len(num_binary) > 96:
      #decimal_value = decimal_value.quantize(Decimal('1'), rounding=ROUND_DOWN)
    if len(num_binary) <= 96 and exponent <= 28:
      decimal_value = decimal_value.quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)
      num_binary = bin(int(decimal_value))[2:]
      break

  padded_binary = num_binary.zfill(((len(num_binary) + 31) // 32) * 32)

  def chunk_bits(bit_string, chunk_size):
    return [bit_string[i:i + chunk_size] for i in range(0, len(bit_string), chunk_size)]

  def bits_to_hex(chunks):
    return [hex(int(chunk, 2))[2:].upper() for chunk in chunks]

  chunk_size = 32
  binary_chunks = chunk_bits(padded_binary, chunk_size)
  hex_chunks = bits_to_hex(binary_chunks)

  hex_chunks.reverse()

  while len(hex_chunks) < 3:
    hex_chunks.append("0")

  formatted_string = f"  s21_decimal {val} = " + "{{" + ", ".join(["0x" + chunk for chunk in hex_chunks])

  last_mantiss = hex((is_negative << 31) | (exponent << 16))[2:].upper()
  formatted_string += ", {}".format("0x" + last_mantiss) + "}};"

  if val == "result":
    return formatted_string, "0"
  else:
    return formatted_string

# Main function to define test type.
def main():
  argc = len(sys.argv) - 1

  if argc == 2:
    func = sys.argv[2]
    if func == "round" or func == "floor" or func == "truncate" or func == "negate":
      round_operations(func)
    else:
      getcontext().prec = 29

      if func == "float_to_decimal":
        float_to_decimal(func)
      elif func == "int_to_decimal":
        int_to_decimal(func)
      elif func == "decimal_to_int":
        decimal_to_int(func)
      elif func == "decimal_to_float":
        decimal_to_float(func)
  elif argc == 3:
    func = sys.argv[2]
    binary_operations(func)

# Start script.
main()
