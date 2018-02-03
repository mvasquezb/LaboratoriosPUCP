#!/usr/bin/env bash

RCol='\e[0m'    # Text Reset

# Regular           Bold                Underline           High Intensity      BoldHigh Intens     Background          High Intensity Backgrounds
Bla='\e[0;30m';     BBla='\e[1;30m';    UBla='\e[4;30m';    IBla='\e[0;90m';    BIBla='\e[1;90m';   On_Bla='\e[40m';    On_IBla='\e[0;100m';
Red='\e[0;31m';     BRed='\e[1;31m';    URed='\e[4;31m';    IRed='\e[0;91m';    BIRed='\e[1;91m';   On_Red='\e[41m';    On_IRed='\e[0;101m';
Gre='\e[0;32m';     BGre='\e[1;32m';    UGre='\e[4;32m';    IGre='\e[0;92m';    BIGre='\e[1;92m';   On_Gre='\e[42m';    On_IGre='\e[0;102m';
Yel='\e[0;33m';     BYel='\e[1;33m';    UYel='\e[4;33m';    IYel='\e[0;93m';    BIYel='\e[1;93m';   On_Yel='\e[43m';    On_IYel='\e[0;103m';
Blu='\e[0;34m';     BBlu='\e[1;34m';    UBlu='\e[4;34m';    IBlu='\e[0;94m';    BIBlu='\e[1;94m';   On_Blu='\e[44m';    On_IBlu='\e[0;104m';
Pur='\e[0;35m';     BPur='\e[1;35m';    UPur='\e[4;35m';    IPur='\e[0;95m';    BIPur='\e[1;95m';   On_Pur='\e[45m';    On_IPur='\e[0;105m';
Cya='\e[0;36m';     BCya='\e[1;36m';    UCya='\e[4;36m';    ICya='\e[0;96m';    BICya='\e[1;96m';   On_Cya='\e[46m';    On_ICya='\e[0;106m';
Whi='\e[0;37m';     BWhi='\e[1;37m';    UWhi='\e[4;37m';    IWhi='\e[0;97m';    BIWhi='\e[1;97m';   On_Whi='\e[47m';    On_IWhi='\e[0;107m';

function error_handler() {
    msg=${1:-"An error has ocurred"}
    echo -e >&2 "${BRed}${msg}${RCol}"
    exit 1
}

# Check if pip3 exists
command -v pip3 >/dev/null 2>&1 || error_handler "This is a Python3 application, pip3 is required."

# Install pip requirements
[ -f "requirements.txt" ] || error_handler "Missing requirements.txt file for pip dependencies"
echo "Installing pip requirements"
pip3 install -r requirements.txt >/dev/null 2>&1 && echo "Done." || error_handler "Error install pip packages"

cd laboratorios

# Check if 'env.py' is present (required for gmail integration)
env_filename="env.py"
[ -f $env_filename ] || error_handler "Required environment config file ($env_filename) does not exist"

# Django app setup
echo "Migrating database structure"
./manage.py migrate && echo "Done." || error_handler

echo "Loading required initial data"
./manage.py loaddata initial.json && echo "Done." || error_handler

echo "Creating superuser with username 'admin'. This requires your input"
./manage.py createsuperuser --username admin && echo "Done." || error_handler

# Create additional resource permissions
./create_permissions.py

# Create superuser role
./create_superuser_role.py

# Create Employee object for superuser
./create_admin_employee.py

echo "App is ready for use"
