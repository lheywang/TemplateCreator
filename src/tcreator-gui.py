# -------------------------------------------------------------------------------
#   tcreator-gui :  Code for the command "tcreator", charged open the
#                   GUI interface for the user.
#   l.heywang
#   11-05-2025
#
# -------------------------------------------------------------------------------

# Module import
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sv_ttk
from PIL import Image, ImageTk
import pathlib


class TkGUI(tk.Tk):
    def __init__(self):
        """
        Initialize the tkGUI class and create basic parameters
        """
        # Parent constructor
        super().__init__()

        # Create the main window
        self.title("Template Editor")
        self.geometry("600x400")  # Removed initial size, will use resizable

        # Define grid (row)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Define grid (column)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # Create elements
        self.elements = dict()
        self.images = dict()
        self.images_obj = dict()

        # Get path of actual file
        self.act_folder = pathlib.Path(__file__).parent
        img_path = self.act_folder / pathlib.Path("gui/logo_256.png")

        # Load images
        self.images_obj["Logo"] = ImageTk.PhotoImage(Image.open(img_path))

        # Labels
        self.elements["Logo"] = tk.Label(self, image=self.images_obj["Logo"])
        self.elements["Logo"].grid(
            row=0,
            column=0,
            sticky="nswe",
        )
        self.elements["Name"] = tk.Label(self, text="Template Creator.")
        self.elements["Name"].grid(
            row=0,
            column=1,
            columnspan=2,
            sticky="nswe",
        )

        # Buttons
        self.elements["Button1"] = tk.Button(
            self,
            text="Open .template file",
            command=self.load_template_file,
        )
        self.elements["Button1"].grid(
            row=1,
            column=1,
            columnspan=2,
            sticky="wne",
        )
        self.elements["Button2"] = tk.Button(
            self,
            text="Write .template file",
            command=self.write_template_file,
        )
        self.elements["Button2"].grid(
            row=2,
            column=1,
            columnspan=2,
            sticky="wne",
        )

        sv_ttk.set_theme("light")
        return

    def Run(self):
        """
        Run the GUI
        """
        self.mainloop()
        return 0

    def load_template_file(self):
        """
        Function to handle the "Load .template file" button click.
        Opens a file dialog and prints the selected file path.
        """
        filepath = filedialog.askopenfilename(
            title="Load .template file",
            filetypes=[("Template Files", "*.template"), ("All Files", "*.*")],
        )
        if filepath:  # Check if a file was selected (not cancelled)
            print(f"Loading template file: {filepath}")
            #  Add your logic to load the template file here
        else:
            print("Load Template action cancelled.")
        return

    def write_template_file(self):
        """
        Function to handle the "Write .template file" button click.
        Opens a file dialog to choose where to save the file.
        """
        filepath = filedialog.asksaveasfilename(
            title="Write .template file",
            defaultextension=".template",
            filetypes=[("Template Files", "*.template"), ("All Files", "*.*")],
        )
        if filepath:
            print(f"Writing template file to: {filepath}")
            # Add your logic to write the template file here
        else:
            print("Write Template action cancelled.")
        return


if __name__ == "__main__":
    GUI = TkGUI()
    GUI.Run()
