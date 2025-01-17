# Python libs
import pathlib

# Locals files
from prints import printHome, printMenu, printSep, printFiles

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
        print(file)
        try:
            # Try to open and reas the file.
            with open(file, "r") as f:
                lines = f.readlines()

                # Iterate over the lines to mark any variables
                for line in lines:
        
                    if "##" in line:

                        files_to_edit.append(file)
                        tmp_s = line.split("##")
                        print(tmp_s)

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

                            print(tmp_s)

                            # The next one will be a variable name
                            for index, text in enumerate(tmp_s):
                                # Ignore one over two iterations
                                if index % 2 == 1:
                                    continue

                                variables.append(tmp_s[index])

                            

            
        except UnicodeDecodeError: # Handle non text files that aren't going to be parsed
            continue

    # Ok for now ! Let's generate scripts, encode data and so...
    print(files_to_edit, variables)


if __name__ == "__main__":
    TemplateCreator()
    exit()