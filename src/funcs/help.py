def HelpMsg():
    print(
        """\
# This tool is developed to create images of folder that can be customized,   #\n\
# when the tool is asked to.                                                  #\n\
#
# This may be usefull when you want to create a dynamyc template for a        #\n\
# project and then only pass few arguments that are going to be replicated    #\n\
# everywhere !                                                                #\n\
#                                                                             #\n\
# Usage :                                                                     #\n\
#                                                                             #\n\
#   Creating files :                                                          #\n\
#       - Identify the different elements that shall be customized, and       #\n\
#         replace they name with ##VarName##, with VarName* a word that       #\n\
#         describe it's usage. It will be prompted to the final user !        #\n\
#       - Run the tool, it will handle everything for you.                    #\n\
#       - Share the data.template file !                                      #\n\
#       - The tool collect some data about the computer you used, to          #\n\
#         ensure file was the right one (Logged user, OS...)                  #\n\
#                                                                             #\n\
#   Reading files :                                                           #\n\
#       - Run the tool to open the file                                       #\n\
#       - It will compare hash of the data to ensure file was not             #\n\
#         modified since it's creation.                                       #\n\
#       - Answer the different questions of the tool, such as variable        #\n\
#         names                                                               #\n\
#       - Files were created into the folder where you'd just call the tool   #\n\
#                                                                             #\n\
# Remarks :
#       - Any variable with the "project" value will take the Project value ! #\n\
#         This can be used inside Makefiles or so to define the top level     #\n\
#         file !                                                              #\n\
#       - Even if the file is hashed to prevent unwanted modifications, the   #\n\
#         file remains uncrypted. This mean anyone with the file can read     #\n\
#         it's content, and it's written in clear ! Do not use, again, to     #\n\
#         share sensitive data (passwords and so ... ) !                      #\n\
==============================================================================="""
    )

    return 0
