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
import hashlib  # Python 3.6 (changes in 3.12 fallback, shall not cause issues but who know...)
import struct  # base python
import zlib  # base python

# Minimal comp : Python 3.6

# Other files
from .messages import printSep
from .utilities import HashBytes
from .guihelper import guiprint, guiinput


# Encoder function
def Decoder(
    template: str,
    ignore_variables: bool,
    verbose: int,
    output: str,
    h_GUI,
    mode: int,
):
    """
    Decoder : Decode a defined template file and output a customized folder structure.

        Arguments :
            - template (str) :          The path for the template file to be outputed.
            - ignore_variables (bool) : Shall we ignore variables (they thus won't be subsitued).
            - verbose :                 The verbose level. 0 = No verbose. 1 = Step verbose. 2 = Full verbose.
            - output :                  Output folder where the files need to be expanded.
            - h_GUI :                   Handler to the GUI. Can be set to None if mode = 0.
            - mode :                    Redirect output to : Console if == 0, GUI if == 1.

        Returns (int) :
            - -1 :                      Template file too small. Did you pass the right file ?
            - -2 :                      Hash does not correspond. The file has been modified.
    """
    # Create different paths
    template_path = pathlib.Path(template)
    output_path = pathlib.Path(output)

    # Then, ensure the file has not been modified by comparing the stored hash and the
    # locally calculated one.
    with open(str(template_path), "rb") as f:

        # Reading the hash length
        hash_len_bytes = f.read(4)
        if not hash_len_bytes or len(hash_len_bytes) < 4:
            guiprint(
                h_GUI,
                mode,
                verbose,
                -1,
                "File is too short to contain hash length. Aborting...",
            )
            return -1

        hash_len = struct.unpack(">I", hash_len_bytes)[0]

        # Read the hash
        stored_hash = f.read(hash_len)
        if not stored_hash:
            guiprint(
                h_GUI,
                mode,
                verbose,
                -1,
                "File does not contain hash data. Aborting...",
            )
            return -1

        # Read the data (binary for now)
        pickled_data = f.read()
        if not pickled_data:
            guiprint(
                h_GUI,
                mode,
                verbose,
                -1,
                "File does not contain pickled data. Aborting...",
            )
            return -1

    # Hashing the whole data to ensure it didn't move
    hash = HashBytes(pickled_data)

    # Comparing hash to ensure they're matching. If they're not, exit.
    if hash != stored_hash:
        guiprint(
            h_GUI,
            mode,
            verbose,
            -1,
            "File hash do not correspond. Aborting...",
        )
        return -2

    # Loading the pickled data
    data = pickle.loads(pickled_data)

    # Ask for the base filename ?
    variables = dict()
    variables[data["ReservedVariable"]] = guiinput(
        h_GUI, mode, "What's the name of the project, to custom the base names ? "
    )

    # Ask the user for the different variables that where listed
    if ignore_variables == False:
        guiprint(
            h_GUI,
            mode,
            verbose,
            -1,
            "Now enter the values for the different variables :",
        )
    for index, var in enumerate(data["VarList"]):

        if var != data["ReservedVariable"]:

            # Let the the variable name as default
            if ignore_variables == False:
                val = guiinput(
                    h_GUI,
                    mode,
                    f"- [{index:3}] : {var} = ",
                )
            else:
                val = f"{data["Token"]}{var}{data["Token"]}"

            variables[var] = val

    # Load the files, and create them on the target computer.
    # If the file is the one where it's name shall be modified, change it.
    tmp_dict = dict()
    for index, file in enumerate(data["Files"]):

        # Get path of the file. May be modified if needed.
        p = pathlib.Path(file)

        # Check if the file is the base one
        if file == data["BaseFile"]:

            # Open a path, but rename the file before creating it.
            source = pathlib.Path(file)
            p = source.with_stem(variables[data["ReservedVariable"]]).with_suffix(
                source.suffix
            )

            # Flag the new file to the edited :
            data["EditRequired"].append(str(p))

        # Update the output file with the wanted output
        tmp = output_path / p

        # In any case, create parents and write "" to the file to ensure the OS will create it.
        if not tmp.exists():
            tmp.parent.mkdir(parents=True, exist_ok=True)

        with open(str(tmp), "w+") as f:
            f.write("")

        # Append new file name to a temp dict (we can"t update the keys of a dict while iterating over it)
        tmp_dict[str(p)] = data["Files"][file]

        # User logs
        guiprint(
            h_GUI,
            mode,
            verbose,
            1,
            f"Customized [{(index + 1):3} / {len(data["Files"]):3}] : {str(p)}",
        )

    # Copy the temp dict to the real one (and thus update the file names !)
    data["Files"] = tmp_dict

    # Then, iterate over file, customize if needed, and write them.
    for index, file in enumerate(data["Files"]):

        # Uncompress the data
        datab = zlib.decompress(data["Files"][file])

        if file in data["EditRequired"]:

            # Decode byte encoded string.
            tmp_content = datab.decode()

            # Iterate over variables to be modified
            for var in variables:
                tmp_content = tmp_content.replace(
                    f"{data["Token"]+var+data["Token"]}", variables[var]
                )

            # Save into the dict the modified variable
            datab = tmp_content.encode()

        # Perform write operation, as binary to let the \n char and other be real (and not treated as strings)
        tmp = output_path / pathlib.Path(file)
        with open(str(tmp), "wb") as f:
            f.write(datab)

        guiprint(
            h_GUI,
            mode,
            verbose,
            1,
            f"Wrote      [{(index + 1):3} / {len(data["Files"]):3}] : {file}",
        )

    # User end logs
    guiprint(
        h_GUI,
        mode,
        verbose,
        -1,
        "Finished creating a new folder from template !",
    )

    return 0
