#!/bin/bash

readonly YELLOW='\033[1;33m'
readonly GREEN='\033[1;36m'
readonly RESET='\033[0m'
readonly BOLD='\033[1m'
readonly RED='\033[1;31m'
readonly DELETE='\033[K'
readonly UP='\033[A'

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
    bold_print "The script generates 100 test functions in the selected case."
    echo
}

bold_print()
{
    echo -e "${BOLD}${1}${RESET}"
}

delete_up()
{
    echo -e -n "\r${UP}${DELETE}"
    echo -e -n "\r${UP}${DELETE}"
}

entering_project_name()
{
    bold_print "Enter the project name (example: s21_math):"
    read project_name
    delete_up
    echo -e "${BOLD}Project name: ${YELLOW}${project_name}${RESET}"
}

entering_testing_func()
{
    bold_print "Enter testing function (example: log):"
    read testing_func
    delete_up
    echo -e "${BOLD}Testing function: ${YELLOW}${testing_func}${RESET}"
}

entering_argument()
{
    bold_print "Enter the argument of the testing function (example: \
log(1.1)):"
    read argument
    delete_up
    echo -e "${BOLD}Argument: ${YELLOW}${argument}${RESET}"
}

dialog_entering_param()
{
    entering_project_name
    entering_testing_func
}

comparison_function()
{
    bold_print "Enter the name of your own comparison function with\
the original function (example: s21_test_log)"
    read comparison_func
    delete_up
    echo -e "${BOLD}Comparison function: ${YELLOW}${comparison_func}${RESET}"
}

entering_test_number()
{
    bold_print "Enter the number of the first test (example 3)"
    read test_number
    delete_up
    echo -e "${BOLD}Argument: ${YELLOW}${test_number}${RESET}"
}

dialog()
{
    dialog_welcome
    dialog_brief
    dialog_entering_param
    entering_argument
    entering_test_number
    comparison_function
}