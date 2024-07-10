#!/bin/bash

# Check Python files using flake8
echo "Checking Python files with flake8..."
flake8 .

# Check TypeScript files using eslint
echo "Checking TypeScript files with eslint..."
npx eslint .


# Capture exit status of flake8 and eslint
FLAKE8_STATUS=$?
ESLINT_STATUS=$?

if [ $FLAKE8_STATUS -ne 0 ] || [ $ESLINT_STATUS -ne 0 ]; then
    echo "Style check failed."
    exit 1
else
    echo "Style check passed."
    exit 0
fi
