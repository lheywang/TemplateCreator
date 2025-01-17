def printHome():
    print(
        """\
===============================================================================\n\
# Welcome on the Template creator tool !                                      #\n\
# The tool will now ask you inputs ...                                        #\n\
==============================================================================="""
    )
    return


def printMenu():
    pass

def printSep():
    print("===============================================================================")
    return

def printFiles(files):
    printSep()
    print("""\
Found files on the system :""")
    for file in files:
        print(f"- {file}")