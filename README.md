# execute.md
run code-blocks in markdown files and insert the results immediately below, like a home-brewed jupyter notebook.


- [x] basic functionality
- [x] additional languages
- [ ] matplotlib support (TODO)


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

#### A standard, unflagged codeblock
```
This'll be ignored
```

#### A codeblock designed to be run
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

#### Shared interpreter demo
*Again, just done with* `'''python#run`.

```python
print(f(10))
```
```
3628800
```

#### A new interpreter instance
This one uses one additional tag, now looking like `'''python#run#new`. Snazzy.
```python
print(f(11))
```
```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
NameError: name 'f' is not defined
```

#### Unboxed output
`'''python#run#unboxed`
```python
print('This is a test of *various* **markdown** ~~features~~.')
```
This is a test of *various* **markdown** ~~features~~.

#### Hidden input-field with `#hide`
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

#### Inverted output order
This one uses `'''python#run#output_first`:
```
7
```
```python
print(3+4)
```

These tags can, of course, be combined. Just look at this very sentence in [README_src.md](https://raw.githubusercontent.com/FraserLee/execute-dot-md/main/README_src.md) 😉

# Languages

## :crab: rust :crab:
```rust
fn main() {
    let x = 2;
    let y = 3;
    println!("{}", x + y);
}
```
```
5
```

```rust
fn main() {
    this is a syntax error
}
```
```
error: expected one of `!`, `.`, `::`, `;`, `?`, `{`, `}`, or an operator, found `is`
 --> <anon>:2:10
  |
2 |     this is a syntax error
  |          ^^ expected one of 8 possible tokens

error: aborting due to previous error

```

## :snake: python :snake:
```python
print(2+2)
```
```
4
```

## c
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

## c++
```cpp
#include <iostream>
#include <cmath>
int main() {
    float x = 1.;
    float y = 2.;
    std::cout << sqrt(-1) << std::endl;
    return 0;
}
```
```
nan
```

## bash :shell:
```bash
# print the first few prime numbers separated by dashes
for ((i=2; i<37; i++)); do
    for ((j=2; j<i; j++)); do
        if (($i % $j == 0)); then break; fi
    done
    if (($i == $j)); then echo -n $i"-"; fi
done

# then finish off a few more with awk
awk 'BEGIN { RS = " "; ORS = "|" } {
    for (i=2; i<$1; i++) {
        if ($1 % i == 0) break
        if ($1 == i+1) print $1
    }
} END { ORS = "\n"; print "" }' <<< $(seq 37 100)
```
```
2-3-5-7-11-13-17-19-23-29-31-37|41|43|47|53|59|61|67|71|73|79|83|89|97|
```

## go
```go
package main
import "fmt"

func main() {
    fmt.Println("go" + "lang")
}
```
```
golang
```

## JS :yellow_square:
```js
const x = '7'
const y = 1
console.log(x - y)
console.log(x + y)
```
```
6
71
```

## Lua
```lua
local a = {1, nil, "test"}

for key, value in pairs(a) do
  local b = value and print(value)
end
```
```
1
test
```


## Kotlin
```kotlin
import kotlin.math.*

infix fun Int.greaterThanExp(x: Int) = this > exp(x.toFloat())

fun factorial(x: Int): Int = when (x) {
    0    -> 1
    else -> x * factorial(x - 1)
}

println(factorial(5) greaterThanExp 6)
println(factorial(6) greaterThanExp 7)
println(factorial(7) greaterThanExp 8)
```
```
false
false
true
```

---

### Haskell
```haskell
main = (putStrLn . reverse) "!dlrow olleh"
```
```
hello world!
```

### Nim :crown:
```nim
proc factorial(x: int): int =
    if x <= 0: 1
    else: x * factorial(x - 1)
  
echo "10! = ", factorial(10)
```
```
10! = 3628800
```

### Haxe
```haxe
class Main {
    static public function main() {
        trace("hello world");
    }
}
```
```
Main.hx:3: hello world
```

### OCaml 🐫
```ocaml
print_string "hello world\n"
```
```
hello world
```

### Java :coffee:
```java
class Main{
    public static void main(String[] args){
        System.out.println("hello world!");
    }
}
```
```
hello world!
```

### Zsh
```zsh
echo "hello world!"
```
```
hello world!
```

### Brainfuck
*(example sourced from Wikipedia)*
```brainfuck
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>
---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
```
```
Hello World!
```
