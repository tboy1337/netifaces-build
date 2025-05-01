#!/usr/bin/env python3
"""
Script to get the latest version of netifaces from PyPI.
Can also be used to verify if a specific version exists.
"""

import argparse
import json
import sys
import os
import time
from urllib.error import URLError
import requests


def get_latest_version(retries=3, timeout=10):
    """
    Get the latest version of netifaces from PyPI.
    
    Args:
        retries: Number of retry attempts
        timeout: Request timeout in seconds
        
    Returns:
        Latest version string
    """
    url = "https://pypi.org/pypi/netifaces/json"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()
            return data["info"]["version"]
        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:  # Last attempt
                print(f"Error fetching version info: {e}", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...", file=sys.stderr)
                time.sleep(1)  # Wait before retrying
    
    # This line should not be reached due to the sys.exit in the exception handler
    sys.exit(1)


def version_exists(version, retries=3, timeout=10):
    """
    Check if a specific version of netifaces exists on PyPI.
    
    Args:
        version: Version string to check
        retries: Number of retry attempts
        timeout: Request timeout in seconds
        
    Returns:
        Boolean indicating if version exists
    """
    url = f"https://pypi.org/pypi/netifaces/{version}/json"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            if attempt == retries - 1:  # Last attempt
                return False
            else:
                time.sleep(1)  # Wait before retrying
    
    return False


def main():
    parser = argparse.ArgumentParser(description="Get netifaces version information.")
    parser.add_argument("--check", "-c", help="Check if specific version exists")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--retries", "-r", type=int, default=3, help="Number of retry attempts")
    parser.add_argument("--timeout", "-t", type=int, default=10, help="Request timeout in seconds")
    parser.add_argument("--output-file", "-o", help="Write output to file instead of stdout")
    args = parser.parse_args()

    result = None
    exit_code = 0

    try:
        if args.check:
            exists = version_exists(args.check, args.retries, args.timeout)
            if args.json:
                result = json.dumps({"version": args.check, "exists": exists})
            else:
                if exists:
                    result = f"Version {args.check} exists on PyPI"
                else:
                    result = f"Version {args.check} does not exist on PyPI"
                    exit_code = 1
        else:
            version = get_latest_version(args.retries, args.timeout)
            if args.json:
                result = json.dumps({"version": version})
            else:
                result = version
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

    # Output result
    if args.output_file:
        try:
            with open(args.output_file, 'w') as f:
                f.write(result)
        except Exception as e:
            print(f"Error writing to file {args.output_file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(result)

    sys.exit(exit_code)


if __name__ == "__main__":
    main() 