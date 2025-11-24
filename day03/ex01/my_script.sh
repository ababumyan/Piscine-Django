#!/bin/bash

# Print which pip is being used
echo "PIP Version: $(pip --version)"

# Determine repository root relative to this script (two levels up)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR" && pwd)"

echo "Repository Directory: $REPO_DIR"
echo "Script Directory: $SCRIPT_DIR"

log_file="$REPO_DIR/instalation.log"
pathlib_git_url="https://github.com/jaraco/path"
local_lib="$REPO_DIR/local_lib"

echo "Logging installation details to $log_file"

# Remove any existing installation to ensure the install "crushes" previous copy
if [ -d "$local_lib" ]; then
    echo "Removing existing $local_lib" | tee -a "$log_file"
    rm -rf "$local_lib" >> "$log_file" 2>&1 || true
fi

echo "Starting Pathlib installation..." | tee -a "$log_file"

# Install the development version from GitHub into local_lib (force-reinstall)
# --upgrade and --force-reinstall help ensure files are replaced.
pip install --upgrade --force-reinstall --target "$local_lib" "git+$pathlib_git_url" >> "$log_file" 2>&1
install_exit=$?

if [ $install_exit -ne 0 ]; then
    echo "Path install failed. See $log_file for details." | tee -a "$log_file"
    exit $install_exit
fi

echo "Pathlib installation completed." | tee -a "$log_file"

# If installed successfully, run the Python program with local_lib on PYTHONPATH
echo "Running the small program using local_lib..." | tee -a "$log_file"
PYTHONPATH="$local_lib" python "$SCRIPT_DIR/my_program.py"

echo "Done." | tee -a "$log_file"