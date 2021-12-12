#!/usr/bin/python3
import re
import sys
import os
import subprocess
from dataclasses import dataclass, field

# <SUBPROCESS MANAGEMENT>
# siloing this code off so I can implement language-specific subprocess processes later
def subp_run(code, lang):
    if lang == 'python':
        return subprocess.run(['python3', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif lang == 'c':
        comp_p = subprocess.run(['gcc', '-x', 'c', '-o', 'a.out', '-', '-lm'], input=code.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if comp_p.returncode != 0:
            return comp_p
        run_p = subprocess.run(['./a.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove('a.out')
        return run_p
    return None
# </SUBPROCESS MANAGEMENT>


# <REGEX DEFINITIONS>
# identifying the start and end of code-blocks
block_start   = re.compile("^```(python|c)#run( *#\w*( *= *[\w.]*)?)*$")
block_end     = re.compile("^```$")

block_unboxed = re.compile(".*#unboxed")
block_new     = re.compile(".*#new")
block_hide    = re.compile(".*#hide")
# </REGEX DEFINITIONS>

# <MAIN PROCESS>
@dataclass
class block:
    """Represents a code-block, tracking relevant features"""
    lang: str

    startline: int
    endline: int = None

    unboxed = False
    hide    = False
    new     = False

    lines: list = field(default_factory = list)

def execute(source_lines):
    """ Execute a markdown file

    Input: Something that can be enumerated over to give strings representing lines
        (A file object, a list of strings, etc)
    Output: A list of strings, the resulting file.
    """

    # <PARSING>
    # Extraction of codeblocks and lines from a file
    lines = []
    codeblocks = []

    global block
    current_block = None
    for i, line in enumerate(source_lines):

        lines.append(line)

        # if we're not in a block, check if we're starting one
        if current_block is None and (match := block_start.match(line)):
            current_block = block(lang = match.group(1), startline = i+1)
            #check for extra optional flags
            current_block.unboxed = bool(block_unboxed.match(line))
            current_block.new     = bool(block_new.match(line))
            current_block.hide    = bool(block_hide.match(line))

        # if we're in one, check if we're ending
        elif current_block is not None:
            if block_end.match(line):
                current_block.endline = i-1
                codeblocks.append(current_block)
                current_block = None
            else: current_block.lines.append(line)
    #</PARSING>


    #<EXECUTION>

    # lang dicts
    prior_code = {}
    prior_output = {}

    # Execute each codeblock
    for block in codeblocks:
        #  print(block.startline, block.endline, block.lines)

        # Runs the block in what'll seem like a shared interpreter by 
        # concatenating prior code, then removing output shared with prior runs.
        lang = block.lang
        if block.new or not lang in prior_code:
            prior_code[lang] = prior_output[lang] = ''

        prior_code[lang] += ''.join(block.lines)
        proc = subp_run(prior_code[lang], lang)
        stdout = proc.stdout.decode('utf-8') + proc.stderr.decode('utf-8')
        for char in prior_output[lang]: # a bit of a hack, but it works (for deterministic output)
            if stdout[0] == char:
                stdout = stdout[1:]
            else: break

        prior_output[lang] += stdout
        if proc.returncode != 0:
            del prior_code[lang]
            del prior_output[lang]

        # Reformat file
        lines[block.startline-1] = f'```{block.lang}\n'
        if block.hide:
            for i in range(block.startline-1, block.endline+2): lines[i] = ""

        if len(stdout) > 0 and stdout[-1] != '\n': stdout += '\n'

        if block.unboxed:
            if len(stdout)>0: lines[block.endline+1] += f"\n{stdout}\n"
        else:
            if len(stdout)>0: lines[block.endline+1] += f"```\n{stdout}```\n"
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
