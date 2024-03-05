#!/bin/bash

generate_num()
{
  local value=""
  local type=$1
  local dot=0

  if ((type == 2)); then
    value=$(perl -e 'print int(rand(2147483647*2+1))-2147483648, "\n"')
  else
    if (((RANDOM % 3) == 0)); then
      value="-"
    fi

    if ((type == 1 && (RANDOM % 15) == 0)); then
      if (((RANDOM % 3) == 0)); then
        value="${value}0.000000000"
      else
        value="${value}0."
      fi
      dot=1
    fi

    value=$(randomize ${value} ${type} ${dot})
    value=$(check_for_mistakes ${value})
  fi

  echo -n "${value}"
}

randomize()
{
  local value=$1
  local type=$2
  local dot=$3

  for ((i = 0; i < 28; i++)); do
    value="${value}$((RANDOM % 10))"

    if ((dot == 0 && type == 1 && (RANDOM % 3) == 0)); then
      value="${value}."
      dot=1
    fi

    if (((RANDOM % 20) == 0)); then
      break
    fi
  done

  echo ${value}
}

check_for_mistakes()
{
  local value=$1

  value=${value%.}
  if [[ $value =~ ^-?0+\. ]]; then
    value=$(echo $value | sed -e 's/^-\?0*\./0./')
  elif [[ $value =~ ^-?0+[^.] ]]; then
    value=$(echo $value | sed -e 's/^-\?0*//')
    if [[ -z $value || $value == "-" ]]; then
      value="0"
    fi
  fi

  while (( ${#value} > 28 )); do
    value="${value%?}"
  done

  if (((RANDOM % 100) == 0)); then
    if (((RANDOM % 2) == 0)); then
      value="0"
    else
      if (((RANDOM % 2) == 0)); then
        value="79228162514264337593543950335"
      else
        value="-79228162514264337593543950335"
      fi
    fi
  fi

  echo ${value}
}

generate_float_decimal()
{
  VALUE_1=$(generate_num 1)
  echo ${VALUE_1}
}

generate_int()
{
  VALUE_1=$(generate_num 2)
  echo ${VALUE_1}
}
