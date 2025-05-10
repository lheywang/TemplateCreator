# -------------------------------------------------------------------------------
#   TemplateCreator.py
#
#   l.heywang
#   08-05-2025
#
# -------------------------------------------------------------------------------

# Other functions imports
from funcs.messages import printHome, printSep
from funcs.encoder import Encoder
from funcs.decoder import Decoder
from funcs.help import HelpMsg

import pathlib


# Main file
def main():
    # Welcome message
    printHome()

    # Fetch the script path, to handle config file IO easily.
    script_path = pathlib.Path(__file__).parent.resolve()

    # Action selection
    print(f"- [{0:3}] : Open a file (.template)")
    print(f"- [{1:3}] : Create a template file")
    print(f"- [{2:3}] : Print help")

    # Wait for a correct user input :
    is_action_valid = False
    while is_action_valid == False:
        try:
            action = int(input("Enter what's the required action ? "))
            if action <= 2:
                is_action_valid = True
            else:
                print(
                    "Enterred ID is valid but does not correspond to any known action !"
                )
        # User cancelled process
        except KeyboardInterrupt:
            return -128
        except:
            print("Please enter valid ID !")

    # Call the adequate function
    if action == 0:
        rval = Decoder(script_path)
    elif action == 1:
        rval = Encoder(script_path)
    elif action == 2:
        rval = HelpMsg()

    # End line
    printSep()

    # End of the script
    return rval


# Call the main
if __name__ == "__main__":
    main()
