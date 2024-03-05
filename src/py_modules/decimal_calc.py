import sys
import random
import numpy as np
from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_HALF_EVEN, ROUND_FLOOR, ROUND_HALF_UP

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
  if '.' in sys.argv[1]:
    print("  float result = ", res, ";", sep="")
  else:
    print("  float result = ", res, ".0;", sep="")
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
  exponent = 0

  res = np.float32(num) 
  res = '{:.28f}'.format(res)
  res = Decimal(res)

  if abs(res) < 1:
    integer_part = 0
  else:
    integer_part = len(str(abs(res)).split('.')[0])
  
  if integer_part == 0:
    while integer_part != 7 and num != 0:
      res *= 10
      exponent += 1
      if abs(res) < 1:
        integer_part = 0
      else:
        integer_part = len(str(abs(res)).split('.')[0])
    res = res.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    res /= 10 ** exponent
  elif integer_part >= 8:
    sign = 1
    
    if res < 0:
      sign = -1
    
    str_res = str(abs(res))
    str_res = str_res[:8]
    res = Decimal(str_res) / 10 * sign
    res = res.quantize(Decimal('1e-{}'.format(0)), rounding=ROUND_HALF_UP)
    res *= 10 ** (integer_part - len(str(abs(res)).split('.')[0]))
  else:
    res = res.normalize()
    res = res.quantize(Decimal('1e-{}'.format(7 - integer_part)), rounding=ROUND_HALF_UP)

  hex_res, code = decimal_to_hex_string(res, "result")

  if abs(num) > 79228162514264337593543950335:
    hex_res = "  s21_decimal result = {{0x0, 0x0, 0x0, 0x0}};"
    code = 1

  print("  char *example = \"", func, "(", num, ") = ", res, "\";", sep="")
  if '.' in sys.argv[1]:
    print("  float value = ", num, ";", sep="")
  else:
    print("  float value = ", num, ".0;", sep="")
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
  equal = 0
  if random.random() > 0.9:
    temp = num1
    while not (temp == temp.to_integral_value()):
      temp *= 10
    if abs(temp) < 1000000000:
      num2 = num1
      equal = 1

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

  if equal == 0:
    hex1 = decimal_to_hex_string(num1, "value_1")
    hex2 = decimal_to_hex_string(num2, "value_2")
  else:
    hex1, hex2 = decimal_to_equal_string(num1)

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
  elif (num1 == 0 or num2 == 0) and func == "*":
    hex_res = "  s21_decimal result = {{0x0, 0x0, 0x0, 0x0}};"
    code = 0
  elif num1 != 0 and abs(res) < 1e-28:
    res = res.quantize(Decimal('1e-{}'.format(28)), rounding=ROUND_HALF_EVEN)
    if res == 0:
      hex_res = "  s21_decimal result = {{0x0, 0x0, 0x0, 0x1C0000}};"
      code = 2
    else:
      hex_res = "  s21_decimal result = {{0x0, 0x0, 0x1, 0x1C0000}};"
      code = 0
  else:
    hex_res, code = decimal_to_equal_string(res, "result")

  print("  char *example = \"", num1, " ", func, " ", num2, " = ", res, "\";", sep="")
  print(hex1)
  print(hex2)
  print(hex_res)
  print("  int code = ", code, ";", sep="")

# Converting from py_decimal to structural view of hex massive.
def decimal_to_equal_string(decimal_value):
  exponent = 0
  is_negative = decimal_value < 0
  if is_negative:
    decimal_value = -decimal_value
  
  while not (decimal_value == decimal_value.to_integral_value()):
    decimal_value *= 10
    exponent += 1
    
  num_binary = bin(int(decimal_value))[2:]
  shift = random.randint(1,10)
  decimal_value2 = decimal_value * (10 ** shift)
  exponent2 = exponent + shift
  equal_binary = bin(int(decimal_value2))[2:]
    
  def chunk_bits(bit_string, chunk_size):
    return [bit_string[i:i + chunk_size] for i in range(0, len(bit_string), chunk_size)]

  def bits_to_hex(chunks):
    return [hex(int(chunk, 2))[2:].upper() for chunk in chunks]

  def hex_format(decimal_value, num_binary, exponent, val):
    while len(num_binary) > 96 or exponent > 28:
      decimal_value /= 10
      exponent -= 1
      num_binary = bin(int(decimal_value))[2:]
      if len(num_binary) <= 96 and exponent <= 28:
        decimal_value = decimal_value.quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)
        num_binary = bin(int(decimal_value))[2:]
        break

    padded_binary = num_binary.zfill(((len(num_binary) + 31) // 32) * 32)

    chunk_size = 32
    binary_chunks = chunk_bits(padded_binary, chunk_size)
    hex_chunks = bits_to_hex(binary_chunks)

    hex_chunks.reverse()

    while len(hex_chunks) < 3:
      hex_chunks.append("0")

    formatted_string = f"  s21_decimal {val} = " + "{{" + ", ".join(["0x" + chunk for chunk in hex_chunks])

    last_mantiss = hex((is_negative << 31) | (exponent << 16))[2:].upper()
    formatted_string += ", {}".format("0x" + last_mantiss) + "}};"

    return formatted_string
  
  first = hex_format(decimal_value, num_binary, exponent, "value_1")
  second = hex_format(decimal_value2, equal_binary, exponent2, "value_2")

  return first, second

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
    
  while len(num_binary) > 96 or exponent > 28:
    decimal_value /= 10
    exponent -= 1
    num_binary = bin(int(decimal_value))[2:]
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
      getcontext().prec = 60

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
