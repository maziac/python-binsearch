
import sys
import io
import bin_dumper


prg_version = b"0.1.0"


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


def get_nth_arg(n: int, args_array ) -> str|None:
	"""
	Returns the next argument in 'args_array' or an error if none exists.
	- 'n' - The index to get from the args_array.
	- 'args_array' - The array of strings.
	Returns: The string at 'n' or None if out of range.
	"""
	if n >= len(args_array):
		return None
	arg = args_array[n]
	return arg


def parse_args(args_array: [str], writer: io.BufferedIOBase):
	"""
	Loops through the passed arguments and executes them.
	- 'args_array' - the array with arguments
	- 'writer' - The writer object (stdout)
	"""
	offs = 0
	arg_len = len(args_array)

	i = 1	# Skip first (path)
	while i < arg_len:
		# Get next arg
		arg = args_array[i]

		# Parse arg
		if arg == "--help":
			args_help()
		elif arg == "--version":
			writer.write(b"Version " + prg_version + b"\n");
		elif arg == "--offs":
			# Get next arg
			i += 1
			o = get_nth_arg(i, args_array)
			if o is None:
				raise Exception("Expected an offset value.")
			# Check value
			if (o[0] == '+') or (o[0] == '-'):
				offs += int(o)
			else:
				offs = int(o)
		elif arg == "--size":
			# Get next arg
			i += 1
			s = get_nth_arg(i, args_array)
			if s is None:
				raise Exception("Expected a size value.")
			# Check for max
			size = sys.maxsize
			if s != "all":
                # It's not "all":
				size = int(s)
			bin_dumper.dump(offs, size, writer)
			offs += size
		elif arg == "--search":
			# Get next arg
			i += 1
			s = get_nth_arg(i, args_array)
			if s is None:
				raise Exception("Expected a value sequence to search for.")
			offs = bin_dumper.search(offs, s)
		else:
			# It is the filename (probably).
			# Open file:
			bin_dumper.read_file(arg)

		# Next
		i += 1

