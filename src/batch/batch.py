def printHeader(file: __file__):
    file.write(
        """\
:: Wrote by l.heywang with a scripting tool, available on https://github.com/lheywang/TemplateCreator\n\
:: build the folder structure for LaTeX report projects.\n\
:: Include all of it's data under a single file to gain in portability.\n\
\n\
@echo off\n\
:: Basic prints...\n\
echo =============================================================\n\
echo # Let's expand the template to your target folder...        #\n\
echo # The script can't install any tool needed, make sure       #\n\
echo #      they work before trying anything...                  #\n\
echo #                                                           #\n\
echo =============================================================\n"""
    )
    return

def printAskForLocation(file: __file__):

    file.write(
        f"""\n\n\
:: =============================================================\n\
:: ASK FOR PATH AND GO TO IT\n\
:: =============================================================\n""")
    file.write(f"set /p base_path=Enter wanted folder location : \n")
    file.write(f"set /p base_name=Enter wanted folder name : \n")

    file.write(f"cd /D %base_path%\n")
    file.write(f"if not exist %base_name% mkdir %base_name%\n")
    file.write(f"cd %base_name%\n")


def printData(file: __file__, filename: str, fileIndex: int, encodeddata, filetoedit):
    # Print some infos and delimiters to remain the script a correct structure
    file.write(
        f"""\n\n\
:: =============================================================\n\
:: FILE {filename}\n\
:: =============================================================\n""")

    # first, split the encoded data into smaller chunks : 4096 characters here
    # This chunk size correspond to an issue : A variable can't be longer
    # than the command line input, and the smallest I could fine was 4096 character (= bytes)
    chunk_size = 4096
    line_size = 64

    chunks = [
        encodeddata[i * chunk_size : (i + 1) * chunk_size]
        for i in range((len(encodeddata) + chunk_size - 1) // chunk_size)
    ]

    # Then, print this data into the target file + some infos to be easier to handle !
    # Parameters writing...
    file.write(f"set File{fileIndex}Name={filename}\n")
    file.write(f"set File{fileIndex}ChunkLen={len(chunks)}\n")
    if filetoedit == True:
        file.write(f"set File{fileIndex}Edit=1\n")
    else:
        file.write(f"set File{fileIndex}Edit=0\n")

    # Then, split theses chunks into 64 character lines. We do this to be more
    # readable and easier to handle with text editor with struggle with long lines.
    for index, chunk in enumerate(chunks):
        lines = [
            chunk[i * line_size : (i + 1) * line_size]
            for i in range((len(chunk) + line_size - 1) // line_size)
        ]
        file.write(f"set File{fileIndex}Encoded{index}=^\n")
        for line_cnt, line in enumerate(lines):
            if line_cnt != 63:
                file.write(f"{line}^\n")
            else:
                # Remove the '^' for the last char, to prevent from overlapping chunks.
                file.write(f"{line}\n")

    # end of the function, the file has been written !
    return

def printVariables(file: __file__, variables):
    # First, make sure that we got a list:

    vars = list(variables)
    
    file.write(
        f"""\n\n\
:: =============================================================\n\
:: VARIABLES INPUTS\n\
:: =============================================================\n""")
    
    file.write("""\
echo =============================================================\n\
echo # Please fill the variables to be replaced in the files      #\n\
echo =============================================================\n""")

    for var in vars:
        file.write(f"set /p {var}=Enter value for field : '{var}' : \n")

    return 

def printFolderStructure(file: __file__, folders):
    
    folds = list(folders)
    
    file.write(
        f"""\n\n\
:: =============================================================\n\
:: FOLDERS CREATION\n\
:: =============================================================\n""")
    
    for folder in folds:
        file.write(f"if not exist '{str(folder)}' mkdir {str(folder)}\n")

    return

def printFileCreation(file: __file__, files):
    filest = list(files)

    file.write(
        f"""\n\n\
:: =============================================================\n\
:: FILES CREATION\n\
:: =============================================================\n""")
    
    for name in filest:
        file.write(f"echo. > {name}\n")

    return


