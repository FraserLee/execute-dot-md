# execute.md
run code-blocks in markdown files and insert the results immediately below, like a home-brewed jupyter notebook.

execute either with `./execute.py [SOURCE] [OUTPUT]` or `./execute.py [SOURCE]` (in which case results will be output to the terminal).

[ ] basic functionality
[ ] matplotlib support
[ ] additional languages 


---

# Test Cases

##### A standard unflagged codeblock
```python
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
`#run` is stripped from the final output, leaving us with just a codeblock starting with `'''python`, followed by a second codeblock with output.

##### Shared interpreter demo, also just done with `'''python#run`
```python#run
x += 100
print(x-y)
```

##### Spinning up a new interpreter instance (with `'''python#run#new`)
```python#run#new
print(x)
```

##### Unboxed output with `'''python#run#unboxed`
```python#run#unboxed
print('This is a test of *various* **markdown** ~~features~~.')
```

##### Hidden input-field, though with `#hide`
The source code block here looks like the following:
> ```
> '''python#run#hide
> print(1+2)
> '''
> ```
However that was removed from the file, leaving us just with
```python#run#hide
print(1+2)
```

```python#run#hide#unboxed
infix = ', of course,'
print(f"These tags can{infix} be combined.")
```
