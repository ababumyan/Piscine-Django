#!/bin/bash

echo "PIP Version: $(pip3 --version)"

current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd "$current_dir" && pwd)"

echo "Repository Directory: $repo_dir"
echo "Script Directory: $current_dir"

log_file="$repo_dir/instalation.log"
pathlib_git_url="https://github.com/jaraco/path"
local_lib="$repo_dir/local_lib"

echo "Logging installation details to $log_file"

if [ -d "$local_lib" ]; then
    echo "Removing existing $local_lib" | tee -a "$log_file"
    rm -rf "$local_lib" >> "$log_file" 2>&1 || true
fi

echo "Starting Pathlib installation..." | tee -a "$log_file"

pip3 install --upgrade --force-reinstall --target "$local_lib" "git+$pathlib_git_url" > "$log_file" 2>&1
install_exit=$?

if [ $install_exit -ne 0 ]; then
    echo "Path install failed. See $log_file for details." | tee -a "$log_file"
    exit $install_exit
fi

echo "Pathlib installation completed." | tee -a "$log_file"

echo "Done." | tee -a "$log_file"