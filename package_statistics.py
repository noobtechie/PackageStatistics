"""
package_statistics.py

A Python script to download and parse the Contents file from a Debian mirror,
and output statistics of the top 10 packages with the most associated files.
"""
import os
import sys
import gzip
import shutil
from urllib.parse import urlparse
from collections import defaultdict
import requests

def download_contents_file(architecture, destination_folder='.', timeout=10):
    """
    Download the compressed Contents file from the Debian mirror.

    Args:
        architecture (str): The architecture (e.g., amd64, arm64).
        destination_folder (str): The folder to save the downloaded file.
        timeout (int): The timeout value for the HTTP request in seconds.
        
    Returns:
        str: The filename of the downloaded Contents file.
    """
    base_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"
    contents_file_url = f"{base_url}Contents-{architecture}.gz"
    try:
        response = requests.get(contents_file_url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading Contents file: {e}")
        sys.exit(1)

    if response.status_code == 200:
        filename = os.path.basename(urlparse(contents_file_url).path)
        destination_path = os.path.join(destination_folder, filename)
        with open(destination_path, 'wb') as file:
            file.write(response.content)
        return filename
    else:
        print(f"Error downloading Contents file. Status code: {response.status_code}")
        sys.exit(1)

def extract_contents_file(filename):
    """
    Extract the Contents file from the compressed file.

    Args:
        filename (str): The filename of the compressed Contents file.

    Returns:
        str: The filename of the extracted Contents file.
    """
    # Construct the output file path by removing the '.gz' extension
    output_file_path = filename[:-3]

    with gzip.open(filename, 'rb') as f_in, open(output_file_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    return output_file_path

def parse_contents_file(contents_file):
    """
    Parse the Contents file and return a dictionary with package names and file counts.

    Args:
        contents_file (str): The filename of the Contents file.

    Returns:
        defaultdict: A dictionary containing package names as keys and file counts as values.
    """
    package_stats = defaultdict(int)

    with open(contents_file, 'r', encoding='utf-8') as file:
        for line in file:
            # Extract qualified package names from the line
            qualified_package_names = line.split(' ', 1)[1].split(',')

            # Iterate through qualified package names and update the stats
            for qualified_package in qualified_package_names:
                package_name = qualified_package.strip()
                package_stats[package_name] += 1

    return package_stats

def main():
    """
    Main function to execute the package statistics script.
    """
    if len(sys.argv) != 2:
        print("Usage: ./package_statistics.py <architecture>")
        sys.exit(1)

    architecture = sys.argv[1]
    contents_data = download_contents_file(architecture)
    contents_file = extract_contents_file(contents_data)
    package_stats = parse_contents_file(contents_file)

    # Sort the packages based on the number of files
    sorted_packages = sorted(package_stats.items(), key=lambda x: x[1], reverse=True)

    # Output the top 10 packages
    print("Package Name\t\tNumber of Files")
    for package, file_count in sorted_packages[:10]:
        print(f"{package}\t\t{file_count}")

if __name__ == "__main__":
    main()
