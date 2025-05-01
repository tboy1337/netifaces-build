# Netifaces Windows Wheels Builder

This repository automatically builds Windows wheels for the [netifaces](https://pypi.org/project/netifaces/) Python package. The wheels are built using GitHub Actions and are made available as GitHub Releases.

## Features

- Automatically builds wheels for Python 3.7 through 3.13
- Weekly builds to ensure the latest version is always available
- Manual trigger option to build specific versions
- Detects the latest version from PyPI
- Modular design with separate Python scripts for maintainability

## How It Works

The GitHub Actions workflow:

1. Runs on a schedule (weekly), on push to main, or can be manually triggered
2. Uses `scripts/get_netifaces_version.py` to fetch the latest netifaces version from PyPI (or uses the specified version for manual builds)
3. Uses `scripts/build_wheel.py` to build wheels for all supported Python versions on Windows
4. Creates a GitHub Release with all wheels

## Using the Wheels

You can download the pre-built wheels from the [Releases](../../releases) page and install them using pip:

```bash
pip install netifaces-0.11.0-cp310-cp310-win_amd64.whl
```

Alternatively, you can use pip to install directly from the GitHub release URL.

## Automatic Updates

This project automatically detects and builds the latest version of netifaces each week, so you don't need to update it manually.

## Manual Build

You can manually trigger a build for a specific netifaces version through the GitHub Actions workflow interface:

1. Go to the Actions tab
2. Select the "Build Netifaces Windows Wheels" workflow
3. Click "Run workflow"
4. Enter the desired netifaces version (e.g., "0.11.0")
5. Click "Run workflow"

## Scripts

This project includes two Python scripts to handle the build process:

- `scripts/get_netifaces_version.py` - Fetches the latest netifaces version from PyPI or verifies if a specific version exists
- `scripts/build_wheel.py` - Downloads and builds a netifaces wheel for a specific version

### Using the Scripts Locally

You can also use these scripts locally to build wheels:

```bash
# Get the latest netifaces version
python scripts/get_netifaces_version.py

# Check if a specific version exists
python scripts/get_netifaces_version.py --check 0.11.0

# Build a wheel for a specific version
python scripts/build_wheel.py --version 0.11.0 --output-dir wheels
```

## License

See the [LICENSE.txt](LICENSE.txt) file for license information.

## Technical Details

The workflow is defined in [.github/workflows/build_wheels.yml](.github/workflows/build_wheels.yml) and includes:

- Matrix build for multiple Python versions
- PyPI API integration to detect the latest version
- Automated GitHub release creation
- Modular Python scripts for better maintainability and testing 