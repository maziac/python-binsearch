from pathlib import Path

prg_version = "0.1.0"

import sys
from pathlib import Path


def args_help():
	sys.stdout.write("""Usage:
        --help: Prints this help.
        --version: Prints the version number.
        --offs offset: Offset from start of file. Moves last position. It is possible to use relative offset with the '+' or '-' sign. In that case the value is added to the current offset.
        --size size: The number of bytes to evaluate. Moves last position (offset:=offset+size).
        --search tokens: Searches for the first occurrence of tokens. Token can be a decimal of hex number or a string. The search starts at last position.
        Examples:
        - "binsearch file --offs 10 --size 100": Outputs the bytes from position 10 to 109.
        - "binsearch file --offs 10 --size 100 --offs 200 --size 10": Outputs the bytes from position 10 to 109, directly followed by 200 to 209.
        - "binsearch file --offs 10 --size 100 --offs +10 --size 20": Outputs the bytes from position 10 to 109, directly followed by 120 to 129.
        - "binsearch file --search abc --size 10": Outputs 10 bytes from the first occurrence of 'abc'.
        - "binsearch file --search "\d130" --size 10": Outputs 10 bytes from the first occurrence of decimal number 130. Only bytes are searched.
        - "binsearch file --search "\\xFF" --size 10": Outputs 10 bytes from the first occurrence of hex number 0xFF. Only bytes are searched.
        - "binsearch file --search "abc\\xFF,xyz\d0" --size 10": Outputs 10 bytes from the first occurrence of the sequence 97,98,99,255,120,121,122,0. Only bytes are searched.
        Please note: If searching for a sequence of bytes, the sequence is not automatically terminated by a 0.
        """)



# Loops through the passed arguments.
len = len(sys.argv)

i = 1	# Skip first (path)
while (i < len):
	# Get next arg
	arg = sys.argv[i]
	print(arg)

	# Parse arg
	if arg == "--help":
		args_help()
	elif arg == "--version":
		sys.stdout.write("Version " + prg_version + "\n");
	elif arg == "--offs":
		print(arg)
	elif arg == "--size":
		print(arg)
	else:
		# It is the filename (probably).
		# Open file:
		print(arg)

	# Next
	i += 1

#for entry in target_dir.iterdir():
#    print(entry.name)

