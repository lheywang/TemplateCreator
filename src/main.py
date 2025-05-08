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

# Main file
if __name__ == "__main__":
    # Welcome message
    printHome()

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
        except:
            print("Please enter valid ID !")

    # Call the adequate function
    if action == 0:
        rval = Decoder()
    elif action == 1:
        rval = Encoder()
    elif action == 2:
        rval = HelpMsg()

    # End line
    printSep()

    # End of the script
    exit(rval)
