import datetime


def printHome():
    return """\
===============================================================================\n\
# Welcome on the Template  tool !                                             #\n\
# Do you want to read or write a template file ?                              #\n\
#                                                                             #\n\
# Requirements :                                                              #\n\
#   - Reading template : Python 3.6                                           #\n\
#   - Writing template : Python 3.11                                          #\n\
#                                                                             #\n\
# A file will be read / wrote, data.template.                                 #\n\
===============================================================================\n"""


def printSep():
    return "===============================================================================\n"


def printFiles(files):
    rval = """\
Found files on the target folder :\n"""

    for index, file in enumerate(files):
        rval = rval + (f"- [{index:3}] : {file}\n")

    return rval


def printEnd():
    return """\
# Exported a blob of the files into data.template. Feel free to share it,     #\n\
# with your friends !                                                         #\n\
#                                                                             #\n\
# They only need python 3 to extract it ! (3.11 required for writting !),     #\n\
# regardless of the OS.                                                       #\n\
#                                                                             #\n\
# Just a reminder : This blob isn't encrypted properly and thus SHALL NOT     #\n\
# contain any sensitive data. I, as the developper can't be sued for any      #\n\
# data loss /                                                                 #\n\
# corruption / leak !                                                         #\n"""


def printMetadata(Hash, OS, Version, Date, User):
    return f"""\
===============================================================================\n\
# File contain theses metadatas :                                             #\n\
#  - Hash       = {str(Hash)}\n\
#  - Date       = {Date}\n\
#  - OS         = {OS}\n\
#  - Version    = {Version}\n\
#  - User       = {User}\n\
#\n\
# Make sure they're correct !
===============================================================================\n"""


def AskUserInteger(message, max):
    # Then, ask the user to select the .template file that is found !
    while True:

        # Securely ask the user for a number
        try:
            ID = int(input(message))

            # Validate user input
            if ID <= max:
                return ID
            else:
                print("Valid input, but it does not correspond to anything known...")

        # User cancel script
        except KeyboardInterrupt:
            return -1

        # NaN
        except:
            print("Please enter valid ID !")
