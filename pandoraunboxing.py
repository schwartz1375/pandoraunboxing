#!/usr/bin/env python3

__author__ = 'Matthew Schwartz (@schwartz1375)'

import argparse
import gzip
import os
import shutil
import subprocess
import tarfile
import zipfile

import magic
import py7zr
from rarfile import RarFile


def is_packed_with_upx(filepath):
    try:
        process = subprocess.run(
            ['upx', '-t', filepath], capture_output=True, text=True)
        if 'NotPackedException' in process.stderr:
            return False
        else:
            return True
    except FileNotFoundError:
        print("The 'upx' tool is not installed or not found in the system's PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")


def unpack_upx(filepath, output_dir):
    print("The file is a Windows executable (PE file) packed with UPX. Unpacking now...")
    output_filepath = os.path.join(output_dir, 'unpacked_file')
    try:
        process = subprocess.run(
            ['upx', '-d', '-o', output_filepath, filepath], capture_output=True, text=True)
        if process.stderr:
            print("An error occurred while trying to unpack the file: ",
                  process.stderr)
    except FileNotFoundError:
        print("The 'upx' tool is not installed or not found in the system's PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")


def is_msi_file(filepath):
    return magic.from_file(filepath, mime=True) == 'application/x-msi'


def extract_msi(filepath, output_dir):
    print("The file is a Windows Installer Package (MSI file). Extracting now...")
    output_filepath = os.path.join(output_dir, 'extracted_files')
    command = f"msiextract -C {output_filepath} {filepath}"
    try:
        process = subprocess.run(
            command, capture_output=True, shell=True, text=True)
        if process.stderr:
            print(
                "An error occurred while trying to extract the MSI file:", process.stderr)
        else:
            print("MSI file has been extracted.")
    except Exception as e:
        print(f"An error occurred while trying to extract the MSI file: {e}")


def decompress_file(filepath, output_dir):
    file_type = magic.from_file(filepath, mime=True)
    print(f"MIME type: {file_type}")

    try:
        if file_type == 'application/x-7z-compressed':
            with py7zr.SevenZipFile(filepath, mode='r') as z:
                z.extractall(output_dir)
            print("7zip file has been decompressed.")
            return

        elif file_type == 'application/zip':
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            print("Zip file has been decompressed.")
            return

        elif file_type == 'application/x-tar':
            with tarfile.TarFile(filepath, 'r') as tar_ref:
                tar_ref.extractall(output_dir)
            print("Tar file has been decompressed.")
            return

        elif file_type == 'application/gzip':
            with gzip.open(filepath, 'rb') as f_in:
                with open(os.path.join(output_dir, os.path.basename(filepath[:-3])), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print("Gzip file has been decompressed.")
            return

        elif file_type == 'application/vnd.rar' or file_type == 'application/x-rar':
            with RarFile(filepath) as rf:
                rf.extractall(output_dir)
            print("Rar file has been decompressed.")
            return

        elif is_msi_file(filepath):
            extract_msi(filepath, output_dir)
            return

        else:
            print(
                "File type not recognized or not supported. Trying UPX unpacking as a fallback...")
            if is_packed_with_upx(filepath):
                unpack_upx(filepath, output_dir)
            else:
                print("Fallback also failed. Unable to decompress the file.")

    except Exception as e:
        print(f"An error occurred while trying to decompress the file: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decompress a file.')
    parser.add_argument('filepath', type=str,
                        help='Path to the file to decompress')
    parser.add_argument('-o', '--output', type=str,
                        default='', help='Output directory')

    args = parser.parse_args()

    output_dir = args.output if args.output else os.path.dirname(
        os.path.realpath(args.filepath))
    decompress_file(args.filepath, output_dir)
