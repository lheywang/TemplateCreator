# -------------------------------------------------------------------------------
#   tcreator-open :     Code for the command "tcreator-open", charged to open
#                       an archive and expand it.
#
#   l.heywang
#   10-05-2025
#
# -------------------------------------------------------------------------------

# module import
import argparse  # Python 3.2
import sys

# Code import
from funcs.decoder import Decoder


# Main function
def tcreator_open():
    """
    tcreator_open : Entry point for the tcreator-open command line.

        Arguments :
            - template :                File to open
            - -i / --ignorev:           Ignore variables. They will be set to the default string.
                                        Done to prevent the CLI to ask questions that can be blocking.
                                        Not recommended for the end user.
            - -o / --output:            Output path. Used to change the output path of the command.
            - -v / --verbose :          Print verbose output

        Returns :

    """
    # Creating the parser
    parser = argparse.ArgumentParser(
        prog="tcreator-open",
        description="Open a .template file and expand it.",
        epilog="WARNING : Actually, this tool will ask the user inputs. In case of automated use, set --ignorev to True to block this behavior. Variables will be left untouched then.",
    )

    # Adding arguments :
    parser.add_argument("template", help="Pass the .template file to be openned.")
    parser.add_argument(
        "-i",
        "--ignorev",
        default=False,
        action="store_true",
        help="Indicate to the script to ignore the input for the variables. Recommended for automated usages, not for final user.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=".",
        help="Change the output destination of the expanded folder",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help="Add logs output when running the command",
    )

    # Parsing arguments
    args = parser.parse_args()

    # Then, we can call the decoder function
    verbose = 0
    if args.verbose == True:
        verbose = 2
    else:
        verbose = 0

    rval = Decoder(
        args.template,
        args.ignorev,
        verbose,
        args.output,
        None,
        0,
    )
    return rval


if __name__ == "__main__":
    rval = tcreator_open()
    sys.exit(rval)
