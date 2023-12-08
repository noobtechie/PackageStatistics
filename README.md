# PackageStatistics
A Python script to download and parse the Contents file from a Debian mirror, and output statistics of the top 10 packages with the most associated files.

# Thought Process
I tried to implement the following steps when trying to solve the problem
 - Understand the problem statement properly
 - Break down the problem into smaller chunks
   - Send an HTTP request to download the file
   - Decompress the gzip file
   - Parse the gzip file line by line
   - Extract filename and package name information from each line
   - Store package names into dictionary with the key being package name and value being the number of appearances.
   - Sort the dictionary and display the top 10 packages with respect to number of files.

## Problems 
There are some problems that I faced along the way:
 - Firstly the index files did not exactly follow the format mentioned in the documentation. The first row did not have the headings "FILE" and "LOCATION".
 - Whitespaces were not consistent across the file. So some cleanup needed to be done to the data.

## Tools
Here's the list of tools that I used to follow Python best practices
 - Static Analysis: Pylint
 - Editor: VSCode with Python Extension Pack
 - Unit Test Framework: Pytest
 - CI/CD: Github Actions
 - Environment: Python 3

# Time Spent
I spent around 2-3 hours solving this challenge. It took around a week to submit because I was also preparing for other interviews lined up during the week while also working on this challenge whenever time permited.

The most amount of time was spent in writing unit tests for the application.


