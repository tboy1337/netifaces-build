#!/usr/bin/env python3
"""
Script to download and build a netifaces wheel for a specific version.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import tarfile
import platform


def download_netifaces(version, output_dir):
    """Download the netifaces source code."""
    url = f"https://pypi.io/packages/source/n/netifaces/netifaces-{version}.tar.gz"
    tar_path = os.path.join(output_dir, "netifaces.tar.gz")
    
    print(f"Downloading netifaces {version}...")
    try:
        urllib.request.urlretrieve(url, tar_path)
        print(f"Downloaded to {tar_path}")
        return tar_path
    except Exception as e:
        print(f"Error downloading netifaces: {e}", file=sys.stderr)
        sys.exit(1)


def extract_tarball(tar_path, output_dir):
    """Extract the tarball."""
    print(f"Extracting {tar_path}...")
    extract_dir = os.path.join(output_dir, "source")
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
    
    try:
        # Use Python's tarfile instead of subprocess to ensure cross-platform compatibility
        with tarfile.open(tar_path, 'r:gz') as tar:
            # Get the top-level directory name from the archive
            top_dir = tar.getnames()[0].split('/')[0]
            
            # Extract all files using a filter to avoid deprecation warning in Python 3.14+
            if sys.version_info >= (3, 12):
                tar.extractall(path=output_dir, filter='data')
            else:
                tar.extractall(path=output_dir)
            
            # The source directory is the full path to the extracted top-level directory
            source_dir = os.path.join(output_dir, top_dir)
            
        print(f"Extracted to {source_dir}")
        return source_dir
    except Exception as e:
        print(f"Error extracting tarball: {e}", file=sys.stderr)
        sys.exit(1)


def build_wheel(source_dir, output_dir):
    """Build the wheel."""
    print("Building wheel...")
    original_dir = os.getcwd()
    os.chdir(source_dir)
    
    try:
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Install build dependencies
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "wheel", "build", "--upgrade"],
            check=True
        )
        
        # Build the wheel
        subprocess.run(
            [sys.executable, "-m", "build", "--wheel"],
            check=True
        )
        
        # Copy the wheel to the output directory
        dist_dir = os.path.join(source_dir, "dist")
        wheel_file = None
        if os.path.exists(dist_dir):
            for file in os.listdir(dist_dir):
                if file.endswith(".whl"):
                    src_path = os.path.join(dist_dir, file)
                    dst_path = os.path.join(output_dir, file)
                    shutil.copy(src_path, dst_path)
                    wheel_file = dst_path
                    print(f"Wheel built: {wheel_file}")
                    break
        
        if wheel_file:
            os.chdir(original_dir)
            return wheel_file
    except subprocess.CalledProcessError as e:
        os.chdir(original_dir)
        print(f"Error building wheel: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        os.chdir(original_dir)
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    
    os.chdir(original_dir)
    print("No wheel was produced", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Build a netifaces wheel.")
    parser.add_argument("--version", "-v", required=True, help="netifaces version to build")
    parser.add_argument("--output-dir", "-o", default=".", help="Output directory for wheel")
    args = parser.parse_args()
    
    # Convert relative path to absolute
    output_dir = os.path.abspath(args.output_dir)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        tar_path = download_netifaces(args.version, temp_dir)
        source_dir = extract_tarball(tar_path, temp_dir)
        wheel_path = build_wheel(source_dir, output_dir)
        
    print(f"Successfully built netifaces {args.version} wheel: {wheel_path}")


if __name__ == "__main__":
    main() 