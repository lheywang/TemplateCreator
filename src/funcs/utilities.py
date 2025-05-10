# -------------------------------------------------------------------------------
#   funcs/utilities.py :    Provide some abstractions functions to make the
#                           code cleaner.
#
#   l.heywang
#   10-05-2025
#
# -------------------------------------------------------------------------------

# Module import
import pathlib
import hashlib


def ConvertPathToRelatives(files: list, base: str):
    """
    ConvertPathToRelatives : Convert an array of full path files and reduce them to relatives path, from base.

        Arguments :
            files : List of pathlib.Path files.
            base : str that define the base path.

        Returns :
            files : List of pathlib.path but simplified.
            folders : Same as files, but the parents.
    """
    # Get base path
    folder = pathlib.Path(base)

    # Create storages
    output_files = []
    output_folders = []

    # Iterate over files and get the relatives.
    for file in files:

        # Compute relative path
        tmp = file.relative_to(pathlib.Path(folder))

        # Append relative file and folder
        output_files.append(tmp)
        output_folders.append(tmp.parent)

    return output_files, output_folders


def HashBytes(bytes):
    """
    HasBytes :  Return the hash of a bytes input.

        Arguments :
            bytes :     Raw data input

        Returns :
            hash :      Hash of the input
    """
    # Configure hasher
    hasher = hashlib.sha3_512()

    # Hash
    hasher.update(bytes)
    hash = hasher.digest()

    # Exit
    return hash
