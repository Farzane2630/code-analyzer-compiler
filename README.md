Mini Compiler Analyzer (Python)

A small educational project for a university Compiler Design course.

This program analyzes source code written in a small custom language. It checks the code in three stages:

1. Lexical analysis — identifies tokens and invalid characters.
2. Syntax analysis — checks whether tokens follow the language's grammar.
3. Semantic analysis — checks variable declarations and basic data-type rules.
   It also offers one simple correction rule: adding semicolons to the ends of non-empty lines. After applying this rule, it runs the analyzer again.
   Important: This is a learning project, not a complete compiler. It does not support all of Python, C, or C++, and it does not generate machine code or run the submitted program. It does not use an AI model; the analysis and correction are based on rules written in Python.

4. Language supported by this project
   The analyzer understands a small language with these features:

- Variable types: int, float, and string
- Variable declarations
- Assignments to variables
- Integer and decimal numbers
- Text in double quotes
- Arithmetic: +, -, \*, /
- Parentheses in expressions
- Semicolons at the end of statements
  Examples:
  int age = 20;
  float price = 12.5;
  string name = "Sara";
  age = age + 1;
  price = price \* 2;
  The language is intentionally small so the compiler concepts are easier to understand.

2. Requirements

- Python 3
- No external Python packages are required.

3. How to run it
1. Save the source code in a file named mini_compiler.py.
1. Open a terminal in the folder containing that file.
1. Run:
   python3 mini_compiler.py
1. Enter the program you want to analyze, one line at a time.
1. Press Enter on an empty line to finish entering code.
1. Read the analysis results. If an error is found, the program may offer its semicolon-correction rule.
   Example input:
   int age = 20;
   age = age + 1;
   The program should report that no lexical, syntax, or semantic errors were found.
1. How the program works
   The program follows the general structure of a compiler's front end:
   Source code
   |
   v
   Lexical analysis
   |
   v
   Syntax analysis
   |
   v
   Semantic analysis
   |
   v
   Valid code / error report
   |
   v
   Optional correction and re-analysis
   Each stage depends on the previous stage. The lexer turns characters into tokens. The parser checks the token sequence and builds a simple tree-like representation of expressions. The semantic analyzer checks whether variables and types are used according to the language's rules.

In this version, a lexical or syntax error stops the later stages. This avoids trying to perform semantic checks on code the parser could not understand. 5. Explanation of the source code
A. The token pattern
The program uses Python's re module, which provides regular expressions. A regular expression is a pattern for recognizing text.

The token pattern recognizes:
Token kind Meaning Example
SPACE Whitespace spaces, tabs, newlines
NUMBER Integer or decimal number 12, 3.5
STRING Text in double quotes "hello"
ID Variable name or keyword before keyword checking age, total
SYMBOL Supported punctuation/operator =, +, ;, (
BAD Any character not matched by the earlier patterns @

The patterns are checked in order. The lexer later changes int, float, and string from identifiers into the TYPE token kind.
B. lexer(code) — lexical analysis
This function reads the source text and returns two things:

- A list of tokens.
- A list of lexical error messages.
  Each token is stored as a Python dictionary with three fields:
- type: the token category.
- value: the actual text.
- line: the line number where it appeared.
  For example, the source int age = 20; produces tokens similar to:
  (TYPE, int)
  (ID, age)
  (SYMBOL, =)
  (NUMBER, 20)
  (SYMBOL, ;)
  Whitespace is skipped because it normally separates tokens rather than being a meaningful token in this language. The lexer tracks newlines to report line numbers. At the end, it adds an EOF token, meaning “end of input.” The parser uses it to know when to stop.

If a character matches BAD, the lexer reports a lexical error.
C. The Parser class — syntax analysis
A class groups related data and functions together. Here, the Parser class stores the token list and the position of the next token to read.

Its main parts are:

- current() returns the token currently being examined.
- eat(expected) checks that the current token has the expected category, then advances to the next token.
- expect_symbol(symbol) checks for a specific symbol such as = or ;.
- parse() reads statements until it reaches EOF.
- statement() recognizes a declaration or an assignment.
- expression(), term(), and factor() analyze arithmetic expressions.
  Why are there three expression functions?
  They implement operator precedence.
- expression() handles + and -.
- term() handles \* and /.
- factor() handles numbers, strings, variable names, and parenthesized expressions.
  Because expression() calls term(), multiplication and division are grouped before addition and subtraction. For example, 2 + 3 _ 4 is understood as 2 + (3 _ 4).

The parser returns tuples that represent simple tree-like structures. For example:
("number", "20")
("variable", "age")
("bin", "+", ("variable", "age"), ("number", "1"))
The last example represents age + 1: it has the node kind bin, the operator +, and the left and right parts of the expression.

If the parser finds an unexpected token, it raises a SyntaxError with a message and line number. The main function catches this error and displays it.
D. semantic_check(statements) — semantic analysis
A statement can be syntactically correct but still make no sense according to the language's rules.

For example:
int age = "twenty";
The statement has a valid general structure, but the declared type is int and the assigned value is a string.

The semantic analyzer uses a dictionary called variables as a symbol table. It stores each successfully declared variable and its type. Conceptually, it might contain:
{
"age": "int",
"price": "float"
}
The nested function expression_type(node, line) works out the type of an expression:

- An integer literal has type int.
- A decimal literal has type float.
- A string literal has type string.
- A variable gets its type from the symbol table.
- An arithmetic expression must use numeric operands.
  The semantic analyzer checks for:
- Using a variable before it has been declared.
- Declaring the same variable more than once.
- Assigning incompatible types.
- Using strings in arithmetic expressions.
  This is a deliberately basic type system. For example, assigning an int value to a float variable is allowed, but assigning a float to an int variable is rejected.
  E. fix_missing_semicolons(code) — basic correction
  This function splits the source code into lines. For each non-empty line, it adds a semicolon if the line does not already end with one.

For example:
int age = 20
becomes:
int age = 20;
This is a simple rule-based correction, not an intelligent general-purpose repair system. It can add a semicolon in places where one is not appropriate, so the corrected code must be analyzed again. The program does this rather than assuming the correction succeeded.
F. analyze(code) — coordinating the stages
This function connects the three analysis stages:

1. Run the lexer.
2. If there are lexical errors, display them and stop.
3. If lexical analysis succeeds, run the parser.
4. If parsing fails, display the syntax error and stop.
5. If parsing succeeds, run semantic analysis.
6. Display semantic errors, or report that the code is valid.
   It returns True if all three stages succeed and False if the program finds an error.
   G. The main block — user interaction
   The condition:
   if **name** == "**main**":
   means the interactive part runs when the file is executed directly.

The program reads lines from the user, combines them into one string, and calls analyze(). If analysis fails, it asks whether the user wants to try the semicolon correction. If the user agrees, it displays the changed code and analyzes it again. 6. Example tests
Test 1 — valid code
Input:
int age = 20;
float price = 12.5;
age = age + 1;
Expected result: no lexical, syntax, or semantic errors.
Test 2 — lexical error
Input:
int age = 20;
int score = 10 @ 2;
Expected result: a lexical error for the @ character.
Test 3 — syntax error
Input:
int age = 20
age = age + 1;
Expected result: a syntax error because the first statement is missing its semicolon. The correction option can try adding it.
Test 4 — undeclared variable
Input:
int age = 20;
price = 12;
Expected result: a semantic error because price has not been declared.
Test 5 — type error
Input:
int age = "twenty";
Expected result: a semantic error because a string value cannot be assigned to an integer variable. 7. Important limitations

- The project supports only the small language described above.
- It does not support functions, loops, conditions, arrays, comments, or many other language features.
- It reports errors but does not attempt full parser error recovery.
- The semicolon fixer is intentionally basic and can make inappropriate changes.
- It does not execute the analyzed source code.
- It does not generate machine code or bytecode.
- It is not a full compiler; it demonstrates the front-end analysis stages.

8. How to explain the project in class
   You can explain it in your own words along these lines:
   “I wrote a small compiler analyzer in Python for a custom language. I chose Python because it lets me focus on the compiler concepts without spending too much time on language-specific implementation details. The program does not use an AI model. I wrote the analysis rules myself.

First, the lexical analyzer converts source text into tokens. Next, a recursive-descent parser checks the structure of the tokens and represents expressions as tuples. Finally, semantic analysis uses a symbol table to check variable declarations and data types.

I also added a simple correction feature that tries to add missing semicolons. It is rule-based, and I run the analyzer again after the correction instead of assuming that the result is valid.”

Do not claim that it can automatically fix every kind of error. Explain that the current correction feature handles only one common, simple case. 9. Questions the instructor might ask
Why did you choose Python?

Python is readable and supports regular expressions, lists, dictionaries, and functions. Those are enough to implement a small lexer, parser, and semantic checker.

What is a token?

A token is a meaningful unit of source code, such as a keyword, identifier, number, operator, or semicolon.

What is the difference between syntax and semantic errors?

A syntax error means the code does not follow the grammar. A semantic error means the structure is acceptable, but a language rule is broken—for example, using an undeclared variable or assigning a string to an integer.

What is a symbol table?

It is a data structure that stores information about identifiers. This project uses a dictionary to store variable names and their types.

What is recursive descent?

It is a parsing technique in which functions represent grammar rules and call one another to recognize the input. Here, expression(), term(), and factor() work together to parse arithmetic expressions.

Does the correction feature use AI?

No. It applies a specific rule written in Python. It does not learn from data or call an AI model.

What would you improve next?

I would add more grammar rules, improve error recovery, track source positions more precisely, and implement additional correction rules that only run when the intended fix is reasonably clear.
Before submitting
Read the source code and make sure you can explain lexer(), Parser, semantic_check(), and analyze() without relying entirely on the README. Try changing a small rule yourself—for example, add a new operator or change a type-checking rule—and test what happens.

That will help you demonstrate that you understand how the project works and can develop it further.
