#!/bin/bash

# Get the latest tag (assuming it's the last release)
LATEST_TAG=$(git describe --tags `git rev-list --tags --max-count=1`)

# If there's no tag, consider all commits
if [ -z "$LATEST_TAG" ]; then
  COMMITS=$(git log --pretty=format:"%s")
else
  COMMITS=$(git log $LATEST_TAG..HEAD --pretty=format:"%s")
fi

# Initialize changelog categories
FEATURES=""
BUG_FIXES=""
OTHER_CHANGES=""

# Categorize commits
while IFS= read -r COMMIT; do
  COMMIT_LOWER=$(echo "$COMMIT" | tr '[:upper:]' '[:lower:]')
  if [[ $COMMIT_LOWER == *"feature"* ]]; then
    FEATURES+="- ${COMMIT}\n"
  elif [[ $COMMIT_LOWER == *"bug"* ]]; then
    BUG_FIXES+="- ${COMMIT}\n"
  else
    OTHER_CHANGES+="- ${COMMIT}\n"
  fi
done <<< "$COMMITS"


# Generate changelog
CHANGELOG="### Changelog\n\n"

if [ ! -z "$FEATURES" ]; then
  CHANGELOG+="#### Features:\n${FEATURES}\n"
fi

if [ ! -z "$BUG_FIXES" ]; then
  CHANGELOG+="#### Bug Fixes:\n${BUG_FIXES}\n"
fi

if [ ! -z "$OTHER_CHANGES" ]; then
  CHANGELOG+="#### Other Changes:\n${OTHER_CHANGES}\n"
fi

# Output changelog to a file
echo -e "$CHANGELOG" > CHANGELOG.md

# Print the changelog
cat CHANGELOG.md
