# binsearch

A binary search command line tool.
The tool allows you to specify one (or more files) and dump out values to stdout from a specific offset and for a specific size.
It is also possible to search for patterns to set the offset.

The output is written to stdout and can be redirected into a file or piped to another command.



# Usage

~~~bash
binsearch file1 [--offs #] [--search tokens] [--size #|all] [file2 [--offs #] ...]
~~~


- "**--help**": Prints the help.
- "**--version**": Prints the version number.
- "**--offs** offset": Offset from start of file. Moves last position. You can also move relatively by prefixing with + or -.
- "**--size** size": The number of bytes to output. Moves last position.
- "**--search** tokens": Searches for the first occurrence of the tokens. The search starts at last position. Tokens can be a decimal of hex number or a string. The search starts at last position.

## Examples

~~~
// Outputs the first 5 bytes:
binsearch file --size 5

// Outputs the bytes from position 10 to 109:
binsearch file --offs 10 --size 100

// Outputs the bytes from position 10 to 109, directly followed by 200 to 209:
binsearch file --offs 10 --size 100 --offs 200 --size 10

// Outputs the bytes from position 10 to 109, directly followed by 120 to 129:
binsearch file --offs 10 --size 100 --offs +10 --size 20

// Outputs 10 bytes from the first occurrence of 'abc':
binsearch file --search abc --size 10

// Outputs 10 bytes from the first occurrence of decimal number 130. Only bytes are searched:
binsearch file --search "\d130" --size 10

// Outputs 10 bytes from the first occurrence of hex number 0xFF. Only bytes are searched:
binsearch file --search "\xFF" --size 10

// Outputs 10 bytes from the first occurrence of the sequence 97,98,99,255,120,121,122,0. Only bytes are searched:
binsearch file --search "abc\xFF,xyz\d0" --size 10

// Searches for string "abc" followed by newline and outputs 10 bytes:
binsearch file --search "abc"\n --size 10
// or:
binsearch file --search abc\n --size 10

// Piping data in:
cat file | binsearch --size 5

// Piping data out:
binsearch file --size 5 | cat

// Saving to a file
binsearch file --size 5 > output.bin
~~~

Please note: when searching for a sequence of bytes, a 0 is **not** automatically added at the end.



# Development

TODO:
- tasks.json
  - to build
  - to run pyinstaller
- launch.json: depend on build


## Run

~~~bash
python3 src/main.py
~~~


## Build executable

~~~bash
pyinstaller src/main.py --onefile --name binsearch
~~~

Or through vscode's tasks.json "Create executable".

The binary is found at "dist/binsearch":


## Unit tests

To run unit tests use
~~~bash
python3 -m unittest  discover --start-directory src --pattern "test*.py" --verbose
~~~

Or run through vscode's unit test runner.

