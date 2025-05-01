# Netifaces Build Scripts

This directory contains Python scripts used for the netifaces build process.

## get_netifaces_version.py

Script to get the latest version of netifaces from PyPI or check if a specific version exists.

### Usage:

```bash
# Get the latest version
python get_netifaces_version.py

# Check if a specific version exists
python get_netifaces_version.py --check 0.11.0

# Output as JSON
python get_netifaces_version.py --json

# Write output to a file
python get_netifaces_version.py --output-file version.txt

# Configure retry attempts and timeout
python get_netifaces_version.py --retries 5 --timeout 15
```

## build_wheel.py

Script to download and build a netifaces wheel for a specific version.

### Usage:

```bash
# Build a wheel for a specific version
python build_wheel.py --version 0.11.0

# Specify an output directory
python build_wheel.py --version 0.11.0 --output-dir ./wheels
```

## Notes

- These scripts handle cross-platform compatibility issues
- They include robust error handling and retry logic
- The scripts can be used independently outside of the GitHub Actions workflow 