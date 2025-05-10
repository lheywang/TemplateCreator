# -------------------------------------------------------------------------------
#   tcreator-write :    Code for the command "tcreator-write", charged to
#                       create an archive from the passed folder
#   l.heywang
#   10-05-2025
#
# -------------------------------------------------------------------------------

# Module import
import argparse  # Python 3.2
import sys

# Code import
from funcs.encoder import Encoder


# Main function
def tcreator_write():
    """
    tcreator_open : Entry point for the tcreator-open command line.

        Arguments :
            - folder :                  Base folder to be zipped on template
            - file :                    A file inside of the folder, which name will be customized.
            - -o / --output:            Output path. Used to change the output path of the command.
            - -t / --token :            Can change the used token for this compression
            - -v / --verbose :          Print verbose output
            - -p / --project :          Change the name of the variable used for 'file' name, but any other customization.

        Returns :

    """
    # Creating the parser
    parser = argparse.ArgumentParser(
        prog="tcreator-write", description="Create a template from a used folder"
    )

    # Adding arguments :
    parser.add_argument(
        "folder", help="Pass the folder you want to zip into a template"
    )
    parser.add_argument(
        "file",
        help="Pass the file for which the name can be customized (ex : main file)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=".",
        help="Change the output location of the template file.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help="Add logs output for the user",
    )
    parser.add_argument(
        "-t",
        "--token",
        default="##",
        help="Change the parsed token to identify variables. Can be usefull is your langage use the default one '##'",
    )
    parser.add_argument(
        "-p",
        "--project",
        default="project",
        help="Change the name of the variable that is used as name for file, or any other customization.",
    )

    # Parsing arguments
    args = parser.parse_args()

    # Then, we can call the encoding function
    verbose = 0
    if args.verbose == True:
        verbose = 2
    else:
        verbose = 0

    rval = Encoder(
        args.folder, args.file, args.token, verbose, args.project, args.output
    )

    return rval


if __name__ == "__main__":
    rval = tcreator_write()
    sys.exit(rval)
