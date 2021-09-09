import re
import os
import sys
import subprocess
from threading import Thread
from queue import Queue, Empty

# Regex expressions for identifying the start and end of code-blocks
block_start = re.compile("^```python#run([#\w=]*)*$");
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

# Setup execution environment
proc      = None
queue_out = None
queue_err = None

def end_interpreter():
	proc.stdin.close()
	proc.terminate()
	proc.wait(timeout=0.2)

def init_interpereter():
	global proc
	global queue_out
	global queue_err

	if proc is not None:
		end_interpreter()

	def enqueue_output(out, queue):
		for line in iter(out.readline, b''):
			queue.put(line)
		out.close()


	proc = subprocess.Popen(['python3', '-i', '-q'],
							stdin =subprocess.PIPE,
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE)

	queue_out  = Queue()
	thread_out = Thread(target=enqueue_output, args=(proc.stdout, queue_out), daemon=True)
	thread_out.start()

	queue_err  = Queue()
	thread_err = Thread(target=enqueue_output, args=(proc.stderr, queue_err), daemon=True)
	thread_err.start()

	return (proc, queue_out, queue_err)

# Execute each codeblock
init_interpereter()

for block in codeblocks:
	if block.new:
		init_interpereter()
	print(block.startline, block.endline, block.lines)

	for line in block.lines:
		proc.stdin.write(f"{line.strip()}\n".encode("utf-8"))
		proc.stdin.flush()
		try:  line = queue_out.get(timeout=.1)
		except Empty: pass
		else:
			print(line.decode('utf-8'), end='')

	while True:
		try:  line = queue_err.get_nowait()
		except Empty: break
		else:
			print(line.decode('utf-8'), end='')

end_interpreter()
# Output the results
with open('Output.md', 'w') as dest:
	for line in lines:
		dest.write(line)


