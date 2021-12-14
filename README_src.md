# execute.md
run code-blocks in markdown files and insert the results immediately below, like a home-brewed jupyter notebook.


- [x] basic functionality
- [x] additional languages
- [ ] matplotlib support


#### Usage:

Either

**1.** execute with `./execute_md.py [SOURCE] [DEST]` or `./execute_md.py [SOURCE]` (which will print results to stdout), or

**2.** use it through python (or whatever you want to FFI that to)
> ```python
> from execute_md import execute_md
> open('dest.md', 'w').writelines(execute_md(open('src.md', 'r'))) 
> ```
---

# Test Cases

##### A standard, unflagged codeblock
```
This'll be ignored
```

##### A codeblock designed to be run
> The following block starts with
> ```
> '''python#run
> ```
```python#run
def f(x):
  if x <= 1: return 1
  return x * f(x-1)

print([f(x) for x in range(6)])
```
The `#run` tag is stripped from the final output, leaving us with just a codeblock starting with `'''python`, followed by a second codeblock with output.

##### Shared interpreter demo
*Again, just done with* `'''python#run`.

```python#run
print(f(10))
```

##### A new interpreter instance
This one uses one additional tag, now looking like `'''python#run#new`. Snazzy.
```python#run#new
print(f(11))
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
However that gets dropped from the file, leaving us with just
```python#run#hide
print(1+2)
```

```python#run#hide#unboxed
infix = ', of course,'
print(f"These tags can{infix} be combined. Just look at this very sentence in [README_src.md](https://raw.githubusercontent.com/FraserLee/execute-dot-md/main/README_src.md) 😉")
```

# Languages

# :crab: rust :crab:
```rust#run
!req(languages/rust_example1.rs)
```

```rust#run#new
!req(languages/rust_example2.rs)
```

# :snake: python :snake:
```python#run
print(2+2)
```

# c
```c#run
!req(languages/c_example.c)
```

## c++
```cpp#run
!req(languages/cpp_example.cpp)
```

# bash :shell:
```bash#run
!req(languages/bash_example.sh)
```

# go
```go#run
!req(languages/go_example.go)
```

# JS :yellow_square:
```js#run
!req(languages/js_example.js)
```

# Lua
```lua#run
!req(languages/lua_example.lua)
```
