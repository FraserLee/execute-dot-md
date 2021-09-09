import re

# Regex expressions for identifying the start and end of code-blocks
CB_start = re.compile("^```python#run(#\w*)*$");
CB_end = re.compile("^```$");

# Extraction of blocks and lines from a file
lines = []
codeblocks = []

with open('TestCases.md', 'r') as source:
	in_codeblock = False
	cb_startline = 0
	for i, line in enumerate(source):

		lines.append(line)

		if not in_codeblock:
			if CB_start.match(line):
				cb_startline = i+1
				in_codeblock = True
		else:
			if CB_end.match(line):
				codeblocks.append((cb_startline, i-1))
				in_codeblock = False

# Execute each codeblock
for i in codeblocks:
	print(i)

# Output the results
with open('Output.md', 'w') as dest:
	for line in lines:
		dest.write(line)
