"""
Test file for package_statistics.py
Tests for functions related to package statistics in a Debian mirror.
"""
import os
from unittest.mock import patch, MagicMock
import subprocess
import gzip
import shutil
import pytest
from package_statistics import (
    download_contents_file,
    extract_contents_file,
    parse_contents_file,
)

# Test download_contents_file function
@patch('package_statistics.requests.get')
def test_download_contents_file(mock_get):
    """
    Test case for download_contents_file function.
    Verifies if the function downloads the contents file correctly.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"Mock contents"
    mock_get.return_value = mock_response

    architecture = "amd64"
    destination_folder = "."
    filename = download_contents_file(architecture, destination_folder)

    assert filename == 'Contents-amd64.gz'
    assert os.path.exists(os.path.join(destination_folder, filename))

# Test extract_contents_file function
def test_extract_contents_file(tmpdir):
    """
    Test case for extract_contents_file function.
    Verifies if the function correctly extracts a compressed file.
    """
    # Create a temporary file
    tmp_file = tmpdir.join('test_file.txt')
    test_content = b'Mock compressed content'
    with open(tmp_file, 'wb') as f:
        f.write(test_content)

    # Compress the temporary file using gzip
    gzipped_file = str(tmp_file) + '.gz'
    with open(tmp_file, 'rb') as f_in, gzip.open(gzipped_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    extracted_file = extract_contents_file(gzipped_file)

    assert os.path.exists(extracted_file)
    with open(extracted_file, 'rb') as f:
        assert f.read() == test_content

# Test parse_contents_file function
def test_parse_contents_file(tmpdir):
    """
    Test case for parse_contents_file function.
    Verifies if the function parses the Contents file correctly.
    """
    # Create a temporary contents file
    contents_data = """\
    File1 package1,package2
    File2 package1
    File3 package2
    """
    tmp_file = tmpdir.join('test_contents_file')
    with open(tmp_file, 'w', encoding='utf-8') as f:
        f.write(contents_data)

    package_stats = parse_contents_file(str(tmp_file))

    # Check if the parsed package statistics match the expected result
    expected_package_stats = {
        'package1': 2,
        'package2': 2
    }
    assert package_stats == expected_package_stats

# Additional tests for main function can be added to check various scenarios
# ...
def test_main_function_with_input():
    """
    Test case for the main function with command line input.
    """

    # Run the main script with a specific architecture argument
    process = subprocess.Popen(['python3', 'package_statistics.py', 'amd64'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()

    # Capture the output and verify if it contains the expected headers and some content
    assert b'Package Name\t\tNumber of Files' in stdout

    # Check for exit status
    assert process.returncode == 0

def test_main_function_without_input():
    """
    Test case for the main function without command line input.
    """

    # Run the main script without any arguments
    process = subprocess.Popen(['python3', 'package_statistics.py'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Capture the error output and verify if it contains the expected error message
    assert b'Usage: ./package_statistics.py <architecture>' in stdout or stderr

    # Check for exit status indicating a failure due to missing arguments
    assert process.returncode != 0

# Run the tests with pytest
if __name__ == '__main__':
    pytest.main()
