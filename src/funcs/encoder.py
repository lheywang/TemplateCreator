# -------------------------------------------------------------------------------
#   Encoder.py : Encode a folder and it's structure into a blob file
#
#   l.heywang
#   08-05-2025
#
# -------------------------------------------------------------------------------

# Modules import
import pickle  # base python
import pathlib  # Python 3.4
import datetime  # base python
import platform  # base python
import struct  # base python
import zlib  # base python

# Others functions imports
from .messages import printEnd, printMetadata
from .utilities import ConvertPathToRelatives, HashBytes  # Require python 3.6

# Minimal comp : Python 3.6


# Functions
def Encoder(
    folder: str, file: str, token: str, verbose: int, reserved_var: str, output: str
):
    """
    Encoder function : Encode a folder into a template file

        Arguments :
            folder (str):       The path of the folder to encoded.
            file (str) :        The path of a file inside the folder where the name can be customized.
            token (str) :       The searched token to identify variables.
            verbose (int) :     The verbose level. 0 = No verbose. 1 = Step verbose. 2 = Full verbose.
            reserved_var(str):  The variable used that will be used as file name, or any other usage.
            output (str) :      The path of the folder where the data.template file is wrote.

        Returns (int) :
            - -1 :              The file is not in the passed folder.
    """
    # Open the folder
    base_path = pathlib.Path(folder).glob("**/*")
    files = [x for x in base_path if x.is_file()]

    # Check for the file in the files list
    base_file = pathlib.Path(file)
    if base_file not in files:
        return -1

    # detect files and variables to be modified
    files_to_edit = []
    binary_files = []
    variables = []

    # Iterate over file, try to read them and search for replacement tokens
    for index, file in enumerate(files):
        try:
            # Try to open and reas the file.
            with open(file, "r") as f:
                lines = f.readlines()

                # Iterate over the lines to mark any variables
                for line in lines:

                    if token in line:

                        files_to_edit.append(file)
                        tmp_s = line.split(token)

                        # Handle single variable per lines
                        if len(tmp_s) == 3:
                            variables.append(tmp_s[1])

                        # Handle multiple variables per lines
                        else:
                            # Copy variable name
                            variables.append(tmp_s[1])

                            # Delete three first strings (already treated)
                            del tmp_s[0]
                            del tmp_s[0]
                            del tmp_s[0]

                            # The next one will be a variable name
                            for index, text in enumerate(tmp_s):
                                # Ignore one over two iterations
                                if index % 2 == 1:
                                    continue

                                variables.append(tmp_s[index])

        # Handle files that aren't text (images...) and flag them as binary
        except UnicodeDecodeError:
            binary_files.append(file)
            continue

        if verbose > 1:
            print(f"Rode       [{(index + 1):3} / {len(files):3}] : {file}")

    # Remove variables that are tied to the project name (this variable will be
    # asked globally, and shall not be in the variable list)
    for index, var in enumerate(variables):
        if var == reserved_var:
            del variables[index]

    # Simplify files path
    rel_files, folders = ConvertPathToRelatives(files, folder)
    edit, _ = ConvertPathToRelatives(files_to_edit, folder)
    ref_file, _ = ConvertPathToRelatives([base_file], folder)

    # Remove duplicates (otherwise they may be asked twice)
    variables = list(dict.fromkeys(variables))
    folders = list(dict.fromkeys(folders))
    files_to_edit = list(dict.fromkeys(edit))

    # Remove '.' path
    if pathlib.Path(".") in folders:
        folders.remove(pathlib.Path("."))

    # Then, creating a big dict of the files and data
    blob = dict()
    blob["VarList"] = variables
    blob["EditRequired"] = [str(tmp) for tmp in files_to_edit]
    blob["BaseFile"] = str(ref_file[-1])
    blob["Token"] = token
    blob["ReservedVariable"] = reserved_var

    # Filling some metadata
    blob["Metadata"] = dict()
    blob["Metadata"]["Date"] = datetime.datetime.today()
    blob["Metadata"]["OS"] = platform.system()
    blob["Metadata"]["OSVersion"] = platform.version()
    blob["Metadata"]["User"] = platform.node()

    # Then, read files and place them as binary streams into the blob while compressing it.
    blob["Files"] = dict()
    for index, file in enumerate(files):
        with open(file, "rb") as f:
            blob["Files"][str(rel_files[index])] = zlib.compress(f.read())

        if verbose > 1:
            print(f"Compressed [{(index + 1):3} / {len(files):3}] : {file}")

    # Now, export the blob into a bytestream
    blob_bytes = pickle.dumps(blob)

    # Get a hash of the bytestream
    hash = HashBytes(blob_bytes)
    hash_len = len(hash)

    # Append default name to the file if a specific .template file has not be provided.
    if not output.endswith(".template"):
        output_path = pathlib.Path(output) / "data.template"
    else:
        output_path = pathlib.Path(output)

    # Write file
    with open(str(output_path), "wb") as f:
        f.write(struct.pack(">I", hash_len))  # 4 bytes used !
        f.write(hash)
        f.write(blob_bytes)

    # Show the user the medatata we used
    if verbose > 0:
        printMetadata(
            hash,
            blob["Metadata"]["OS"],
            blob["Metadata"]["OSVersion"],
            blob["Metadata"]["Date"],
            blob["Metadata"]["User"],
        )

        # Add an end message
        printEnd()

    print(blob)

    return 0
