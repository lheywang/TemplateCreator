# -------------------------------------------------------------------------------
#   gui-helper.py : A file that create some helper functions to handle IO
#                   within the GUI context
#
#   l.heywang
#   08-05-2025
#
# -------------------------------------------------------------------------------


def guiprint(h_GUI, mode, verbose, verbose_threshold, message):
    """
    guiprint :  Define a print method that handle the nasty stuff for us about
                the print redirection for the GUI or console mode.

        Arguments :
            h_GUI :                 self argument of the GUI class
            mode :                  Mode of the GUI : 0 = console, 1 = GUI
            verbose :               Level of verbose : 0 = LOW, 1 = medium, 2 = high.
            verbose_threshold :     Minimal level of verbose to trigger the print
            message :               The printed message

        Returns :
            None
    """

    if mode == 0:
        # Console print

        if verbose > verbose_threshold:
            # Trigger the print

            print(message)

    elif mode == 1:
        # GUI prints

        if verbose > verbose_threshold:
            # Trigger the GUI pop up

            h_GUI.OpenInfoPopUp(message)

    return


def guiinput(h_GUI, mode, message):
    """
    guiinput :  Define an input method that handle the redirection into the GUI
                or the console.

        Arguments :
            h_GUI :     Handle to the gui (self)
            mode :      Mode of print : 0 = console, 1 = GUI
            message :   Message to be asked to the user before input

        Returns :
            input (str)
    """

    if mode == 0:
        # Console

        rval = input(message)

    elif mode == 1:
        # GUI

        rval = h_GUI.OpenAskPopUp(message)

    return rval
