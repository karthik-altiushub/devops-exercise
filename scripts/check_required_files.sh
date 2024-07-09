#!/bin/bash

# List of required files
REQUIRED_FILES=("README.md" "LICENSE" ".gitignore")

# Loop through the required files and check if they exist
for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "Error: $file is missing."
        exit 1
    fi
done

echo "All required files are present."
exit 0
