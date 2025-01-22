# Python libs
import pathlib
import base64

# Locals files
from prints import printHome, printMenu, printSep, printFiles
from batch import (
    printHeader,
    printData,
    printVariables,
    printFolderStructure,
    printFileCreation,
    printAskForLocation,
)


def TemplateCreator():
    # First, input the source folder for the template :
    printHome()

    is_path_valid = False
    base_path = None
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

    # detect files and variables to be modified
    files_to_edit = []
    variables = []

    for file in files:
        try:
            # Try to open and reas the file.
            with open(file, "r") as f:
                lines = f.readlines()

                # Iterate over the lines to mark any variables
                for line in lines:

                    if "##" in line:

                        files_to_edit.append(file)
                        tmp_s = line.split("##")

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
            continue

    # Then, encode all of the data
    encoded = []
    for file in files:
        with open(file, "rb") as f:
            tmp = f.read()
            encoded.append(base64.b64encode(tmp))

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

    # Need to write the preample : File count, list, edited files, needed variables and soooo
    # Need to add the logic to handle theses variables and file edits.

    # Generate scripts
    with open(input_path + "/template.bat", "w+") as f:
        printHeader(f)
        printAskForLocation(f)
        printFolderStructure(f, folders)
        printFileCreation(f, rel_files)
        printVariables(f, variables)
        printData(f, "test.png", 0, encoded[4], True)


if __name__ == "__main__":
    TemplateCreator()
    exit()
