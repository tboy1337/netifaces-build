# Netifaces Windows Wheels Builder - Project Summary

## Project Structure
- `.github/workflows/build_wheels.yml`: GitHub Actions workflow that builds Windows wheels for multiple Python versions
- `scripts/build_wheel.py`: Script to download and build netifaces wheels
- `scripts/get_netifaces_version.py`: Script to detect latest netifaces version from PyPI
- `scripts/README.md`: Documentation for the build scripts
- `README.md`: Project documentation
- `LICENSE.txt`: Project license

## Components Relationship
- GitHub Actions workflow invokes the Python scripts to:
  1. Detect latest netifaces version (or use specified version)
  2. Build wheels for each Python version in matrix
  3. Create GitHub release with built wheels

## Fixed Issues
- Fixed tar extraction in `build_wheel.py` to properly preserve source directory structure
- Added compatibility fix for Python 3.14's tar extraction deprecation warning

## Pending Tests
- Local verification of wheel building process
- Test with specific netifaces versions

## Critical Information
- The project is designed to automatically build wheels weekly
- Wheels are built for Python versions 3.7 through 3.13
- Manual builds can be triggered through GitHub Actions interface 