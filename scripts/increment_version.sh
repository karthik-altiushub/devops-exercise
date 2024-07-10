#!/bin/bash
set -e

# Read current version
version=$(cat version.txt)
echo "Current version: $version"

# Split version into components
IFS='.' read -ra VERSION_PARTS <<< "$version"
major=${VERSION_PARTS[0]}
minor=${VERSION_PARTS[1]}
patch=${VERSION_PARTS[2]}

# Increment patch version
new_patch=$((patch + 1))

# Construct new version
new_version="$major.$minor.$new_patch"
echo "New version: $new_version"

# Update version.txt
echo $new_version > version.txt

# Set output for use in GitHub Actions
echo "new_version=$new_version" >> $GITHUB_OUTPUT