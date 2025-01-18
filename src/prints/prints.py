def printHome():
    print(
        """\
===============================================================================\n\
# Welcome on the Template creator tool !                                      #\n\
# The tool will now ask you inputs ...                                        #\n\
#                                                                             #\n\
# Two script will be generated : a .bat and a .sh for all systems !           #\n\
===============================================================================""")
    return


def printMenu():
    pass

def printSep():
    print("===============================================================================")
    return

def printFiles(files):
    printSep()
    print("""\
Found files on the target folder :""")
    for file in files:
        print(f"- {file}")