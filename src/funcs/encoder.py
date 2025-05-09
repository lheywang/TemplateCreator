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
import zlib

from .messages import printEnd, printFiles, printSep, printMetadata, AskUserInteger


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
    p = pathlib.Path(__file__).parent.resolve()
    p = p / "../../config/config.toml"

    with open(str(p), "rb") as f:
        config = tomllib.load(f)

    # Setting some variable to track state of the program
    is_path_valid = False
    base_path = None

    printSep()
    # Requesting the user to input a path
    while is_path_valid == False:
        input_path = input("Enter the source folder for the template : ")

        try:
            base_path = pathlib.Path(input_path).glob("**/*")
            is_path_valid = True
        except KeyboardInterrupt:
            return 1
        except:
            print("Please enter a valid path !")

    # Get the list of all the files, and then print them
    files = [x for x in base_path if x.is_file()]
    printFiles(files)
    printSep()

    # Getting the name of the custom file
    # Ask the user to select a file
    BaseFileID = AskUserInteger(
        "Enter the ID of the file to be customized ? ", (len(files) - 1)
    )

    # detect files and variables to be modified
    files_to_edit = []
    binary_files = []
    variables = []

    # Get the token value
    token = config["Reader"]["Token"]
    reserved_var = config["Reader"]["ReservedVariable"]

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

        print(f"Rode       [{(index + 1):3} / {len(files):3}] : {file}")

    # Remove variables that are tied to the project name (this variable will be
    # asked globally, and shall not be in the variable list)
    for index, var in enumerate(variables):
        if var == reserved_var:
            del variables[index]

    # Simplify files path
    rel_files = []
    folders = []
    for file in files:
        # Compute relative path
        tmp = file.relative_to(pathlib.Path(input_path))

        # Append relative file and folder
        rel_files.append(tmp)
        folders.append(tmp.parent)

    edit = []
    for file in files_to_edit:
        # Compute relative path
        tmp = file.relative_to(pathlib.Path(input_path))

        # Append relative file and folder
        edit.append(tmp)

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
    blob["BaseFile"] = str(rel_files[BaseFileID])
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

        print(f"Compressed [{(index + 1):3} / {len(files):3}] : {file}")

    # Now, export the blob into a bytestream
    blob_bytes = pickle.dumps(blob)

    # Get a hash of the bytestream
    hasher = hashlib.sha3_512()
    hasher.update(blob_bytes)
    hash = hasher.digest()
    hash_len = len(hash)

    # Write to the file the different data, in order
    output = pathlib.Path(input_path) / "data.template"
    with open(str(output), "wb") as f:
        f.write(struct.pack(">I", hash_len))  # 4 bytes used !
        f.write(hash)
        f.write(blob_bytes)

    # Show the user the medatata we used
    printMetadata(
        hash,
        blob["Metadata"]["OS"],
        blob["Metadata"]["OSVersion"],
        blob["Metadata"]["Date"],
        blob["Metadata"]["User"],
    )

    # End message
    printEnd()

    return 0
