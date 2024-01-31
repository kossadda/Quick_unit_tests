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
    echo -e "${YELLOW}"
    echo "    _              _                                             _               ";
    echo "   | |            | |                                           | |              ";
    echo "  _| |_  ___  ___ | |_      __ _   ___  _ __    ___  _ __  __ _ | |_  ___   _ __ ";
    echo " |_  __|/ _ \/ __|| __|    / _\` | / _ \| '_ \  / _ \| '__|/ _\` || __|/ _ \ | '__|";
    echo "   | |_|  __/\__ \| |_    | (_| ||  __/| | | ||  __/| |  | (_| || |_| (_) || |   ";
    echo "    \__|\___||___/ \__|    \__, | \___||_| |_| \___||_|   \__,_| \__|\___/ |_|   ";
    echo "                            __/ |                                                ";
    echo "                           |___/                                                 ";
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
    bold_print "Enter the project name:"
    read project_name
    delete_up
    echo -e "${BOLD}Project name: ${YELLOW}${project_name}${RESET}"
}

entering_testing_func()
{
    bold_print "Enter testing function:"
    read testing_func
    delete_up
    echo -e "${BOLD}Testing function: ${YELLOW}${testing_func}${RESET}"
}

dialog_entering_param()
{
    entering_project_name
    entering_testing_func
}