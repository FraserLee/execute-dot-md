import re
import os

# Regex expressions for identifying the start and end of code-blocks
block_start = re.compile("^```python#run(#\w*)*$");
block_end = re.compile("^```$");

# Define a structure to keep track of codeblocks
class block:
	# include a language enum if extended later
	startline: int
	endline = None
	unboxed = False
	hide    = False
	new     = False
	def __init__(self, startline):
		self.startline = startline
		self.lines   = []

# Extraction of blocks and lines from a file
lines = []
codeblocks = []

with open('TestCases.md', 'r') as source:
	current_block = None
	for i, line in enumerate(source):

		lines.append(line)

		if current_block is None and block_start.match(line):
				current_block = block(i+1)

		elif current_block is not None:
			if block_end.match(line):
				current_block.endline = i-1
				codeblocks.append(current_block)
				current_block = None
			else: current_block.lines.append(line)

# Execute each codeblock
for i in codeblocks:
	print(i.startline, i.endline, i.lines)

# Output the results
with open('Output.md', 'w') as dest:
	for line in lines:
		dest.write(line)
