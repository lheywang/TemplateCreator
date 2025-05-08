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

from .messages import printFiles, printSep, printMetadata


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

    # First, input the user for the file to be rode
    act_path = pathlib.Path(".").glob("*.template")
    files = [x for x in act_path if x.is_file()]
    printFiles(files)

    # Getting the name of the custom file
    is_file_valid = False
    while is_file_valid == False:
        try:
            BaseFileID = int(input("Enter the ID of the file to be rode ? "))
            if BaseFileID <= len(files):
                is_file_valid = True
            else:
                print("Enterred ID is valid but does not correspond to any file !")
        except:
            print("Please enter valid ID !")

    # Then, start to read the file and get the hash
    with open(files[BaseFileID], "rb") as f:
        # Reading the hash length
        hash_len_bytes = f.read(4)
        if not hash_len_bytes or len(hash_len_bytes) < 4:
            print("File is too short to contain hash length.")
            return -1

        hash_len = struct.unpack(">I", hash_len_bytes)[0]
        stored_hash = f.read(hash_len)

        if not stored_hash:
            print("File does not contain hash data.")
            return -2

        pickled_data = f.read()
        if not pickled_data:
            print("File does not contain pickled data.")
            return -3

    # Hashing the whole data to ensure it didn't move
    hasher = hashlib.sha3_512()
    hasher.update(pickled_data)
    hash = hasher.digest()

    if hash != stored_hash:
        printSep()
        print("File hash do not correspond. Shall we continue ?")
        # Action selection
        print(f"- [{0:3}] : No")
        print(f"- [{1:3}] : Yes (DANGEROUS !)")
        # Wait for a correct user input :
        is_hashact_valid = False
        while is_hashact_valid == False:
            try:
                action = int(input("Enter what's the required action ? "))
                if action <= 1:
                    is_hashact_valid = True
                else:
                    print(
                        "Enterred ID is valid but does not correspond to any known action !"
                    )
            except:
                print("Please enter valid ID !")
        printSep()

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

    # Action selection
    print(f"- [{0:3}] : No")
    print(f"- [{1:3}] : Yes")
    # Wait for a correct user input :
    is_metaact_valid = False
    while is_metaact_valid == False:
        try:
            action = int(input("Enter what's the required action ? "))
            if action <= 1:
                is_metaact_valid = True
            else:
                print(
                    "Enterred ID is valid but does not correspond to any known action !"
                )
        except:
            print("Please enter valid ID !")
    printSep()

    if action == 0:
        print("Exiting...")
        return -129

    # Start the loading of the file now
    # First, create the files and folders
    for file in data["Files"]:
        p = pathlib.Path(file)
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)

        with open(p, "w+") as f:
            f.write("")

    # Ask for variables
    # Then, read the file to check if there is any token
    # Replace theses variables
    # Write the files
    # END

    return 0
