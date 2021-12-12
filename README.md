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
```python
def f(x):
  if x <= 1: return 1
  return x * f(x-1)

print([f(x) for x in range(6)])
```
```
[1, 1, 2, 6, 24, 120]
```
The `#run` tag is stripped from the final output, leaving us with just a codeblock starting with `'''python`, followed by a second codeblock with output.

##### Shared interpreter demo
*Again, just done with `'''python#run`.*

```python
print(f(10))
```
```
3628800
```

##### Spinning up a new interpreter instance
This one uses one additional tag, now looking like `'''python#run#new`. Snazzy.
```python
print(f(11))
```
```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
NameError: name 'f' is not defined
```

##### Unboxed output with `#unboxed`
```python
print('This is a test of *various* **markdown** ~~features~~.')
```

This is a test of *various* **markdown** ~~features~~.


##### Hidden input-field with `#hide`
The source code block here looks like the following:
> ```
> '''python#run#hide
> print(1+2)
> '''
> ```
However that gets dropped from the file, leaving us with just
```
3
```


These tags can, of course, be combined. Just look at this very sentence in [README_src.md](https://raw.githubusercontent.com/FraserLee/execute-dot-md/main/README_src.md) 😉


# Other Languages

#### c

```c
#include <stdio.h>
#include <math.h>
int main() {
    float x = 5.0;
    float y = 0.4;
    printf("%f\n", sqrt(x*y));
    return 0;
}
```
```
1.414214
```

```c
#include <stdio.h>
int main() {
    this is a syntax error
}
```
```
<stdin>:3:5: error: use of undeclared identifier 'this'
    this is a syntax error
    ^
1 error generated.
```


