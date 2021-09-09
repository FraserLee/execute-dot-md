# Test

The rest of this should work fine as fairly standard markdown.

##### A standard unflagged codeblock
```python
This should be ignored
```

##### A codeblock designed to be run
> The following block starts with
> ```
> '''python#run
> ```
The most basic example:
```python#run
x = 5
y = 6
print(x+y)
```
`#run` is stripped from the final output, leaving us with just a codeblock starting with `'''python`, followed by a second codeblock with output.

##### Shared interpretor demo, also just with `#run`
```python#run
x += 100
print(x-y)
```

##### New interpretor demo (with `#run#new`)
```python#run
print(x)
```

##### Unboxed output with `#run#unboxed`
```python#run#unboxed
print('This is a test of *various* **markdown** ~~features~~.')
```

##### Hidden input after with `#run#hide`
The source code block here has a single line containing the statement `print('test')`.
```python#run#hide
print('test')
```

These tags can, of course, be combined.
