#!/usr/bin/python3
import re
import os
import sys
import subprocess
from threading import Thread
from queue import Queue, Empty


# <SUBPROCESS MANAGEMENT>
def init_interpereter():
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

def end_interpreter(proc):
	proc.stdin.close()
	proc.terminate()
	proc.wait(timeout=0.2)
# </SUBPROCESS MANAGEMENT>


# <REGEX DEFINITIONS>
# identifying the start and end of code-blocks
block_start = re.compile("^```python#run([#\w=]*)*$")
block_end = re.compile("^```$")

block_unboxed = re.compile(".*#unboxed")
block_new = re.compile(".*#new")
block_hide = re.compile(".*#hide")

stderr_start = re.compile("^(>>> )+")
# </REGEX DEFINITIONS>


# <MAIN PROCESS>
class block:
	"""Represents a code-block, tracking relevant features"""

	# include a language enum here if extended later
	startline: int
	endline = None
	unboxed = False
	hide    = False
	new     = False
	def __init__(self, startline):
		self.startline = startline
		self.lines   = []

def execute(source_lines):
	""" Execute a markdown file

	Input: Something that can be enumerated over to give strings representing lines
	 - eg. A file object, a list of strings, etc.
	Output: A list of strings, the resulting file.
	"""

	# <PARSING>
    # Extraction of blocks and lines from a file
	lines = []
	codeblocks = []

	global block
	current_block = None
	for i, line in enumerate(source_lines):

		lines.append(line)

		if current_block is None and block_start.match(line):
			current_block = block(i+1)
			#check for extra optional flags
			current_block.unboxed = bool(block_unboxed.match(line))
			current_block.new     = bool(block_new.match(line))
			current_block.hide    = bool(block_hide.match(line))

		elif current_block is not None:
			if block_end.match(line):
				current_block.endline = i-1
				codeblocks.append(current_block)
				current_block = None
			else: current_block.lines.append(line)
	#</PARSING>


	#<EXECUTION>
	# Setup execution environment
	(proc, queue_out, queue_err) = init_interpereter()

	# Execute each codeblock
	for block in codeblocks:
		#  print(block.startline, block.endline, block.lines)

		if block.new:
			end_interpreter(proc)
			(proc, queue_out, queue_err) = init_interpereter()

		# Get stdout
		stdout = ""
		for line in block.lines:
			proc.stdin.write(line.encode("utf-8"))
			proc.stdin.flush()
			# This line is by far the jankiest part of the current way of doing things. Instead of properly determining whether 
			# the interpreter has output something or is just waiting for input, we just wait .1 seconds and if nothing new has
			# printed we assume it's probably safe to enter the next line. I know, it sucks, I'll fix it later.
			try:  line = queue_out.get(timeout=.1)
			except Empty: pass
			else: stdout += line.decode('utf-8')
		# Get stderr
		stderr = ""
		while True:
			try:  line = queue_err.get_nowait()
			except Empty: break
			else: stderr += line.decode('utf-8')

		# Reformat file
		lines[block.startline-1] = "```python\n"
		if block.hide:
			for i in range(block.startline-1, block.endline+2): lines[i]=""

		if block.unboxed:
			if len(stdout)>0: lines[block.endline+1] +=    f"\n{stdout}\n"
		else:
			if len(stdout)>0: lines[block.endline+1] += f"```\n{stdout}```\n"
		# (strips the line-prompts from stderr)


		stderr=re.sub(stderr_start,'',stderr)
		if len(stderr)>0:lines[block.endline+1] += f"```\n{stderr}```\n"
		# #hide implementation
	end_interpreter(proc)

	#</EXECUTION>

	return lines
# </MAIN PROCESS>


# <CLI INVOCATION>
if __name__ == '__main__':
	with open(sys.argv[1], 'r') as source:
		result = execute(source)
		# Output the results
		if len(sys.argv) == 3:
			with open(sys.argv[2], 'w') as dest:
				for line in result:
					dest.write(line)
		else:
			for line in result:
				print(line, end='')
# </CLI INVOCATION>
