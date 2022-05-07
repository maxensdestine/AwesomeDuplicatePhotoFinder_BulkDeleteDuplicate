from typing import List
import os
import argparse
import platform
from pathlib import PureWindowsPath
import traceback

""" This script is made in a way that it will not break if eventually a single group can contain more than 2 files"""

curindex: int = 0



def win_to_unix_path(winpath: str) -> str:
    return str(PureWindowsPath(winpath).as_posix())


def win_to_wsl2_path(winpath: str) -> str:
    d,p = winpath.split(':')
    return '/mnt/'+d.lower()+p.replace('\\','/')   



def get_all_members(lines: List[str], groupindex: int) -> List[str]:
    "returns the largest file of a group, a list containing the path to each group member and the similarity of the group"
    global curindex
    all_members = []
    biggest_size: int = 0
    biggest_path = ""
    percent = 0
    while curindex < len(lines):
        columns = lines[curindex].split(";")
        if not int(columns[0]) == groupindex:
            break

        path = columns[1]
        # transform into unix or wsl path
        if "Windows" not in platform.system(): 
            if "WSL" in platform.uname().release:
                path = win_to_wsl2_path(path)
            else:
                path = win_to_unix_path(path)
        
        all_members.append(path)
        size = get_size(path)

        # just change the sign if you want the smallest image instead. You would also have to initialize size at a random large value rather than 0 and change the default return of the get_size function
        if size > biggest_size:
            biggest_path = path
            biggest_size = size
        percent = int(columns[2])
        curindex += 1
    
    return biggest_path, all_members, percent


def get_size(path: str) -> int:
    try:
        file_stats = os.stat(path)
        return file_stats.st_size
    except Exception:
        return 0



def delete_similar(lines: List[str], similarity: int):
    "Deletes the smallest member of groups which have a similarity at least as large as the given parameter. The lines argument should contains the lines of the 'Awesome duplicate photo finder' output text file except the first line."
    max = int(lines[-1].split(";")[0])
    for i in range(0, max):
        try:
            biggest, all_members, percent = get_all_members(lines, (i + 1))
            if percent >= similarity:
                for member in all_members:
                    if member != biggest:
                        try:
                            os.remove(member)
                        except Exception:
                            print("Could not delete " + member + ". It was most likely already deleted")
        except Exception as e:
            print("Unexpected error")
            print(traceback.format_exc())

        print(str(i+1)+"/" + str(max), end = "\r")
    
    print(str(max)+"/" + str(max))



def integer_format_validator(temp: str) -> int:
    msg = "Must an integer be greater than 0"
    try:
        someVal = int(temp)
        if not someVal > 0:
            raise argparse.ArgumentTypeError(msg)
        else:
            return someVal
    except:
        raise argparse.ArgumentTypeError(msg)


def file_format_validator(temp: str) -> str:
    if os.path.isfile(temp):
        return temp
    else:
        raise argparse.ArgumentTypeError("Not a file. Try using an absolute path if the file actually exists.")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Python CLI app to bulk delete duplicate images found with Awesome Duplicate Photo Finder")

    parser.add_argument("-sim", "--similarity", type=integer_format_validator, default="50", help="Integer representing the minimum similarity percentage to delete a picture. Must be greater than 0. Default value: 80")

    parser.add_argument("file", type=file_format_validator, help="Path to the file which contains the Awesome duplicate photo finder output (semi colon separated values)")

    args = parser.parse_args()

    return args.file, args.similarity



def main():
    file, percent = parse_arguments()
    with open(file, "r") as f:
        lines = f.readlines()[1:]

    delete_similar(lines, percent)


if __name__ == "__main__":
    main()