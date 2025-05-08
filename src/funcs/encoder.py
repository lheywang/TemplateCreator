# -------------------------------------------------------------------------------
#   Encoder.py : Encode a folder and it's structure into a blob file
#
#   l.heywang
#   08-05-2025
#
# -------------------------------------------------------------------------------

# Modules import
import pickle
import pathlib
import datetime
import platform
import hashlib
import struct

from .messages import printEnd, printFiles, printSep, printMetadata


# Encoder function
def Encoder():
    """
    Encoder :   Function that explore a folder and subfolder for files, parses files, and create an output blob.
                Add some metadata and a hash value to ensure the pickled data has been correctly handled !

    Arguments :
        None

    Returns :
        Integer :
            0 = SUCESS
            !0 = ERROR
    """

    import tomllib  # This line required python 3.11, placed here to not cause any issues with older versions !

    # Reading config files
    config = None
    with open("../config/config.toml", "rb") as f:
        config = tomllib.load(f)

        # Setting some variable to track state of the program
    is_path_valid = False
    base_path = None

    # Requesting the user to input a path
    while is_path_valid == False:
        input_path = input("Enter the source folder for the template : ")

        try:
            base_path = pathlib.Path(input_path).glob("**/*")
            is_path_valid = True
        except:
            print("Please enter a valid path !")

    # Get the list of all the files, and then print them
    files = [x for x in base_path if x.is_file()]
    printFiles(files)
    printSep()

    # Getting the name of the custom file
    is_file_valid = False
    while is_file_valid == False:
        try:
            BaseFileID = int(
                input(
                    "Enter the ID of the file for which the name shall be customized : "
                )
            )
            if BaseFileID <= len(files):
                is_file_valid = True
            else:
                print("Enterred ID is valid but does not correspond to any file !")
        except:
            print("Please enter valid ID !")

    # detect files and variables to be modified
    files_to_edit = []
    binary_files = []
    variables = []

    # Get the token value
    token = config["Reader"]["Token"]

    for file in files:
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

                        else:
                            # Copy variable name
                            variables.append(tmp_s[1])

                            # Delete three first strings
                            del tmp_s[0]
                            del tmp_s[0]
                            del tmp_s[0]

                            # The next one will be a variable name
                            for index, text in enumerate(tmp_s):
                                # Ignore one over two iterations
                                if index % 2 == 1:
                                    continue

                                variables.append(tmp_s[index])

        except (
            UnicodeDecodeError
        ):  # Handle non text files that aren't going to be parsed
            binary_files.append(file)
            continue

    # Simplify files path
    rel_files = []
    folders = []
    for file in files:
        # Compute relative path
        tmp = file.relative_to(pathlib.Path(input_path))

        # Append relative file and folder
        rel_files.append(tmp)
        folders.append(tmp.parent)

    # Remove duplicates
    variables = list(dict.fromkeys(variables))
    folders = list(dict.fromkeys(folders))

    # Remove '.' path
    if pathlib.Path(".") in folders:
        folders.remove(pathlib.Path("."))

    # Then, creating a big dict of the files
    blob = dict()
    blob["Metadata"] = dict()
    blob["VarList"] = []
    blob["EditRequired"] = []
    blob["Files"] = dict()

    # Filling some metadata
    blob["Metadata"]["Date"] = datetime.datetime.today()
    blob["Metadata"]["OS"] = platform.system()
    blob["Metadata"]["OSVersion"] = platform.version()
    blob["Metadata"]["User"] = platform.node()

    # Then, fill config variables
    blob["EditRequired"] = files_to_edit  # To somplify
    blob["VarList"] = variables

    # Then, read files and place them as binary streams into the blob
    for index, file in enumerate(files):
        with open(file, "rb") as f:
            blob["Files"][str(rel_files[index])] = f.read()

    # Now, export the blob into a file
    blob_bytes = pickle.dumps(blob)

    # Get a hash of the data
    hasher = hashlib.sha3_512()
    hasher.update(blob_bytes)
    hash = hasher.digest()
    hash_len = len(hash)
    print(hash, hash_len)

    with open("data.template", "wb") as f:
        f.write(struct.pack(">I", hash_len))  # 4 bytes used !
        f.write(hash)
        f.write(blob_bytes)

    printMetadata(
        hash,
        blob["Metadata"]["OS"],
        blob["Metadata"]["OSVersion"],
        blob["Metadata"]["Date"],
        blob["Metadata"]["User"],
    )

    printEnd()

    return 0
