import sys
from decimal import Decimal, getcontext, ROUND_DOWN

getcontext().prec = 60

def binary_operations(func):
  num1 = Decimal(sys.argv[1])
  num2 = Decimal(sys.argv[3])
  res = 0
  arithmetic = 0

  if func == "+":
    res = num1 + num2
    arithmetic = 1
  elif func == "-":
    res = num1 - num2
    arithmetic = 1
  elif func == "*":
    res = num1 * num2
    arithmetic = 1
  elif func == "/":
    res = num1 / num2
    arithmetic = 1
  elif func == "%":
    res = num1 % num2
    arithmetic = 1

  if arithmetic:
    calculate(num1, num2, res, func)
  else: 
    compare(num1, num2, func)

def compare(num1, num2, func):
  hex1 = decimal_to_hex_string(num1, "value_1")
  hex2 = decimal_to_hex_string(num2, "value_2")

  code = 0

  num1 = num1.quantize(Decimal('1e-28'), rounding=ROUND_DOWN)
  num2 = num2.quantize(Decimal('1e-28'), rounding=ROUND_DOWN)

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

  print("//", num1, func, num2, "=", code)
  code *= 1
  print(hex1)
  print(hex2)
  print("  int error_code = ", code, ";", sep="")

def calculate(num1, num2, res, func):
  hex1 = decimal_to_hex_string(num1, "value_1")
  hex2 = decimal_to_hex_string(num2, "value_2")
  hex_res, code = decimal_to_hex_string(res, "result")

  print("//", num1, func, num2, "=", res)
  print(hex1)
  print(hex2)
  print(hex_res)
  print("  int error_code = ", code, ";", sep="")

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
    
  while len(num_binary) > 96:
    decimal_value /= 10
    exponent -= 1
    num_binary = bin(int(decimal_value))[2:]

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

func = sys.argv[2]
binary_operations(func)
