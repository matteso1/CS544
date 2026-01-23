# Read-only Access

We've opened up the `autobadger` tool in attempt to make things more visible to you and less of a "black box". We've done this by making the repository *read-only*, meaning you should be able to `git clone` the repo but not `git push` to it.

To start, navigate to a directory outside of any class project. I'd recommend cloning to the same directory as your projects.

```bash
git clone https://oauth2:glpat-JbpjuwYwgD4O0a5mmYvd6m86MQp1OmNqeQk.01.0z1jzxwzu@git.doit.wisc.edu/cdis/cs/courses/cs544/tools/autobadger.git
```


> **NOTE**: if you want to use this method throughout the semester, you'll need to `git pull` to get up-to-date code for each project.


Your folder structure should look something like

```
some-directory/
	autobadger/
	p1/
	p2/
    ... # other projects
```

# Making Changes

You can change the code inside of `autobadger`. The only files that will be of interest to you are inside the `projects/` directory, i.e. `projects/*.py`). Your changes will be for debugging, i.e. `print()` or `breakpoint()` statements.
#### Using `pip`

For whatever project you're working on, you will need to *apply* any changes you make using `pip`

For example, assuming
- I'm working on `p2`
- in my `p2` directory
- and have my `venv` activated

I would do something like:

```bash
pip3 install ../autobadger/.
```

This would install and replace my local version of `autobadger` . Now when I run 

```
autobadger --project=p2
```

I will see my changes in effect.

# Breakpoints

Since `breakpoint()` is less known and straightforward, I will teach about it here.

> **NOTE**: It is not required to use `breakpoint()`. You are also welcome to use `print()` instead. `breakpoint()` has a **steeper learning curve**, but may **help you iterate more quickly and save you time** once the basic concepts are well-understood.

### What is a breakpoint?

`breakpoint()` is a built-in function in Python and starts the **debugger** at the point where it is called. It allows developers to inspect variables, step through code, and debug interactively.
#### Simple Example:

```python
# Inside of /path/to/file.py

def calculate_sum(a, b):
    breakpoint()  # Debugger starts here
    return a + b 


calculate_sum(3, 5)  # execute function
```

Adding a `breakpoint()`  will pause execution, allowing you to inspect `a` and `b` before proceeding. I would see something like:

```
> /path/to/file.py(3)calculate_sum()
-> return a + b
```

in the terminal, which displays
1. the next line to be executed `return a + b`
2. `(3)calculate_sum()` tells me the line number and the function name (if applicable)
3. `/path/to/file.py` tells me the current file

### Navigating the debugger

While the Python debugger is active, you can use several commands to navigate through your program and investigate.

- `Variable name`:  I can type any variable that is in scope and get it's value.
	- Ex: Typing `a` in the previous example would return the *value* of `a`
	- **NOTE**: if a variable name also coincides with a command keyword in the debugger, you may need to use `print(<variable_name>)` instead. `b` is one of those commands, so to print the value of `b` to the terminal, I would need to do `print(b)`:
- `Evaluation`: I can also evaluate statements (i.e. add two numbers)

```
In [3]: calculate_sum(3, 5)
> <ipython-input-2-443b6e8e0b0a>(3)calculate_sum()
-> return a + b

(Pdb) print(a)
3

(Pdb) print(b)
5

(Pdb) print(a + b)
8
```

- `n`: Steps to the next line of my program
- `c`: Continues execution of the program until the next breakpoint, or until the program ends.
- `s`: Steps *into* a function or method call
- `exit`: kills the debugger and ends the program

# An example

### Using breakpoints

Suppose I want to investigate `Q4` for `p2`. I can add `breakpoint()` statements to the Q4 test method for the `ProjectTwoTest` class.

Navigating to `projects/p2.py` inside of `autobadger`, I find:

```python
@graded(Q=4, points=10)  
def test_simple_http(self) -> int | TestError:  
    address = self._test_cache_server("-cache-1")  
    if isinstance(address, TestError):  
        return address  
    r = requests.get(f"{address}/lookup/53706")  
    r.raise_for_status()  
    result = r.json()  
    if "addrs" not in result or "source" not in result:  
        return TestError(  
            message=f"Result body should be JSON with 'addrs' and 'source' fields, but got {result}.",  
            earned=5,  
        )  
    return 10
```

> Note: This is Q4 since I have `Q=4` in the decorator.

**I can edit this method by adding *breakpoints*!**

```python
@graded(Q=4, points=10)  
def test_simple_http(self) -> int | TestError:  
    breakpoint()  
    address = self._test_cache_server("-cache-1")  
    if isinstance(address, TestError):  
        return address  
    r = requests.get(f"{address}/lookup/53706")  
    breakpoint()
    r.raise_for_status()
    result = r.json()  
    if "addrs" not in result or "source" not in result:  
        return TestError(  
            message=f"Result body should be JSON with 'addrs' and 'source' fields, but got {result}.",  
            earned=5,  
        )  
    return 10
```

Now, after I update with `pip` as mentioned above, I can run `autobadger --project=p2` and get:

```
> /Users/.../p2.py(103)test_simple_http()
-> address = self._test_cache_server("-cache-1")
```

Note that in this situation, typing `address` would give me an error cause it **not yet defined**:

```
(Pdb) address
*** NameError: name 'address' is not defined
```
###### Using `n` (next line)

`address` defined on the *next line*. So, I use the `n` command to step!

```
(Pdb) n
> /Users/.../p2.py(104)test_simple_http()
-> if isinstance(address, TestError):

(Pdb) address
'http://localhost:64879'
```
###### Using `s` (step into)

I could have also used `s` to *step into* `self._test_cache_server(...)` if I had wanted to investigate further:

```
> /Users/.../p2.py(103)test_simple_http()
-> address = self._test_cache_server("-cache-1")

(Pdb) s
--Call--
> /Users/.../p2.py(118)_test_cache_server()
-> def _test_cache_server(self, server_suffix: str) -> str | TestError:
       # Now in a new method — _test_cache_server

(Pdb) n
> /Users/.../p2.py(119)_test_cache_server()
-> cache_server = [c for c in self.containers if c["Name"].endswith(server_suffix)]

```
###### Using `c` (continue)

I can also *continue* till the next breakpoint, which is quite convenient if you don't need to step over every line of code:

```
> /Users/.../p2.py(103)test_simple_http()
-> address = self._test_cache_server("-cache-1")

(Pdb) c
> /Users/.../p2.py(108)test_simple_http()
-> r.raise_for_status()

(Pdb) print(r.json())
{'addrs': [...], 'error': None, 'source': '...'}
```

Using `c` jumped from line `103` to line `108`, where I had my two breakpoints defined.

> **NOTE**: using `c` again would continue the Python program till the end of its execution since I have no other `breakpoint()` statements