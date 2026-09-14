# NumScript: A Numerical Programming Language

NumScript is a **lightweight, esoteric, interpreted scripting language** designed for **numerical programming** and writing simple scripts.

The language started as a joke back in **mid-2024**, and over time it grew into its current form featuring a **rich syntax** and a **unique numerical logic system**.

The code is not perfect as this is my first project I started right around when I started learning programming, however I try to improve it from time to time.

👉 You can try the language at [**numscript.xyz**](https://numscript.xyz)

## Key Features

NumScript includes several defining features that shape its unique programming model:
13 01 00 24 01 00
- **Token-Based Syntax:** All instructions are built using numeric token pairs (for example, `13 01`).
- **Zero-Error Policy:** NumScript never crashes. Mistyped or incomplete code automatically defaults to safe (though possibly unintended) behavior.
- **Real-Time Execution:** The interpreter processes code one line at a time, providing immediate feedback.
- **Simplicity:** NumScript features a minimalistic syntax and a limited set of data types, resulting in a lightweight and efficient programming experience.

## Requirements

NumScript doesn't use any non standard Python libraries so you will need to simply install Python. Bellow are the versions of Python that I've tried so far.

| Works | Python Version |
|-------|----------------|
| ✅ | 3.14.4 |
| ✅ | 3.14.0 |
| ✅ | 3.13.9 |
| ✅ | 3.13.7 |

## How to use

Running NumScript shell:

### Windows

`python NumScript.py`

### Linux 

`python3 NumScript.py`

Running NumScript file:

### Windows 

`python NumScript.py main.ns`

### Linux

`python3 NumScript.py main.ns`

### AUR Package

`yay -s numscript`

## Core Mechanics

NumScript is an **interpreted language**, meaning the interpreter reads and executes code **one line at a time**.

It works with two stacks of code:

### 1. Tokenized Code
This stack contains a code from either shell or file. 

It is the code that is primarily executed.

### 2. Higher Tokenized Code
This stack contains a code with higher execution priority. 

This code can originate from called definitions for example.

After each executed line from Tokenized Code the NumScript Virtual Machine checks this stack if it contains any new code and if it does it is executed.

After all code from Higher Tokenized Code is executed the NumScript Virtual Machine continues with execution of the primary code in Tokenized Code.

## Execution process
The internal execution process is composed of several steps:

### 1. Tokenization
The code is first processed by a **tokenizer**, which checks that its content is numeric and splits it into **token pairs** — for example: "10", "01", "00"

### 2. Execution Setup
After the instruction 00 (RUN) is passed, the code is compiled into a simplified internal format and sent to the executor.
The executor reads each line in order and passes it to the code runner.
    
### 3. Parsing
The code runner sends the current line to the interpreter.
The interpreter analyzes the tokens to determine which function should be executed — this is defined by the first token pair.
That first pair is then removed, and the remaining tokens are passed to the interpreteoperandAssembler for further analysis.
    
### 4. Lexing
The interpreteoperandAssembler processes the remaining tokens and groups them into interpreteoperandAssembler Blocks, which represent final, usable values.
In NumScript, these blocks are separated by the token 24.
    
Example — Variable Definition: 13 01 00 24 01 01 01 00
    
This expression contains two blocks:
    
The first block defines the variable name, with the value 00.
The second block defines the value of that variable, with the value 01 10.
    
These blocks are then passed back to the interpreter and they are used as parameters in the executed function.
    
### 5. Execution Result
The interpreter assigns the blocks as parameters for the target function, and the result is printed to the console.
    
### Summary
Tokenizer -> Splits code into numeric token pairs.
    
Executor -> Reads and sends each line for execution.
    
interpreter -> Determines which function each token pair represents and sets its arguments.
    
interpreteoperandAssembler -> Groups tokens into logical blocks and evaluates their values.
    
Console Output -> Displays the final result after execution.

## Builder Variables
The builder is a function that combines all of the parts of NumScript Virtual Machines.

It has multiple variables that are used in the entire code.
    
## Runtime Architecture
    
```
cli -> run -> lineRunner -> interpreter -> interpreter -> operandAssembler -> interpreter -> lineRunner -> cli
                   |                                              |
                   <----------------------------------------------<  
```
                      
## Token MAP

| Name | Token | Description                                                          | Example |
|------|--------|----------------------------------------------------------------------|----------|
| Run | 00 | Another way of running code inserted to console.                     | 00 |
| Number | 01 | Stack towards a number.                                              | 01 00 |
| Variable (num) | 02 | Stack towards variable by name.                                      | 02 00|
| Variable (var) | 03 | Points to variable by value of variable.                             | 03 00|
| Index (num) | 04 | Replaces interpreteoperandAssembler block by numeric index.                               | 01 00 01 01 04 00 |
| Index (var) | 05 | Replaces interpreteoperandAssembler block by variable value index.                        | 01 00 01 01 05 00 |
| Rest is num | 06 | Considers rest of line to be a number.                               | 06 00 01 |
| Rest is var | 07 | Considers rest of line to be a variable.                             | 07 00 01 |
| Stack (num) | 08 | Calls all variables from a stack where its name is a number.         | 08 00 |
| Stack (var) | 09 | Calls all variables from a stack where its name is a variable value. | 09 00 |
| Print | 10 | Prints all interpreteoperandAssembler blocks.                                             | 10 01 00 |
| Print in NS Ascii | 11 | Prints all interpreteoperandAssembler blocks translated by NS Ascii.                      | 11 01 00 |
| Input | 12 | Adds user input to current interpreteoperandAssembler block.                              | 10 12 |
| Let | 13 | Defines a variable (name + combined value).                          | 13 01 00 24 01 10 |
| Define Stack | 14 | Defines a stack with specified variables.                            | 14 01 00 24 01 05 24 01 07 |
| Remove variable from Stack by name | 15 | Removes specific variables from stack.                               | 15 01 00 24 01 05 |
| Remove variable from Stack by index | 16 | Removes specific variable from stack by index.                       | 16 01 00 24 01 05 |
| Append to Stack | 17 | Adds variables to stack.                                             | 17 01 00 24 01 00 |
| Merge Stacks | 18 | Merges second stack into first.                                      | 18 01 00 24 01 01 |
| Delete Stack | 19 | Deletes specific stack.                                              | 19 01 00 |
| Exit | 20 | Ends execution of script.                                            | 20 |
| Restart | 21 | Restarts the console.                                                | 21 |
| Comment | 22 | Marks code as comment (not executed).                                | 22 10 01 00 |
| Split between variables | 23 | Splits between variables in interpreteoperandAssembler block.                             | 10 02 00 23 02 01 |
| Split in interpreteoperandAssembler parts | 24 | Split between interpreteoperandAssembler blocks.                                          | 13 01 00 24 01 00 |
| Then | 25 | Allows multiple lines on one line.                                   | 10 01 00 25 10 01 01 |
| Date | 26 | Inserts current date as number.                                      | 10 26 |
| Time | 27 | Inserts current time as number.                                      | 10 27 |
| Read down | 28 | Interpreter reads from top to bottom.                                | 28 |
| Read up | 29 | Interpreter reads from bottom to top.                                | 29 |
| + | 30 | Plus operator.                                                       | 10 01 01 30 01 01 |
| - | 31 | Minus operator.                                                      | 10 01 01 31 01 01 |
| * | 32 | Times operator.                                                      | 10 01 01 32 01 01 |
| / | 33 | Division operator.                                                   | 10 01 01 33 01 01 |
| > | 34 | Greater than operator.                                               | 10 01 00 34 01 01 |
| < | 35 | Smaller than operator.                                               | 10 01 01 35 01 01 |
| = | 36 | Equals operator.                                                     | 10 01 01 36 01 01 |
| & | 37 | AND operator.                                                        | 10 01 01 37 01 01 |
| \| | 38 | OR operator.                                                         | 10 01 01 38 01 01 |
| ~ | 39 | NOT operator.                                                        | 10 39 01 01 |
| Jump | 40 | Jumps to specific line.                                              | 40 01 00 |
| Wait | 41 | Freezes script for time.                                             | 41 01 01 |
| Clean Console | 42 | Cleans console content.                                              | 42 |
| Clean States | 43 | Resets state values.                                                 | 43 |
| Clean Tokenized Code | 44 | Clears tokenized code.                                               | 44 |
| Clean Higher Priority Tokenized Code | 45 | Clears higher priority tokenized code.                               | 45 |
| Clean Variables | 46 | Clears variable memory.                                              | 46 |
| Clean Definitions | 47 | Clears definitions memory.                                           | 47 |
| Clean Stacks | 48 | Clears stack memory.                                                 | 48 |
| States | 49 | Switches state values.                                               | 49 01 00 01 00 |
| TAB (if/cycles) | 50 | Marks code inside conditional/cycle.                                 | 50 10 01 00 |
| End of cycle/statement | 51 | Ends a conditional or cycle.                                         | 50 51 |
| If | 52 | Conditional statement.                                               | 52 01 01 |
| While | 53 | Repeats code while condition true.                                   | 53 02 00 34 01 10 |
| For | 54 | Loops for variable’s value count.                                    | 54 01 00 |
| Do if | 55 | Runs at least once even if false.                                    | 55 01 00 |
| Define | 56 | Creates a new definition.                                            | 56 01 00 |
| TAB (define) | 57 | Adds code to definition.                                             | 57 10 01 00 |
| Call definition | 58 | Calls a defined definition.                                          | 58 01 00 |
| Lambda | 59 | Defines inline function-like definition.                             | 59 01 00 24 06 10 01 00 |
| Load TXT | 60 | Loads value from .txt file.                                          | 60 01 00 24 01 05 |
| Save TXT in NumScript | 61 | Saves variable to .txt file (NumScript).                             | 61 01 00 24 01 05 |
| Save TXT in NumScript Ascii | 62 | Saves variable to .txt file (Ascii).                                 | 62 01 00 24 01 05 |
| Import variables | 63 | Imports variables from JSON file.                                    | 63 01 00 24 01 00 |
| Export variables | 64 | Exports variables to JSON file.                                      | 64 01 00 24 01 00 |
| Import Stacks | 65 | Imports stacks from file.                                            | 65 01 00 24 01 05 |
| Export Stacks | 66 | Exports stacks to file.                                              | 66 01 00 24 01 05 |
| Import Definition | 67 | Imports definitions from JSON.                                       | 67 01 00 24 01 00 |
| Export Definition | 68 | Exports definitions to JSON.                                         | 68 01 00 24 01 00 |
| Load NS code | 69 | Loads NumScript code and executes.                                   | 69 01 00 |
| Minimal | 70 | Keeps smallest token pair.                                           | 10 01 00 01 01 70 |
| Maximal | 71 | Keeps largest token pair.                                            | 10 01 00 01 01 71 |
| Average | 72 | Replaces tokens with average.                                        | 10 01 00 01 04 72 |
| Sum | 73 | Replaces tokens with sum.                                            | 10 01 03 01 02 73 |
| Length | 74 | Replaces with total token count.                                     | 10 01 00 01 00 74 |
| Sort | 75 | Sorts token pairs.                                                   | 10 01 01 01 03 01 02 75 |
| Any | 76 | True if any token > 00.                                              | 10 01 00 01 00 76 |
| All same | 77 | True if all tokens equal.                                            | 10 01 01 01 01 77 |
| Random item | 78 | Picks random token.                                                  | 10 01 00 01 01 01 02 78 |
| Most common | 79 | Keeps most frequent token.                                           | 10 01 00 01 00 01 01 79 |
| Shuffle | 80 | Randomizes token order.                                              | 10 01 00 01 01 80 |
| Reverse | 81 | Reverses token order.                                                | 10 01 02 01 03 81 |
| Poke variable memory name | 82 | Gets variable name by index.                                         | 82 01 00 |
| Poke variable memory value | 83 | Gets variable value by index.                                        | 83 01 00 |
| Insert to tokenized code | 84 | Inserts code to Tokenized Code.                                      | 84 01 00 24 06 10 01 00 |
| Insert to higher tokenized code | 85 | Inserts code to higher tokenized.                                    | 85 01 00 24 06 10 01 00 |
| Remove variable from memory | 86 | Deletes variable from memory.                                        | 86 01 00 |
| Remove definition from memory | 87 | Deletes definition from memory.                                      | 87 01 00 |
| Swap variable name/value | 88 | Swaps variable name and value.                                       | 88 01 00 |
| Rename variable | 89 | Renames a variable.                                                  | 89 01 00 24 01 01 |
| Contains | 90 | Checks if item is in sequence.                                       | 90 01 00 24 01 05 24 01 00 01 01 01 02 |
| Add tokens by index | 91 | Adds tokens to variable by index.                                    | 91 01 00 24 01 00 24 01 01 |
| Remove token by index | 92 | Removes token by index.                                              | 92 01 05 24 01 00 |
| Replace | 93 | Replaces token pair with another.                                    | 93 01 00 24 01 00 24 01 01 24 01 00 01 00 |
| Replace by index | 94 | Replaces token at specific index.                                    | 94 01 00 24 01 00 24 01 01 |
| Random randint | 95 | Sets variable to random int in range.                                | 95 01 00 24 01 00 24 01 05 |
| Substring | 96 | Extracts substring by start/end index.                               | 96 01 00 24 01 01 24 01 04 |
| &= | 97 | Sets variable to 01 if equal, else 00.                               | 97 01 00 24 01 00 |
| \|= | 98 | Sets variable to 00 if not equal, else 01.                           | 98 01 00 24 01 00 |
| Guide | 99 | Shows NumScript website URL.                                         | 99 |

## NumScript Ascii 

| Code | Char | Code | Char | Code | Char | Code | Char | Code | Char |
|------|------|------|------|------|------|------|------|------|------|
| 00 | a | 01 | b | 02 | c | 03 | d | 04 | e |
| 05 | f | 06 | g | 07 | h | 08 | i | 09 | j |
| 10 | k | 11 | l | 12 | m | 13 | n | 14 | o |
| 15 | p | 16 | q | 17 | r | 18 | s | 19 | t |
| 20 | u | 21 | v | 22 | w | 23 | x | 24 | y |
| 25 | z | 26 | A | 27 | B | 28 | C | 29 | D |
| 30 | E | 31 | F | 32 | G | 33 | H | 34 | I |
| 35 | J | 36 | K | 37 | L | 38 | M | 39 | N |
| 40 | O | 41 | P | 42 | Q | 43 | R | 44 | S |
| 45 | T | 46 | U | 47 | V | 48 | W | 49 | X |
| 50 | Y | 51 | Z | 52 | 0 | 53 | 1 | 54 | 2 |
| 55 | 3 | 56 | 4 | 57 | 5 | 58 | 6 | 59 | 7 |
| 60 | 8 | 61 | 9 | 62 | ! | 63 | " | 64 | # |
| 65 | $ | 66 | % | 67 | & | 68 | ' | 69 | ( |
| 70 | ) | 71 | * | 72 | + | 73 | , | 74 | - |
| 75 | . | 76 | / | 77 | : | 78 | ; | 79 | < |
| 80 | = | 81 | > | 82 | ? | 83 | @ | 84 | [ |
| 85 | \\ | 86 | ] | 87 | ^ | 88 | _ | 89 | ` |
| 90 | { | 91 | &#124; | 92 | } | 93 | ~ | 94 | € |
| 95 | £ | 96 | ¥ | 97 | ¢ | 98 | § | 99 | ' ' |

## NumScript Interpreter Debug Codes

| Code | Function | Description |
|------|----------|-------------|
| -99 | Invalid Function | Returned when a token does not match any case; the line is deleted. |
| -99002401 | Run (00) | Returned after a code execution is initialized. |
| -991324[value]24[value] | Define Var (13) | Confirms a variable was set with a specific name and value. |
| -991424[value] | Define Stack (14) | Confirms a new stack was initialized with provided variables. |
| -991524[value] | Stack Pop Name (15) | Returned after removing a variable from a stack by name. |
| -991624[value] | Stack Pop Index (16) | Returned after removing a variable from a stack by index. |
| -991724[value] | Stack Append (17) | Confirms data was successfully appended to the specified stack. |
| -991824[value] | Merge Stacks (18) | Confirms two stacks were merged into one. |
| -991924[value] | Delete Stack (19) | Confirms a specific stack was deleted from memory. |
| -9921 | Restart (21) | Issued when all memory, variables, and states are reset. |
| -9928 | Top-Down (28) | Confirms execution direction is set to top-to-bottom. |
| -9929 | Bottom-Up (29) | Confirms execution direction is set to bottom-to-top. |
| -994024[value] | Jump (40) | Indicates a jump to a specific line index in the script. |
| -994124[value] | Wait (41) | Confirms the interpreter paused for the specified duration. |
| -9942 | Clear Console (42) | Issued after clearing the terminal screen. |
| -9943 | Clear States (43) | Confirms all internal flags were reset. |
| -9944 | Clear Code (44) | Confirms the primary tokenized code was wiped. |
| -9945 | Clear High Code (45) | Confirms the higher tokenized code buffer was wiped. |
| -9946 | Clear Variables (46) | Confirms all user-defined variables were deleted. |
| -9947 | Clear Definitions (47) | Confirms all custom function definitions were deleted. |
| -9948 | Clear Stacks (48) | Confirms all stacks were deleted. |
| -9951 | Break (51) | Issued when exiting a loop or conditional block. |
| -9952[00 / 01] | If (52) | Evaluates a condition: 01 for true, 00 for false. |
| -995301 | While (53) | Confirms the initialization of a while-loop. |
| -9954[00 / 01] | For (54) | Returns success (01) or variable failure (00) for for-loops. |
| -9955 | Do If (55) | Confirms a conditional execution block was processed. |
| -995624[value] | Define (56) | Confirms the creation of a new function definition. |
| -995824[value] | Call Def (58) | Returns the definition name called (or 00 if missing). |
| -99[value]24[value] | Lambda (59) | Confirms a single-line lambda definition was created. |
| -9960[value] | Load TXT (60) | Confirms file loading or returns 00 if not found. |
| -9961 | Save TXT (61) | Confirms data was saved to a .txt file. |
| -9962 | Save NS Ascii (62) | Confirms data was saved using NumScript Ascii encoding. |
| -9963[value] | Import Vars (63) | Returns the list of variables imported from JSON. |
| -9964[value] | Export Vars (64) | Returns the list of variables exported to JSON. |
| -9965[value] | Import Stacks (65) | Returns the list of stacks imported from JSON. |
| -996624[value] | Export Stacks (66) | Returns the list of stacks exported from JSON. |
| -996724[value] | Import Defs (67) | Returns the list of definitions imported from JSON. |
| -996824[value] | Export Defs (68) | Returns the list of definitions exported from JSON. |
| -996924[value] | Load NS (69) | Confirms external code was loaded into the higher buffer. |
| -9984 | Insert Code (84) | Confirms tokens were inserted into the primary code list. |
| -9985 | Insert High (85) | Confirms tokens were inserted into higher code list. |
| -9986 | Remove Var (86) | Confirms the deletion of specific variables. |
| -9987 | Remove Def (87) | Confirms the deletion of specific function definitions. |
| -9988[value]24[value] | Swap Var (88) | Confirms a variable name and value have been swapped. |
| -9989[value]24[value] | Rename Var (89) | Returns the new name and value of a renamed variable. |
| -9991[value]24[value] | Add Token (91) | Confirms a token was inserted into a string by index. |
| -9992[value]24[value] | Rem Token (92) | Confirms a token was removed from a string by index. |
| -999324[value] | Replace (93) | Returns the string after a search-and-replace. |
| -999424[value] | Replace Index (94) | Returns the string after replacing a specific index. |
| -999524[value] | Random (95) | Returns the generated random integer. |
| -999624[value] | Sub String (96) | Returns the extracted segment of a string. |
| -999724[value] | Equals (97) | Returns 01 if equal, 00 if not. |
| -999824[value] | Not Equals (98) | Returns 01 if not equal, 00 if equal. |

### Data Folders
These folders are automatically created in the path of your choice after NumScript.py is ran for the first time.

There are 5 different subfolders inside the data folder.

The NumScript functions that save and load different types of files use these folders.

#### 1. Code
This folder is used for loading .ns files.

#### 2. Definitions
This folder is used for saving or loading definitions using a .json files.

#### 3. Files
This folder is used for saving or loading .txt files.

### 4. Stacks
This folder is used for saving or loading stacks using a .json files.

#### 5. Variables
This folder is used for saving or loading variables using a .json files.

## NumScript Container

Container is a way to run NumScript code embeded in regular Python files.

It uses the nsOut variable which saves the last print.

NumScript Virtual Machine is restarted after each container instance finishes.

### Example usage

```
from source.builder import NumScriptVirtualMachine

NSVM = NumScriptVirtualMachine()

result = NSVM.container("10 01 00")

print(result)

NSVM.container([
    "13 01 00 24 01 10",
    "13 01 01 24 01 05",
    "10 02 00 30 02 01"
])

print(NSVM.nsOut)
```

## Code Examples

Note: $ stands before user input in Console output parts.

### Example of using the print function.

NumScript code

```
10 01 00
10 01 05
10 01 10
```

Console output

```
00
05
10
```

### Example of defining variables and then printing their values

NumScript code

```
13 01 00 24 01 10
13 01 01 24 01 20

10 02 00
10 02 01
```

Console output

```
10
20
```

### Example of defining a variable and for cycle

NumScript code

```
13 01 01 24 01 10
54 01 01
50 10 02 01
50 51
```

Console output

```
10
09
08
07
06
05
04
03
02
01
```

### Example of while cycle

NumScript code

```
13 01 00 24 01 01
53 02 00 35 01 11
50 10 02 00
50 13 01 00 24 02 00 30 01 01
50 51
```

Console output

```
01
02
03
04
05
06
07
08
09
10
```

### Guess a number between 00 - 99

NumScript code

```
13 01 00 24 01 01
95 01 01 24 01 00 24 01 99
11 06 32 20 04 18 18 99 19 07 04 99 13 20 12 01 04 17
53 02 00
50 13 01 02 24 12
50 52 02 02 36 02 01
50 50 11 06 50 14 20 99 22 14 13
50 50 13 01 00 24 01 00
50 50 51 
50 52 02 02 35 02 01
50 50 11 06 33 08 06 07 04 17
50 50 51
50 52 02 02 34 02 01
50 50 11 01 37 01 14 01 22 01 04 01 17
50 50 51
50 51
```

Example of Console output

```
Guess the number
$ 50
Higher
$ 75
Lower
$ 62
Higher
$ 67
Lower
$ 65
Lower
$ 63
You won
```

### Recursion Example

NumScript code

```
13 01 00 24 01 00
56 01 00
57 10 02 00
57 13 01 00 24 02 00 30 01 01
57 52 02 00 35 01 10
57 50 58 01 00
58 01 00
```

Console output

```
00
01
02
03
04
05
06
07
08
09
10
```
