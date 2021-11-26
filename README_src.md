# execute.md
run code-blocks in markdown files and insert the results immediately below, like a home-brewed jupyter notebook.


- [x] basic functionality
- [ ] matplotlib support
- [ ] additional languages 


#### Usage:
**1.** Execute either with `./execute.py [SOURCE] [DEST]` or `./execute.py [SOURCE]` (in which case results will be output to stdout)

**2.** Use it in python
> ```python
> from execute import execute
> open('dest.md', 'w').writelines(execute(open('src.md', 'r'))) 
> ```
---

# Test Cases

##### A standard, unflagged codeblock
```
This should be ignored
```

##### A codeblock designed to be run
> The following block starts with
> ```
> '''python#run
> ```
```python#run
x = 5
y = 6
print(x+y)
```
The `#run` tag is stripped from the final output, leaving us with just a codeblock starting with `'''python`, followed by a second codeblock with output.

##### Shared interpreter demo
*Again, just done with `'''python#run`.*

```python#run
for i in range(4):
  x += 100
  y -= x

print(x-y)
```

##### Spinning up a new interpreter instance
This one uses one additional tag, now looking like `'''python#run#new`. Snazzy.
```python#run#new
print(x)
```

##### Unboxed output with `#unboxed`
```python#run#unboxed
print('This is a test of *various* **markdown** ~~features~~.')
```

##### Hidden input-field with `#hide`
The source code block here looks like the following:
> ```
> '''python#run#hide
> print(1+2)
> '''
> ```
However that gets dropped from the file in the course of processing, leaving us with just
```python#run#hide
print(1+2)
```

```python#run#hide#unboxed
infix = ', of course,'
print(f"These tags can{infix} be combined. Just look at this very sentence in [README_src.md](https://raw.githubusercontent.com/FraserLee/execute-dot-md/main/README_src.md) 😉")
```
