import re

source = open('TestCases.md', 'r')
lines = []
for line in source:
	lines.append(line)
source.close()



CB_start = re.compile("^```python#run(#\w*)*$");
CB_end = re.compile("^```$");

codeblocks = []

in_codeblock = False
cb_startline = 0
for i, line in enumerate(lines):
	if not in_codeblock:
		if CB_start.match(line):
			cb_startline = i+1
			in_codeblock = True
	else:
		if CB_end.match(line):
			codeblocks.append((cb_startline, i-1))
			in_codeblock = False

for i in codeblocks:
	print(i)

dest = open('Output.md', 'w')
for line in lines:
	dest.write(line)
dest.close()
