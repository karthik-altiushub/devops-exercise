#!/bin/bash

echo "Running at.... $(date)"
echo "Checking for required files..."

REQUIRED_FILES=("README.md" "LICENSE" ".gitignore")

for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "Error: $file is missing."
        exit 1
    fi
done

echo "All required files are present."
exit 0
