# TemplateCreator
A simple python tool to create templates of folder and output a single independant file that can be executed on any system, without installing tools !

## How does it works ?
First, the tool read all files present on the folder, and once done, it seek for a "%#[variable]%#" delimiters. Any text between them will be subsituted with the variable name. For example, you can replace it with author name !

Then, it create a single batch / shell file to be executed on the target system, that will duplicate automatically the folder, and replace any variable with it's value. Usefull to duplicate folder and customize them in one click !

## Warning : 
Due to the fact that the data is stored into the script file, the tool isn't effective for large file. Even an image will output very large data !
