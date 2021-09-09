source = open('TestCases.md', 'r')
lines = []

for line in source:
	lines.append(line)

source.close()

dest = open('Output.md', 'w')
for line in lines:
	dest.write(line)
dest.close()
