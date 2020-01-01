#!/usr/bin/env python3
"""Prints all the files which are having file size greater than the limit given."""
import os
import sys
import re
import argparse


# 1GB = 1e+9 bytes
def consumers(path, limit, o_file):
    try:
        filenames = os.listdir(path)
    except (PermissionError, OSError):
        return
    output_lines = []
    if len(filenames) != 0:
        for filename in filenames:
            match_dot_obj = re.compile(r'^[.]\w*')
            if match_dot_obj.search(filename) is None:
                file_path = os.path.join(path, filename)
                # Checks whether the path is directory or file
                if os.path.isdir(file_path):
                    consumers(file_path, limit, o_file)
                else:
                    try:
                        size_b = os.stat(file_path).st_size
                    except OSError:
                        return
                    if size_b > limit:
                        if o_file:
                            output_lines.append("Path: {}, size: {}Bytes".format(file_path, size_b/(1e+3)))
                        print("Path: {}, size: {}kB".format(file_path, size_b/(1e+3)))
    if o_file:
        with open(o_file, mode="at", encoding="utf-8") as f:
            for output_line in output_lines:
                f.write(output_line+"\n")
            f.close()
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Appends output to the file you specify")
    parser.add_argument("-s", "--size", help="The size of the files you want to search for ... UNITS: kB", type=int, default=1000000)
    parser.add_argument("-d", "--directory", help="In which directory you want to search for ...", default=".")
    args = parser.parse_args()
    consumers(os.path.abspath(args.directory), args.size*1000, args.output)
    if args.output:
        with open(args.output, mode="at", encoding="utf-8") as f:
            f.write("-------CHECKED {}-------".format(os.path.abspath(args.directory)))
            f.close()
    return


if __name__ == "__main__":
    main()
    print("-------CHECKED-------")
