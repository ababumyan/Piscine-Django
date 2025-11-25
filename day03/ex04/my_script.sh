#!/bin/bash

echo "PIP Version: $(pip3 --version)"

log_file="setup.log"
python3 -m venv django_venv > $log_file 2>&1
source django_venv/bin/activate
echo "Virtual environment 'django_venv' activated."
pip install -r requirement.txt >> $log_file 2>&1

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Check $log_file for details."
    exit 1
fi
echo "Dependencies installed successfully."
sleep 1