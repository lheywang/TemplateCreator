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

def printSep():
    print("===============================================================================")
    return

def printFiles(files):
    printSep()
    print("""\
Found files on the target folder :""")
    for index, file in enumerate(files):
        print(f"- [{index:3}] : {file}")

