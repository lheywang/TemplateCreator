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
import hashlib
import struct

# Other files
from .messages import printFiles, printSep, printMetadata, AskUserInteger


# Encoder function
def Decoder():
    """
    Decoder : Function that explore a template and create all files and customize them !

    Arguments :
        None

    Returns :
        Integer :
            0 = SUCESS
            !0 = ERROR
    """

    # First, search for .template file where the script is called
    act_path = pathlib.Path(".").glob("*.template")
    files = [x for x in act_path if x.is_file()]
    printFiles(files)

    # Ask the user to select a file
    BaseFileID = AskUserInteger(
        "Enter the ID of the file to be rode ? ", (len(files) - 1)
    )

    # Then, ensure the file has not been modified by comparing the stored hash and the
    # locally calculated one.
    with open(files[BaseFileID], "rb") as f:

        # Reading the hash length
        hash_len_bytes = f.read(4)
        if not hash_len_bytes or len(hash_len_bytes) < 4:
            print("File is too short to contain hash length.")
            return -1
        hash_len = struct.unpack(">I", hash_len_bytes)[0]

        # Read the hash
        stored_hash = f.read(hash_len)
        if not stored_hash:
            print("File does not contain hash data.")
            return -2

        # Read the data (binary for now)
        pickled_data = f.read()
        if not pickled_data:
            print("File does not contain pickled data.")
            return -3

    # Hashing the whole data to ensure it didn't move
    hasher = hashlib.sha3_512()
    hasher.update(pickled_data)
    hash = hasher.digest()

    # Comparing hash to ensure they're matching.
    # The user can force the manipulation if needed, but clearly not required !
    if hash != stored_hash:
        printSep()
        print("File hash do not correspond. Shall we continue ?")
        # Action selection
        print(f"- [{0:3}] : No")
        print(f"- [{1:3}] : Yes (DANGEROUS !)")
        # Wait for a correct user input :

        # Ask the user to select a file
        action = AskUserInteger("Continue ? ", 1)
        printSep()

        # Exit the code here, to ensure the binary data can't cause anything
        if action == 0:
            print("Exiting...")
            return -128

    # Loading the pickled data
    data = pickle.loads(pickled_data)

    # Showing to the user some metadata about the file :
    printMetadata(
        hash,
        data["Metadata"]["OS"],
        data["Metadata"]["OSVersion"],
        data["Metadata"]["Date"],
        data["Metadata"]["User"],
    )

    # Ask the user if the metadata are correct
    print(f"- [{0:3}] : No")
    print(f"- [{1:3}] : Yes")
    action = AskUserInteger("Are the metadata correct ? ", 1)
    printSep()

    # Exit if no
    if action == 0:
        print("Exiting...")
        return -129

    # Ask for the base filename ?
    variables = dict()
    variables[data["ReservedVariable"]] = input(
        "What's the name of the project, to custom the base names ? "
    )

    # Ask the user for the different variables that where listed
    printSep()
    print("Now enter the values for the different variables :")
    for index, var in enumerate(data["VarList"]):
        if var != data["ReservedVariable"]:
            val = str(input(f"- [{index:3}] : {var} = "))
            variables[var] = val
    printSep()

    # Load the files, and create them on the target computer.
    # If the file is the one where it's name shall be modified, change it.
    tmp_dict = dict()
    for index, file in enumerate(data["Files"]):

        # Check if the file is the base one
        if file == data["BaseFile"]:

            # Open a path, but rename the file before creating it.
            source = pathlib.Path(file)
            p = source.with_stem(variables[data["ReservedVariable"]]).with_suffix(
                source.suffix
            )

            # Flag the new file to the edited :
            data["EditRequired"].append(str(p))

        # In any case, create parents and write "" to the file to ensure the OS will create it.
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w+") as f:
            f.write("")

        # Append new file name to a temp dict (we can"t update the keys of a dict while iterating over it)
        tmp_dict[str(p)] = data["Files"][file]

        # User logs
        print(f"Customized [{(index + 1):3} / {len(data["Files"]):3}] : {str(p)}")

    # Copy the temp dict to the real one (and thus update the file names !)
    data["Files"] = tmp_dict
    printSep()

    # Then, iterate over file, customize if needed, and write them.
    for index, file in enumerate(data["Files"]):

        if file in data["EditRequired"]:

            # Decode byte encoded string.
            tmp_content = data["Files"][file].decode()

            # Iterate over variables to be modified
            for var in variables:
                tmp_content = tmp_content.replace(
                    f"{data["Token"]+var+data["Token"]}", variables[var]
                )

            # Save into the dict the modified variable
            data["Files"][file] = tmp_content.encode()

        # Perform write operation, as binary to let the \n char and other be real (and not treated as strings)
        with open(file, "wb") as f:
            f.write(data["Files"][file])

        print(f"Wrote      [{(index + 1):3} / {len(data["Files"]):3}] : {file}")

    # User end logs
    printSep()
    print("Finished creating a new folder from template !")

    return 0
