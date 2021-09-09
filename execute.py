# import re
# import os
# 
# # Regex expressions for identifying the start and end of code-blocks
# block_start = re.compile("^```python#run(#\w=*)*$");
# block_end = re.compile("^```$");
# 
# # Define a structure to keep track of codeblocks
# class block:
# 	# include a language enum if extended later
# 	startline: int
# 	endline = None
# 	unboxed = False
# 	hide    = False
# 	new     = False
# 	def __init__(self, startline):
# 		self.startline = startline
# 		self.lines   = []
# 
# # Extraction of blocks and lines from a file
# lines = []
# codeblocks = []
# 
# with open('TestCases.md', 'r') as source:
# 	current_block = None
# 	for i, line in enumerate(source):
# 
# 		lines.append(line)
# 
# 		if current_block is None and block_start.match(line):
# 				current_block = block(i+1)
# 
# 		elif current_block is not None:
# 			if block_end.match(line):
# 				current_block.endline = i-1
# 				codeblocks.append(current_block)
# 				current_block = None
# 			else: current_block.lines.append(line)
# 
# # Execute each codeblock
# for i in codeblocks:
# 	print(i.startline, i.endline, i.lines)
# 
# # Output the results
# with open('Output.md', 'w') as dest:
# 	for line in lines:
# 		dest.write(line)

import sys
import subprocess
from threading  import Thread
from queue import Queue, Empty

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

proc = subprocess.Popen(['python3', '-i', '-q'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

qo = Queue()
to = Thread(target=enqueue_output, args=(proc.stdout, qo), daemon=True)
to.start()


qe = Queue()
te = Thread(target=enqueue_output, args=(proc.stderr, qe), daemon=True)
te.start()

lines = ["print(2+4)",
		"print('test 1')",
		"x=1",
		"print('test 2')",
		"print(y)",
		"print(200-x)"]

for line in lines:
	proc.stdin.write(f"{line.strip()}\n".encode("utf-8"))
	proc.stdin.flush()
	try:  line = qo.get(timeout=.1)
	except Empty:
		print('no output yet')
	else:
		print(line.decode('utf-8'), end='')

while True:
	try:  line = qe.get_nowait()
	except Empty:
		break
	else:
		print(line.decode('utf-8'), end='')

proc.stdin.close()
proc.terminate()
proc.wait(timeout=0.2)
