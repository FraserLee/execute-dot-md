#!/usr/bin/python3
import re
import sys
import os
import subprocess
from dataclasses import dataclass, field

# <REGEX DEFINITIONS>
# identifying the start, end, and properties of code-blocks
block_start   = re.compile("^```(" \
        "python|lua|js|javascript|bash|zsh|brainfuck" \
        "|c|rust|cpp|c\+\+|go|java|kotlin|kts|haskell|hs" \
    ")#run( *#\w*( *= *[\w.]*)?)*$")
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

    # this syntax makes the list of lines instance specific
    # (other fields are python's equivalent of primitives)
    lines: list = field(default_factory = list)

def execute_md(source_lines):
    """ Execute a markdown file

    Input: Something that can be enumerated over to give strings representing lines
        (A file object, a list of strings, etc)
    Output: A list of strings, the resulting file.
    """

    # <PARSING>
    # extract codeblocks and lines from a file
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
        # otherwise just add the line the current block
            else: current_block.lines.append(line)
    #</PARSING>


    #<EXECUTION>

    # key: language of codeblock
    prior_code = {}
    prior_output = {}

    for block in codeblocks:
        # runs blocks in what'll seem like a shared interpreter by 
        # concatenating prior code, then removing output shared with prior runs.
        #
        # it's a bit of a hack, but it works fine for deterministic code.
        if block.new or not block.lang in prior_code:
            prior_code[block.lang]   = ''
            prior_output[block.lang] = ''
        prior_code[block.lang] += ''.join(block.lines)

        proc = subp_run(prior_code[block.lang], block.lang)
        stdout = proc.stdout.decode('utf-8') + proc.stderr.decode('utf-8')

        # remove shared output with prior runs (unoptimized, potential future bottleneck)
        for char in prior_output[block.lang]:
            if stdout[0] == char:
                stdout = stdout[1:]
            else: break

        prior_output[block.lang] += stdout
        if proc.returncode != 0:
            del prior_code[block.lang]
            del prior_output[block.lang]

        # Reformat file to insert results
        lines[block.startline-1] = f'```{block.lang}\n'
        if len(stdout) > 0 and stdout[-1] != '\n': stdout += '\n'
        if block.hide:
            for i in range(block.startline-1, block.endline+2): lines[i] = ""
        if block.unboxed:
            if len(stdout)>0: lines[block.endline+1] += f"\n{stdout}\n"
        else:
            if len(stdout)>0: lines[block.endline+1] += f"```\n{stdout}```\n"
    #</EXECUTION>

    return lines

# </MAIN PROCESS>

# <SUBPROCESS MANAGEMENT>
# siloing everything language-specific in execution to this one section
def subp_run(code, lang):
    lang = { # re-map languages with multiple names
        'javascript' : 'js',
        'c++'        : 'cpp',
        'kts'        : 'kotlin',
        'hs'         : 'haskell',
    }.get(lang, lang)
    # interpreted languages
    if lang == 'python'  or \
       lang == 'js'      or \
       lang == 'lua'     or \
       lang == 'kotlin'  or \
                            \
       lang == 'bash'    or \
       lang == 'zsh'     or \
                            \
       lang == 'brainfuck':
        return subprocess.run({
            'python'    : ['python3',   '-c', code],
            'js'        : ['node',      '-e', code],
            'lua'       : ['lua',       '-e', code],
            'kotlin'    : ['kotlin',    '-e', code],

            'bash'      : ['bash',      '-c', code],
            'zsh'       : ['zsh',       '-c', code],

            'brainfuck' : ['brainfuck', '-e', code],
            }[lang], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # compiled languages
    elif lang == 'rust' or \
         lang == 'c'    or\
         lang == 'cpp':
        comp_p = subprocess.run({
            'rust' : ['rustc',            '-o', '.temp.out', '-'],
            'c'    : ['gcc', '-x', 'c',   '-o', '.temp.out', '-', '-lm'],
            'cpp'  : ['g++', '-x', 'c++', '-o', '.temp.out', '-', '-lm'],
            'c++'  : ['g++', '-x', 'c++', '-o', '.temp.out', '-', '-lm'],
            }[lang], input=code.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # if compilation's failed, return that so we can print the error
        if comp_p.returncode != 0: return comp_p
        # run the compiled code
        run_p = subprocess.run(['./.temp.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove('.temp.out')
        return run_p

    # languages that need code written to a file
    elif lang == 'go'      or \
         lang == 'haskell' or \
         lang == 'java':
        with open(src_file:={
            'go'      : 'temp.go',
            'haskell' : 'temp.hs',
            'java'    : 'temp.java',
            }[lang], 'w') as f: f.write(code)

        run_p = subprocess.run({
            'go'   : ['go', 'run',  src_file],
            'haskell' : ['runhaskell', src_file],
            'java' : ['java',       src_file],
            }[lang], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove(src_file)
        return run_p

    # this shouldn't happen unless the regex covers cases that've been missed here.
    else: raise Exception(f'Language {lang} not implemented')
# </SUBPROCESS MANAGEMENT>

# <CLI INVOCATION>
if __name__ == '__main__':
    with open(sys.argv[1], 'r') as source:

        result = execute_md(source)

        if len(sys.argv) == 3: # output to file
            with open(sys.argv[2], 'w') as dest:
                for line in result:
                    dest.write(line)
        else:                  # output to stdout
            for line in result:
                print(line, end='')
# </CLI INVOCATION>
