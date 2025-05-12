# -------------------------------------------------------------------------------
#   tcreator-gui :  Code for the command "tcreator", charged open the
#                   GUI interface for the user.
#   l.heywang
#   11-05-2025
#
# -------------------------------------------------------------------------------

# Module import
import tkinter as tk
import sv_ttk
import pathlib
import sys
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog

# Function import
from funcs.decoder import Decoder
from funcs.encoder import Encoder


class TkGUI(tk.Tk):
    def __init__(self):
        # Parent constructor
        super().__init__()

        # Create the main window
        self.title("Template Editor")
        self.geometry("400x400")  # Removed initial size, will use resizable

        # Define grid (row)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Row
        self.grid_columnconfigure(0, weight=1)

        # Create elements
        self.elements = dict()
        self.images = dict()
        self.images_obj = dict()

        # Get path of actual file
        self.act_folder = pathlib.Path(__file__).parent
        img_path = self.act_folder / pathlib.Path("gui/logo_128.png")

        # Load images
        self.images_obj["Logo"] = ImageTk.PhotoImage(Image.open(img_path))

        # Labels
        self.elements["Logo"] = ttk.Label(
            self,
            image=self.images_obj["Logo"],
            text="Template Creator",
            compound=tk.LEFT,
        )
        self.elements["Logo"].grid(
            row=0,
            column=0,
            sticky="nswe",
        )

        # Buttons
        self.elements["Button1"] = ttk.Button(
            self,
            text="Open .template file",
            command=self.load_template_file,
        )
        self.elements["Button1"].grid(
            row=1,
            column=0,
            sticky="wne",
        )
        self.elements["Button2"] = ttk.Button(
            self,
            text="Write .template file",
            command=self.write_template_file,
        )
        self.elements["Button2"].grid(
            row=2,
            column=0,
            sticky="wne",
        )

        # Apply a theme to it
        sv_ttk.set_theme("light")
        return

    def Run(self):
        self.mainloop()
        return 0

    def load_template_file(self):
        # Ask for a file path
        filepath = filedialog.askopenfilename(
            title="Load .template file",
            filetypes=[("Template Files", "*.template"), ("All Files", "*.*")],
        )
        if not filepath:
            return

        # First, ask target folder
        folderpath = filedialog.askdirectory(
            title="Select the folder where the archive must be expanded",
            mustexist=True,
        )
        if not folderpath:
            return

        # Call the decoding function...
        rval = Decoder(
            filepath,
            False,
            0,
            folderpath,
            self,
            1,
        )

        return rval

    def write_template_file(self):

        # First, ask target folder
        folderpath = filedialog.askdirectory(
            title="Select a folder that need to be transformed as a template",
            mustexist=True,
        )
        if not folderpath:
            return

        # Then, ask the base file
        filepath = filedialog.askopenfilename(
            title="Select the base file of the template",
            filetypes=[("All Files", "*.*")],
            initialdir=folderpath,
        )
        if not filepath:
            return

        # Finally, ask for the write file emplacement :
        outputpath = filedialog.asksaveasfilename(
            title="Write .template file",
            defaultextension=".template",
            filetypes=[("Template Files", "*.template"), ("All Files", "*.*")],
            initialdir=folderpath,
        )
        if not outputpath:
            return

        # Finally, call the encoding function
        rval = Encoder(
            folderpath,
            filepath,
            "##",
            0,
            "project",
            outputpath,
            self,
            1,
        )

        return rval

    def OpenInfoPopUp(self, message):
        # Create a pop up :
        top = tk.Toplevel(self)
        top.geometry("400x400")
        top.title("Info :")

        # Configure the grid on the child
        # columns
        top.grid_columnconfigure(0, weight=1)

        # rows
        top.grid_rowconfigure(0, weight=1)
        top.grid_rowconfigure(1, weight=1)

        # Create elements
        msg = ttk.Label(top, text=message, wraplength=360)
        msg.grid(row=0, column=0, sticky="NSWE")
        bp = ttk.Button(top, text="OK", command=top.destroy)
        bp.grid(row=1, column=0, sticky="NSWE")

        # Wait for the pop up to be closed
        top.wait_window()
        return

    def OpenAskPopUp(self, message):
        # Create a pop up :
        top = tk.Toplevel(self)
        top.geometry("400x400")
        top.title("Enter info ?")

        # Create text container
        out = tk.StringVar()

        # Configure the grid on the child
        # columns
        top.grid_columnconfigure(0, weight=1)

        # rows
        top.grid_rowconfigure(0, weight=1)
        top.grid_rowconfigure(1, weight=1)
        top.grid_rowconfigure(2, weight=1)

        # Create elements
        msg = ttk.Label(top, text=message, wraplength=360)
        msg.grid(
            row=0,
            column=0,
            sticky="NSWE",
            padx=20,
            pady=20,
        )
        text = ttk.Entry(top, textvariable=out, justify=tk.CENTER)
        text.grid(
            row=1,
            column=0,
            sticky="NSWE",
            padx=20,
            pady=20,
        )
        bp = ttk.Button(top, text="OK", command=top.destroy)
        bp.grid(
            row=2,
            column=0,
            sticky="NSWE",
            padx=20,
            pady=20,
        )

        # Wait for the pop up to be closed
        top.wait_window()
        return out.get()


if __name__ == "__main__":
    GUI = TkGUI()
    GUI.Run()
    sys.exit(0)
