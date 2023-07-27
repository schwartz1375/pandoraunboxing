#!/usr/bin/env python3

__author__ = 'Matthew Schwartz (@schwartz1375)'

import gzip
import os
import shutil
import subprocess

import py7zr

# Location of the decompression script
DECOMPRESSION_SCRIPT = "./pandoraunboxing.py"

# Test file
test_file = "test_file.txt"
with open(test_file, "w") as f:
    f.write("This is a test file.")

# Compress the test file in different formats
shutil.make_archive("test", 'zip', '.', test_file)
shutil.make_archive("test", 'gztar', '.', test_file)
shutil.make_archive("test", 'tar', '.', test_file)

with py7zr.SevenZipFile("test.7z", mode="w") as z:
    z.write(test_file)

with gzip.open('test.gz', 'wb') as f:
    f.write(open(test_file, 'rb').read())

# Rar files can be a bit tricky as the rarfile module doesn't support compression, you can use the rar command if it's available
subprocess.call(['rar', 'a', 'test.rar', test_file])

# Create a simple Hello World program in C
with open("hello.c", "w") as f:
    f.write(
        '#include <stdio.h>\nint main() {printf("Hello, World!");return 0;}')

# Compile the C program to create an executable
os.system('gcc -o hello.exe hello.c')

# Pack the executable with UPX
os.system('upx -o hello_upx.exe hello.exe')

# Test the unpacking of the UPX packed executable
subprocess.run(["python3", DECOMPRESSION_SCRIPT, "hello_upx.exe"], check=True)

# Run the decompression script on the compressed files
subprocess.run(["python3", DECOMPRESSION_SCRIPT, "test.zip"], check=True)
subprocess.run(["python3", DECOMPRESSION_SCRIPT, "test.tar.gz"], check=True)
subprocess.run(["python3", DECOMPRESSION_SCRIPT, "test.tar"], check=True)
subprocess.run(["python3", DECOMPRESSION_SCRIPT, "test.7z"], check=True)
subprocess.run(["python3", DECOMPRESSION_SCRIPT, "test.gz"], check=True)
subprocess.run(["python3", DECOMPRESSION_SCRIPT, "test.rar"], check=True)

# Test the extraction of the MSI file
# Assuming you have test.msi file in the same directory
subprocess.run(["python3", DECOMPRESSION_SCRIPT,
               "putty-64bit-0.78-installer.msi"], check=True)

# Clean up the test files
files_to_remove = [
    "test",
    "hello_upx.exe",
    "test_file.txt",
    "test.zip",
    "test.tar.gz",
    "test.tar",
    "test.7z",
    "test.gz",
    "test.rar",
    "hello.c",
    "hello.exe",
    "unpacked_file",
    "extracted_files"
]

for filename in files_to_remove:
    if os.path.exists(filename):
        if os.path.isfile(filename):
            os.remove(filename)
        elif os.path.isdir(filename):
            shutil.rmtree(filename)
    else:
        print(f"The file or directory {filename} does not exist")
