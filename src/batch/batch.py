# Internal function, to write logs automatically
def WriteToLog(file: __file__, Function: str, Message: str):
    file.write(":: LOGS --------------------------------------------------------\n")
    file.write(f"""\
echo [%date% %time%] ^|     ^\n\
{Function:25}     ^|     ^\n\
{Message} >> logs.txt\n""")
    return


def printHeader(file: __file__):
    file.write(
        """\
:: Wrote by l.heywang with a scripting tool, available
::  on https://github.com/lheywang/TemplateCreator
:: build the folder structure for LaTeX report projects.
:: Include all of it's data under a single file to gain
::  in portability.

@echo off
setlocal EnableDelayedExpansion
:: Basic prints...
echo ===========================================================
echo # Let's expand the template to your target folder...      #
echo # The script can't install any tool needed, make sure     #
echo #      they work before trying anything...                #
echo #                                                         #
echo ===========================================================\n"""
    )
    return


def printAskForLocation(file: __file__):

    file.write(
        f"""
:: =============================================================
:: ASK FOR PATH AND PROJECT NAME AND GO TO IT
:: =============================================================\n"""
    )
    file.write(f"set /p base_path=Enter wanted folder location : \n")
    file.write(f"set /p base_name=Enter wanted folder name : \n")

    file.write(f"cd /D %base_path%\n")
    file.write(f"if not exist %base_name% mkdir %base_name%\n")
    file.write(f"cd %base_name%\n")

    # Write initialization log here, since we can't before...
    WriteToLog(file, "Initialisation", "Script started...")
    WriteToLog(file, "Folder creation", "Target folder created !")


def printData(file: __file__, filename: str, fileIndex: int, encodeddata, filetoedit):
    # first, split the encoded data into smaller chunks : 4096 characters here
    # This chunk size correspond to an issue : A variable can't be longer
    # than the maximal command line input, and the smallest I could fine was 4096 character (= bytes)
    chunk_size = 4096
    line_size = 64

    chunks = [
        encodeddata[i * chunk_size : (i + 1) * chunk_size]
        for i in range((len(encodeddata) + chunk_size - 1) // chunk_size)
    ]

    # Check if there is content to be added...
    # If not, exit directly.
    if len(chunks) == 0:
        return

    # Print some infos and delimiters to leave the script in a human understable format, even in base64 !
    file.write(
        f"""
:: =============================================================
:: FILE {filename} (Base64 encoded)
:: =============================================================\n"""
    )

    # Then, print this data into the target file + some infos to be easier to handle !
    # Parameters writing...
    file.write(f"set File{fileIndex}Name={filename}\n")
    file.write(f"set /A File{fileIndex}ChunkLen={len(chunks) - 1}\n")
    if filetoedit == True:
        file.write(f"set /A File{fileIndex}Edit=1\n")
    else:
        file.write(f"set /A File{fileIndex}Edit=0\n")

    # Then, split theses chunks into 64 character lines. We do this to be more
    # readable and easier to handle with text editor that struggle with long lines.
    for index, chunk in enumerate(chunks):
        lines = [
            chunk[i * line_size : (i + 1) * line_size]
            for i in range((len(chunk) + line_size - 1) // line_size)
        ]
        file.write(f"set File{fileIndex}Encoded{index}=")
        for line in lines:
            file.write(f"^\n{str(line)[2:-1]}")

        file.write(
            """
:: -------------------------------------------------------------\n"""
        )

    # end of the function, the file has been written !
    WriteToLog(file, "File fetching", f"Fetched {filename} from base64 encoding !")
    return


def printVariables(file: __file__, variables):
    # First, make sure that we got a list:

    vars = list(variables)

    file.write(
        f"""
:: =============================================================
:: VARIABLES INPUTS
:: =============================================================\n"""
    )

    file.write(
        """\
echo ===========================================================
echo # Please fill the variables to be replaced in the files   #
echo ===========================================================\n"""
    )

    for var in vars:
        file.write(f"set /p {var}=Enter value for field : '{var}' : \n")
        WriteToLog(file, "Variable input", f"Got a value for {var} : %{var}%")

    WriteToLog(file, "Variables input", "Got all the variables to be replaced !")

    return


def printFolderStructure(file: __file__, folders):

    folds = list(folders)

    file.write(
        f"""
:: =============================================================
:: FOLDERS CREATION
:: =============================================================\n"""
    )

    for folder in folds:
        file.write(f"if not exist '{str(folder)}' mkdir {str(folder)}\n")
        WriteToLog(file, "Folder creation", f"Created folder {str(folder)} !")

    WriteToLog(file, "Folder creation", "Created folder structure !")

    return


def printFileCreation(file: __file__, files, BaseFile):
    filest = list(files)

    file.write(
        f"""
:: =============================================================
:: FILES CREATION
:: =============================================================\n"""
    )

    for index, name in enumerate(filest):
        if index == BaseFile:
            file.write(f"echo. > %base_name%.{str(name).split(".")[-1]}\n")
            WriteToLog(
                file,
                "Folder creation",
                f"Created file  %base_name%.{str(name).split(".")[-1]} !",
            )
        else:
            file.write(f"echo. > {name}\n")
            WriteToLog(file, "Folder creation", f"Created file {str(name)} !")

    WriteToLog(file, "File creation", "Created empty files !")

    return


def printFilesInfos(file: __file__, fileNB):
    file.write(
        f"""
:: =============================================================
:: FILES INFOS
:: =============================================================\n"""
    )

    file.write(f"set /A file_count={fileNB}\n")
    WriteToLog(file, "Script parameters", "Got script parameters !")

    return


def printDecoder(file: __file__):
    file.write(
        f"""
:: =============================================================
:: DECODER LOGIC
:: =============================================================\n"""
    )

    WriteToLog(file, "File decoding", "Starting decoding and replacement of files...")

    # Handle syntax error here...

    # First, iterate over different files:
    file.write(
        f"""
for /l %%i in (0, 1, %file_count%) do (
               
    :: If file is non empty :
    if defined File%%iName (
    
        :: list all chunks
        for /l %%e in (0, 1, !File%%iChunkLen! - 1) do (
            echo !File%%iEncoded%%e! >> tmp.b64
        )
               
        :: file is non edited, dump directly into dest
        if !File%%iEdit!==0 (
            echo [%date% %time%] ^| Decoding                              ^| >> logs.txt
            certutil.exe -f -decode tmp.b64 !File%%iName! >> logs.txt
            del tmp.b64
               
        ) else (
            :: decode file into tmp file
            echo [%date% %time%] ^| Decoding                              ^| >> logs.txt
            certutil.exe -f -decode tmp.b64 tmp.txt >> logs.txt
            
            :: Doing this will force to replace variable automatically...
            for /F "delims=" %%a in (tmp.txt) do (
	            echo %%a >> !File%%iName!
            )
            
            :: Delete temporary files
            if exist "tmp.txt" del tmp.txt
            if exist "tmp.b64" del tmp.b64
        )
    )
)
"""
    )

    WriteToLog(file, "File decoding", "Decoded all files ! Job Done !")

    return
