# TemplateCreator

A tool that can pack a folder with subfiles into an archive, which can be customized once extracted !
The script is OS agnostic, which means that the files will be created regardless of the OS, since they're
expressed internally as relative paths (strings).

## How does it works ?

Create a folder structure, with files that you're going to use as template.
When you want a word / phrase to be customized, add the tokens (by default ##) before and after it.

```
I'm getting ##customized##
```

Here, the word customized will be changed when extracted !
This also work if you have multiple variables in the same line.

The base file, which can contain the project name can be fully customized, including it's name !

All text files are supported (Tex, Py, Makefile...). Binary files are simply ignored, but replicated.

### Creating an archive :

Launch the tool, you will be asked to input a reference path to create. You then need to choose which file is
the "main", which will then be renamed.

Let the tool compute everything as needed, you'll end up with a data.template file on the root of the folder structure.

This archive can be renamed without any issues, it's even recommended ! You can have multiple archive in the same folder.

### Openning an archive

Place the archive in the folder where it will be expanded, and then, call the Python tool.
The tool will proceed to some safety check to ensure the file wasn't modified since creation, and then, will create files and
folder if needed.

You can then use any tool you want !

## Technicals details

Under the hood, some aspects are required to ensure the file will be correctly generated.
This include :

- Reading text files only
- Compressing data
- Computing an SHA3_512 hash of the data
- Write to file (using pickle module)

- ...

- Reading the template file
- Ensuring hash match
- Decompressing data
- Customizing files
- Outputing files.
