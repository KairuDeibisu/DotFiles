
from genericpath import exists
import shutil
import json
import os
import sys
import argparse
import pathlib

DOTFILE_DIR_PATH = pathlib.Path("/home/kyled/DotFiles/")

class PathExist(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):

        if not os.path.exists(values):
            raise argparse.ArgumentTypeError(f"PathExist: {values} is not a valid path")
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(f"PathExist: {values} is not readable")


def main(args):

    parser = argparse.ArgumentParser("Manage Dotfiles")

    parser.add_argument('path', type=pathlib.Path, action=PathExist)
    args = parser.parse_args()

    path : pathlib.Path = args.path

    try:

        copied_path = pathlib.Path(shutil.copy2(path.absolute(), DOTFILE_DIR_PATH, follow_symlinks=True))
        symlink_path = path
        
        path_bak = path.rename(path.resolve().as_posix() + ".bak")
        symlink_path.symlink_to(copied_path)
    
    except shutil.SameFileError as err:
        print(err, end="\n\n")
        print("You already did this!") 

if __name__ == "__main__":
    
    
    main(sys.argv)
