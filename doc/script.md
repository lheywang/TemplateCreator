# Script format
The script is done to be executable in place, without needing any external tool.
Thus, the usage of advanced features is impossible.

## How data is parsed ?
First, the tool read all of the file, in search of the delimiters. Theses will for now don't be replaced, they will on the target device, when the template will be used.

Then, we encode the data into base64 format. This is bigger than source, yes, but it prevent any issues relative to non handled characters, as well to hide a little bit the raw data. At the end, this is easier for us to do like that rather than printing whole files directly.

## How data is stored ?
Data is stored directly on the script file, thus creating a pretty bit archive. This may slow down very old systems, but won't affect any newer ones.
When executing the script, we dump the data into a temporary file to be parsed, decoded and then customized.