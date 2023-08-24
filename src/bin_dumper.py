
import io
import os
import sys


buffer = None


def read_file(filepath: str):
	""" Reads a file, allocates data and makes 'buffer' point to it. """
	global buffer
	buffer = None	# Just in case an exception is catched
	file = open(filepath, 'rb')
	buffer = file.read()
	file.close()


def read_stdio():
	""" Reads from stdio, allocates data and makes 'buffer' point to it. """
	global buffer
	# Check if data is available (if not read would block)
	if os.isatty(0) == False:
		buffer = sys.stdin.buffer.read()


def dump(offset: int, size: int, writer: io.BufferedIOBase):
	"""
    Dumps out the contents of a slice of 'buffer' to 'output'.
	Arguments:
	 - 'offset' - The first byte to dump out.
	 - 'size' - The number of bytes to dump out.
	 - 'writer' - The destination to write to.
	"""
	global buffer
	if buffer is not None:
		blen = len(buffer)
		start = offset
		count = size
		if start < blen:
			if start < 0:
				count += start
				start = 0
			if count > blen - start:
				count = blen - start
			end = start + count
			writer.write(buffer[start:end])


def parse_search_string(search_string: str) -> bytes:
	"""
    Parses the search string.
	A search string contains search characters but can also contain decimals
	or hex numbers.
	'search_string' - E.g. "a\\xFA,\\d7,bc\\d9"
	Returns: a string with \\ converted to a number
	"""
	search_bytes = b""
	slen = len(search_string)
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
				search_bytes += bytes(c, 'ascii')
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
				val = int(search_string[i:k], radix)
				search_bytes += val.to_bytes(1, 'little')
				# Next
				i = k
			else:
				# Error
				raise Exception("Expected 'd' or 'x'.")
		else:
			# "Normal" letter
			search_bytes += bytes(c, 'ascii')

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
	if buffer is None:
		return offset
	# Parse search string
	search_bytes = parse_search_string(search_string)
	slen = len(search_bytes)
	if slen == 0:
		return offset
	blen = len(buffer)
	offs = offset
	if offs < 0:
		offs = 0
	last = blen - slen + 1
	if offs <= last:
		# Loop all elements
		i = offs
		while i < last:
			# Binary compare
			if buffer[i:i+slen] == search_bytes:
				# Search bytes found
				return i
			# Next
			i += 1
		# Nothing found
	return blen
