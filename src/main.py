import os
import sys
import bin_dumper
import args


# MAIN:
# Read in the stdin (in case data is piped)
bin_dumper.read_stdio()

# Parse arguments
with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout:
	args.parse_args(sys.argv, stdout);
