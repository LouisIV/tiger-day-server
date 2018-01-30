"""
    createFileOnDrive.py
    Louis Lombardo IV
    LouisLombardoIV@gmail.com
    DEC 2017
"""
import better_exceptions
from GoogleDrive import GoogleDriveManager
import sys

if __name__ == '__main__':
    print("This application is used to create a file on the Google Drive. 'q'"
          + "to exit.\n")
    title = input("Enter a title: ")
    if title != "q":
        data_file = GoogleDriveManager().search_first(title)
        print("Go online and check if it worked!")
    sys.exit()
