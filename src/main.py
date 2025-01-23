# Python libs
import pathlib
import base64

# Locals files
from prints import printHome, printSep, printFiles
from batch import (
    printHeader,
    printData,
    printVariables,
    printFolderStructure,
    printFileCreation,
    printAskForLocation,
    printFilesInfos,
    printDecoder
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
    printSep()

    is_file_valid = False
    while is_file_valid == False:
        try:
            BaseFileID = int(input("Enter the ID of the file for which the name shall be customized : "))
            if BaseFileID <= len(files):
                is_file_valid = True
            else:
                print("Enterred ID is valid but does not correspond to any file !")
        except:
            print("Please enter valid ID !")

    printSep()

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

    # Generate scripts
    with open(input_path + "/template.bat", "w+") as f:
        printHeader(f)
        printAskForLocation(f)
        printFilesInfos(f, len(files))
        printFolderStructure(f, folders)
        printFileCreation(f, rel_files, BaseFileID)
        printVariables(f, variables)

        for index, file in enumerate(files):
            # Read and encode file
            with open(file, "rb") as f2:
                # Read and replace ## with ! to mark the value as a variable. 
                # This is done here since it work with batch file only !
                tmp = f2.read().replace(b"##", b"!")
                tmp = base64.b64encode(tmp)

                edit = False
                if file in files_to_edit:
                    edit = True
                printData(f, rel_files[index], index, tmp, edit)

        printDecoder(f)


if __name__ == "__main__":
    TemplateCreator()
    exit()

    # Add for loops logics to decode files
    # Add file parsing !
