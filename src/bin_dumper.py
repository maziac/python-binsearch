
import sys

buffer = None



def read_file(filepath: str):
    """ Reads a file, allocates data and makes 'buffer' point to it. """
    global buffer
    buffer = open(filepath, 'rb')


def read_stdio():
	""" Reads from stdio, allocates data and makes 'buffer' point to it. """
#	stdin = sys.stdin
#    stdin_size = stdin.buffer.length
	global buffer
	buffer = sys.stdin.buffer

def dump(offset: int, size: int, writer):
    # TODO: 'writer' is probably unused
	"""
    Dumps out the contents of a slice of 'buffer' to 'output'.
	Arguments:
	 - 'offset' - The first byte to dump out.
	 - 'size' - The number of bytes to dump out.
	 - 'writer' - The destination to write to.
	"""
	global buffer
	if buffer is not None:
		len = buffer.length
		start = offset
		count = size
		if start < len:
			if start < 0:
				count += start
				start = 0
			if count > len - start:
				count = len - start
			end = start + count
			sys.stdout.write(buffer[start, end])


def parse_search_string(search_string: str) -> str:
	"""
    Parses the search string.
	A search string contains search characters but can also contain decimals
	or hex numbers.
	'search_string' - E.g. "a\\xFA,\\d7,bc\\d9"
	Returns: E.g. []u8{ 'a', 0xFA, 7, 'b', 'c', 9 }
    """
	search_bytes = ""
	slen = search_string.length
	i = 0

	while i < slen:
		c = search_string[i]
		if c == '\\':
			# Get next char
			i += 1;
			if i >= slen:
				raise Exception("Expected 'd' or 'x'.")
			c = search_string[i];
			# Check for \, decimal or hex
			if c == '\\':
				# The letter \
				search_bytes += c
			elif c == 'd' or c == 'x':
				# A decimal or hex will follow
				radix = 16
				if c == 'd':
					radix = 10
				# Find string until ','
				i += 1
				k = i
				while k < slen:
					if search_string[k] == ',':
						break
					k += 1
				# Check range
				if k == i:
					raise Exception("Expected a number.")
				# Now convert decimal value
				val = int(search_string[i,k], radix);
				search_bytes += val
				# Next
				i = k
			else:
				# Error
				raise Exception("Expected 'd' or 'x'.")
		else:
			# "Normal" letter
			search_bytes += c

		# Next
		i += 1

	return search_bytes



def search(offset: int, search_string: str) -> int:
	"""
    Searches a string in the buffer and changes the 'offset'.
	If the string is not found the buffer length is returned in 'offset'.
	A search string contains search characters but can also contain decimals
	or hex numbers.
	Arguments:
	'offset' - The offset to search from. The found offset is returned here.
	'search_string' - the search string.
	  E.g. "a\\xFA,\\d7,bc\\d9"
	Returns: The new offset.
    """
	global buffer
	if buffer is not None:
		# Parse search string
		search_bytes = parse_search_string(search_string)
		slen = search_bytes.length
		if slen > 0:
			blen = buffer.length
			offs = offset
			if offs < 0:
				offs = 0
			last = blen - slen + 1
			if offs <= last:
				# Loop all elements
				i = offs
				while i < last:
					# Binary compare
					if buffer[i, i+slen] == search_bytes:
						# Search bytes found
						return i
					# Next
					i += 1
				# Nothing found
			return blen
