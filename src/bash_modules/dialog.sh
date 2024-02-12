readonly YELLOW='\033[1;33m'
readonly GREEN='\033[1;36m'
readonly RESET='\033[0m'
readonly BOLD='\033[1m'
readonly RED='\033[1;31m'
readonly DELETE='\033[K'
readonly UP='\033[A'

bold_print()
{
  echo -e "${BOLD}${1}${RESET}"
}

print_param()
{
  echo -e "${BOLD}${1}: ${YELLOW}${2}${RESET}"
}

dialog_welcome()
{
  clear
  echo -e "${YELLOW}"

  echo "                   _              _                     ";
  echo "                  | |            | |                    ";
  echo "                  | |_  ___  ___ | |_                   ";
  echo "                  | __|/ _ \/ __|| __|  _               ";
  echo "                  | |_|  __/\__ \| |_  | |              ";
  echo "   __ _   ___  _ __\__|\___||___/ \__| | |_  ___   _ __ ";
  echo "  / _\` | / _ \| '_ \  / _ \| '__|/ _\` || __|/ _ \ | '__|";
  echo " | (_| ||  __/| | | ||  __/| |  | (_| || |_| (_) || |   ";
  echo "  \__, | \___||_| |_| \___||_|   \__,_| \__|\___/ |_|   ";
  echo "   __/ |                                                ";
  echo "  |___/                                                 ";

  echo -e "${RESET}"
}

dialog_brief()
{
  bold_print "The script generates 100 test functions in the selected case"
  echo
}

dialog_project_name()
{
  print_param "Project name" ${PROJECT_NAME}
}

dialog_function_name()
{
  print_param "Function name" ${FUNCTION}
}

