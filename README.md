# PANDORAUNBOXING

This Python script automatically decompresses files in various formats, including 7z, zip, tar, gzip, rar, and MSI (Windows Installer Packages). It also detects and unpacks Windows executable files (PE files) that have been packed using the UPX packer. The script takes as input the path of the file to be decompressed and an optional output directory, defaulting to the directory of the input file if none is specified.

## Why not use 'pyunpack'?
This is primarily for two reasons:
* Control: Using specific libraries for each file type provides more control over the decompression process. These libraries often offer more configuration options and specific error handling than a general-purpose tool like pyunpack.
* Efficiency: When you use a specific library, you're only loading the code necessary to handle that specific file type, which could potentially make the script run more efficiently.

## UPX Unpacking and Fallback Mechanism
In addition to handling common compressed file formats, the PandoraUnboxing script also identifies files that have been packed using the UPX packer. Notably, this is not just limited to Windows executable files (PE files) but extends to other files that may have been packed using UPX. If the script encounters a file with a type that isn't recognized or isn't directly supported, it uses UPX unpacking as a fallback mechanism in an attempt to decompress the file. This increases the range of files that the script can successfully decompress.

## Package Installation
The `PandoraUnboxing` script requires specific Python packages to run. You can install these required packages using `pip`, the Python package installer.

First, ensure you have `pip` installed on your system. If it's not installed, you can download and install it from the [official website](https://pip.pypa.io/en/stable/installation/).

Once `pip` is installed, you can install all required packages using the `requirements.txt` file included in the repository. This file lists all the Python packages that `PandoraUnboxing` depends on.

Open a terminal (command prompt), navigate to the directory containing `requirements.txt`, and run the following command:
```
pip install -r requirements.txt
```

## Prerequisites
PandoraUnboxing requires Python 3.x (where 'x' is a version number). Ensure that you have the appropriate version of Python installed on your system. You can check your Python version by running `python --version` in your terminal.

## Usage
To use the script, run the following command:
``` 
python3 pandoraunboxing.py [filepath] -o [output_directory]
```

## Running the Tests
This repository includes a test script, `pandoraunboxing_test.py`, which verifies the functionality of `PandoraUnboxing`. 

Please note that the test script assumes that certain tools are already installed on your system and available in your system's path. Specifically, the `rar` command is used to create a RAR file for testing, the `upx` tool is used to create a UPX-packed Windows executable, and the `msitools` package is used for handling MSI files. If these tools are not installed or not in the system's path, some tests may fail.

The test script generates a test file and compresses it in several different formats (7z, zip, tar, gzip, rar, UPX-packed EXE, and MSI), then runs the `PandoraUnboxing` script on each of the compressed files.

For testing the extraction of MSI files, the script uses an MSI installer for [PuTTY](https://putty.org/), a free and open-source terminal emulator. This installer file, `putty-64bit-0.78-installer.msi`, must be present in the same directory as the test script for the test to run successfully. The PuTTY MSI installer can be downloaded from the official [PuTTY](https://putty.org/) website.

Please note that this MSI file is used purely for testing purposes and is not integral to the functionality of the PandoraUnboxing script itself.

To run the test script, use the following command:
```
python3 pandoraunboxing_test.py
```