#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: No directory path provided."
    exit 1
fi

DIRECTORY=$1

if [ ! -d "$DIRECTORY" ]; then
    echo "Error: $DIRECTORY is not a directory."
    exit 1
fi

FILE_COUNT=$(find "$DIRECTORY" -maxdepth 1 -type f | wc -l)

# Output the result
echo "$FILE_COUNT"
