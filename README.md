# Mini Compiler Analyzer (Python)

A small educational project for a university **Compiler Design** course.

This project implements a simple compiler analyzer using Python. It analyzes source code written in a small custom programming language and checks it through three main stages:

1. **Lexical Analysis** – Identifies tokens and detects invalid characters.
2. **Syntax Analysis** – Checks whether the tokens follow the language grammar.
3. **Semantic Analysis** – Checks variable declarations, assignments, and basic data-type rules.

The project also includes a simple error-correction feature that attempts to add missing semicolons to non-empty lines and then analyzes the corrected code again.

**Important:** This is an educational compiler analyzer, not a complete compiler. It does not execute the submitted code or generate machine code. It does not use AI; all analysis and correction rules are implemented manually in Python.

---

# 1. Language Supported by This Project

The analyzer understands a small custom language with the following features:

| Feature | Description | Example |
|---|---|---|
| `int` | Integer variables | `int age = 20;` |
| `float` | Decimal variables | `float price = 12.5;` |
| `string` | Text variables | `string name = "Sara";` |
| Declarations | Creating variables | `int score = 100;` |
| Assignments | Updating variables | `score = 150;` |
| Numbers | Integer and decimal values | `10`, `3.5` |
| Strings | Text inside double quotes | `"Hello"` |
| Arithmetic | Addition, subtraction, multiplication, division | `a + b` |
| Parentheses | Grouping expressions | `(a + b) * 2` |
| Semicolons | Ending statements | `int x = 10;` |

### Example program

```python
int age = 20;
float price = 12.5;
string name = "Sara";

age = age + 1;
price = price * 2;
```

The language is intentionally small to make compiler concepts easier to understand.

---

# 2. Requirements

- Python 3
- No external Python packages are required.

The project uses Python's built-in `re` module for regular expressions.

---

# 3. How to Run the Project

1. Save the source code in a file named `mini_compiler.py`.
2. Open a terminal in the folder containing the file.
3. Run the following command:

```bash
python3 mini_compiler.py
```

4. Enter your source code, one line at a time.
5. Press Enter on an empty line to finish entering the code.
6. The analyzer will display the results of each analysis stage.

### Example input

```python
int age = 20;
age = age + 1;
```

Expected result:

```text
--- Lexical Analysis ---
No lexical errors found.

--- Syntax Analysis ---
No syntax errors found.

--- Semantic Analysis ---
No semantic errors found.

Code is valid!
```

If an error is detected, the program asks whether you want to try its missing-semicolon correction feature.

---

# 4. How the Program Works

The program follows the general structure of a compiler's front end.

```text
             Source Code
                  |
                  v
          Lexical Analysis
                  |
                  v
          Syntax Analysis
                  |
                  v
         Semantic Analysis
                  |
                  v
        Valid Code / Errors
                  |
                  v
       Optional Error Correction
                  |
                  v
             Re-analysis
```

Each stage depends on the previous one:

- The lexer converts source code characters into tokens.
- The parser checks the token sequence and builds a tree-like representation of expressions.
- The semantic analyzer checks variable declarations and data types.

If lexical or syntax analysis fails, the program stops the later stages. This prevents semantic analysis from running on code that could not be parsed successfully.

---

# 5. Explanation of the Source Code

The program is organized into simple Python functions. It does not use classes or object-oriented programming.

## A. Token Pattern

The program uses Python's `re` module, which provides regular expressions.

A regular expression is a pattern used to recognize specific sequences of characters.

The `TOKEN_PATTERN` recognizes the following token types:

| Token | Meaning | Example |
|---|---|---|
| SPACE | Whitespace characters | Spaces, tabs, newlines |
| NUMBER | Integer or decimal number | `12`, `3.5` |
| STRING | Text inside double quotes | `"Hello"` |
| ID | Variable name or keyword before checking | `age`, `total` |
| SYMBOL | Supported operators and punctuation | `=`, `+`, `;`, `(` |
| BAD | Any character that does not match the previous patterns | `@`, `#` |

The patterns are checked in order.

After recognizing an identifier, the lexer checks whether its value is one of the supported data types:

- `int`
- `float`
- `string`

If it is, its token type changes from `ID` to `TYPE`.

## B. `lexer(code)` — Lexical Analysis

This function reads the source code and returns two results:

- A list of tokens.
- A list of lexical error messages.

Each token is stored as a Python dictionary containing three fields:

```python
{
    "type": "NUMBER",
    "value": "20",
    "line": 1
}
```

These fields represent:

- `type`: The category of the token.
- `value`: The actual text found in the source code.
- `line`: The line number where the token appears.

For example, the source code:

```python
int age = 20;
```

produces tokens similar to:

```text
(TYPE, int)
(ID, age)
(SYMBOL, =)
(NUMBER, 20)
(SYMBOL, ;)
```

Whitespace is ignored because it normally separates tokens rather than representing meaningful instructions in this language.

The lexer also tracks line numbers so that errors can be reported with their locations.

At the end of the token list, it adds a special token:

```python
{
    "type": "EOF",
    "value": "EOF",
    "line": line
}
```

EOF means **End Of File** (or end of input).

The parser uses this token to know when it has finished reading the source code.

If a character matches the `BAD` pattern, the lexer reports a lexical error.

## C. Syntax Analysis — Functional Parser

In the previous version, syntax analysis was implemented using a `Parser` class.

In this version, the parser has been rewritten using ordinary Python functions. There are no classes or `self` variables.

The main idea is simple:

**Each parsing function receives the token list and the current position, then returns the parsed result and the updated position.**

For example:

```python
node, position = parse_factor(tokens, position)
```

Here:

- `tokens` contains all tokens generated by the lexer.
- `position` tells us which token is currently being examined.
- `node` contains the parsed result.
- The updated `position` tells the next function where to continue.

This replaces the old class-based approach, where the parser stored its position using `self.pos`.

### Main parsing functions

| Function | Responsibility |
|---|---|
| `current_token()` | Returns the token at the current position. |
| `eat()` | Checks the expected token type and advances the position. |
| `expect_symbol()` | Checks for a specific symbol such as `=` or `;`. |
| `parse_program()` | Reads statements until EOF. |
| `parse_statement()` | Recognizes variable declarations and assignments. |
| `parse_expression()` | Handles addition and subtraction. |
| `parse_term()` | Handles multiplication and division. |
| `parse_factor()` | Handles numbers, strings, variables, and parentheses. |

### How expressions are parsed

The parser uses three functions to handle arithmetic expressions:

**1. `parse_expression()`**

Handles:
- Addition (`+`)
- Subtraction (`-`)

**2. `parse_term()`**

Handles:
- Multiplication (`*`)
- Division (`/`)

**3. `parse_factor()`**

Handles:
- Numbers
- Strings
- Variable names
- Parenthesized expressions

Why are three functions necessary?

They implement **operator precedence**.

Multiplication and division must be evaluated before addition and subtraction.

For example:

```python
2 + 3 * 4
```

The parser understands this as:

```python
2 + (3 * 4)
```

Not:

```python
(2 + 3) * 4
```

### Understanding the parsing process

Consider this expression:

```python
age + 5 * 2
```

The parser processes it as follows:

1. `parse_expression()` starts parsing the expression.
2. It calls `parse_term()`.
3. `parse_term()` calls `parse_factor()` to read `age`.
4. It finds the multiplication operator in the next part of the expression and processes `5 * 2`.
5. Finally, `parse_expression()` combines the two parts using the addition operator.

### Expression representation

The parser returns tuples that represent simple tree-like structures.

For example:

```python
("number", "20")
```

Represents the number `20`.

```python
("variable", "age")
```

Represents the variable `age`.

```python
("bin", "+",
    ("variable", "age"),
    ("number", "1")
)
```

Represents:

```python
age + 1
```

The `bin` node represents a binary operation. It contains:

- The node type (`bin`).
- The operator (`+`).
- The left operand.
- The right operand.

These structures are passed to semantic analysis.

### Error handling

If the parser finds an unexpected token, it raises a `SyntaxError` with an error message and line number.

For example, if a semicolon is missing:

```python
int age = 20
```

The parser expects `;` but reaches EOF instead.

It reports the syntax error, and the main analysis function displays it.

## D. `semantic_check(statements)` — Semantic Analysis

A statement can be syntactically correct but still violate the language's rules.

For example:

```python
int age = "twenty";
```

The statement follows the correct syntax, but the variable is declared as an integer and receives a string value.

The semantic analyzer detects this problem.

### Symbol Table

The semantic analyzer uses a Python dictionary called `variables` as its symbol table.

A symbol table stores information about declared variables.

For example, after analyzing:

```python
int age = 20;
float price = 12.5;
```

The dictionary conceptually contains:

```python
{
    "age": "int",
    "price": "float"
}
```

This allows the analyzer to check whether variables exist and what their data types are.

### `expression_type()` function

This function determines the data type of an expression.

It checks the expression's tuple representation.

The rules are:

| Expression | Resulting type |
|---|---|
| Integer number | `int` |
| Decimal number | `float` |
| String literal | `string` |
| Declared variable | Its type from the symbol table |
| Arithmetic with integers | `int` |
| Arithmetic involving a float | `float` |

Arithmetic operations only accept numeric operands.

For example:

```python
int x = 10 + 5;
```

Is valid.

But:

```python
int x = "hello" + 5;
```

Produces a semantic error because arithmetic operations cannot use strings.

### What does semantic analysis check?

The semantic analyzer checks:

1. Using a variable before declaring it.
2. Declaring the same variable more than once.
3. Assigning incompatible data types.
4. Using strings in arithmetic expressions.

### Type compatibility

The project uses a simple type system.

Assigning an integer to a float variable is allowed:

```python
float price = 10;
```

But assigning a float to an integer variable is rejected:

```python
int age = 10.5;
```

Similarly, assigning a string to an integer variable is rejected:

```python
int age = "twenty";
```

## E. `fix_missing_semicolons(code)` — Basic Error Correction

This function provides one simple correction rule.

It:

1. Splits the source code into individual lines.
2. Checks each non-empty line.
3. Adds a semicolon if the line does not already end with one.
4. Combines the lines into the corrected source code.

Example:

Before correction:

```python
int age = 20
age = age + 1
```

After correction:

```python
int age = 20;
age = age + 1;
```

This is a basic rule-based correction, not an intelligent general-purpose repair system.

It may add semicolons in places where they are not appropriate. Therefore, the program analyzes the corrected code again instead of assuming the correction was successful.

## F. `analyze(code)` — Main Analysis Function

This function coordinates all three analysis stages.

Its workflow is:

1. Run the lexer.
2. If lexical errors are found, display them and stop.
3. If lexical analysis succeeds, run the parser.
4. If syntax errors are found, display them and stop.
5. If parsing succeeds, run semantic analysis.
6. Display semantic errors or report that the code is valid.

The function returns:

- `True` if all three analysis stages succeed.
- `False` if an error is detected.

This function connects the different parts of the project.

## G. Main Program — User Interaction

The program uses:

```python
if __name__ == "__main__":
```

This condition makes sure that the interactive part runs when the Python file is executed directly.

The main program:

1. Asks the user to enter source code.
2. Reads the input line by line.
3. Combines all lines into one string.
4. Calls `analyze(code)`.
5. If analysis fails, asks whether the user wants to try adding missing semicolons.
6. If the user agrees, displays the corrected code and analyzes it again.

---

# 6. Example Tests

These examples can be used to test the analyzer.

### Test 1 — Valid Code

Input:

```python
int age = 20;
float price = 12.5;
age = age + 1;
```

Expected result:

```text
No lexical errors found.
No syntax errors found.
No semantic errors found.
Code is valid!
```

### Test 2 — Lexical Error

Input:

```python
int age = 20;
int score = 10 @ 2;
```

Expected result:

```text
Lexical error at line 2: Invalid character '@'
```

### Test 3 — Syntax Error

Input:

```python
int age = 20
age = age + 1;
```

Expected result:

A syntax error because the first statement is missing its semicolon.

The correction option can try adding it.

### Test 4 — Undeclared Variable

Input:

```python
int age = 20;
price = 12;
```

Expected result:

```text
Semantic error at line 2:
Variable 'price' is not declared
```

### Test 5 — Type Error

Input:

```python
int age = "twenty";
```

Expected result:

```text
Semantic error at line 1:
Cannot assign string to int
```

### Test 6 — Duplicate Declaration

Input:

```python
int age = 20;
int age = 25;
```

Expected result:

```text
Semantic error at line 2:
Variable 'age' is already declared
```

### Test 7 — Operator Precedence

Input:

```python
int result = 2 + 3 * 4;
```

Expected result:

The expression is syntactically valid, and its resulting type is `int`.

Multiplication is parsed before addition.

---

# 7. Important Limitations

This project is intentionally limited to basic compiler concepts.

It currently:

- Supports only the small custom language described above.
- Does not support functions, loops, conditions, arrays, or comments.
- Does not support unary operators such as `-5`.
- Does not implement full parser error recovery.
- Uses a basic semicolon correction rule.
- Does not execute the analyzed source code.
- Does not generate machine code or bytecode.
- Does not use an AI model.

It is not a complete compiler. It demonstrates the main front-end stages of compiler design.

---

# 8. How to Explain the Project in Class

You can explain the project using the following description:

"I developed a small compiler analyzer in Python for my Compiler Design course. I chose Python because its readable syntax and built-in features, such as regular expressions, lists, dictionaries, and functions, make it easier to focus on compiler concepts.

The project analyzes source code through three stages.

First, the lexical analyzer converts the source code into tokens. Next, the syntax analyzer uses a recursive-descent parsing technique to check the grammar and represent expressions using tuples.

Unlike a class-based parser, I implemented the parser using simple functions. Each function receives the token list and the current position and returns the updated position after parsing.

Finally, semantic analysis uses a symbol table implemented as a dictionary to check variable declarations and data types.

I also implemented a simple error-correction feature that attempts to add missing semicolons. It uses a predefined Python rule rather than an AI model, and the program analyzes the corrected code again to check whether the correction was successful."

Do not claim that the program automatically fixes every kind of error. Its correction feature handles only one specific case: missing semicolons.

---

# 9. Questions the Instructor Might Ask

### 1. Why did you choose Python?

Python is readable and provides built-in tools such as regular expressions, lists, dictionaries, and functions. These are sufficient for implementing a small lexer, parser, and semantic analyzer.

### 2. What is a token?

A token is a meaningful unit of source code, such as a keyword, identifier, number, operator, or semicolon.

### 3. What is the difference between syntax and semantic errors?

A syntax error means the code does not follow the grammar rules.

A semantic error means the code has a valid structure but violates a language rule.

For example:

```python
int age = "twenty";
```

This has valid syntax but an incompatible data type.

### 4. What is a symbol table?

A symbol table is a data structure that stores information about identifiers.

In this project, a Python dictionary stores variable names and their data types.

### 5. What is recursive descent parsing?

Recursive descent is a parsing technique where separate functions represent grammar rules and call one another to recognize the input.

In this project:

- `parse_expression()` handles addition and subtraction.
- `parse_term()` handles multiplication and division.
- `parse_factor()` handles individual values and parentheses.

### 6. Why did you remove the Parser class?

I wanted to implement syntax analysis using basic Python functions instead of object-oriented programming.

The parser's current position is passed as an argument to each function and returned after parsing. This allows the functions to work together without storing state inside a class.

### 7. What does EOF mean?

EOF stands for End Of File or end of input.

It is a special token added by the lexer to indicate that there are no more tokens to process.

### 8. Does the correction feature use AI?

No. It uses a predefined rule written in Python to add semicolons to non-empty lines that do not already end with one.

### 9. What would you improve next?

I would add more grammar rules, improve syntax error recovery, support additional operators and statements, track source positions more precisely, and implement safer correction rules.

---

# 10. Before Submitting

Before submitting the project, make sure you can explain these functions:

- `lexer()`
- `current_token()`
- `eat()`
- `expect_symbol()`
- `parse_factor()`
- `parse_term()`
- `parse_expression()`
- `parse_statement()`
- `parse_program()`
- `expression_type()`
- `semantic_check()`
- `fix_missing_semicolons()`
- `analyze()`

Try changing a small rule yourself, such as adding a new operator or changing a type-checking rule, and test what happens.

Understanding how these functions work together is more important than simply memorizing the code.

---

# نسخه فارسی — تحلیلگر کامپایلر کوچک با پایتون

یک پروژه آموزشی کوچک برای درس **طراحی کامپایلر (Compiler Design)**.

این پروژه یک تحلیلگر کامپایلر ساده با استفاده از زبان پایتون پیاده‌سازی می‌کند. برنامه کدهایی را که با یک زبان برنامه‌نویسی کوچک و اختصاصی نوشته شده‌اند، بررسی می‌کند و آن‌ها را در سه مرحله اصلی تحلیل می‌کند:

1. **تحلیل لغوی (Lexical Analysis):** شناسایی توکن‌ها و تشخیص کاراکترهای نامعتبر.
2. **تحلیل نحوی (Syntax Analysis):** بررسی اینکه آیا توکن‌ها از قواعد دستوری زبان پیروی می‌کنند یا خیر.
3. **تحلیل معنایی (Semantic Analysis):** بررسی تعریف متغیرها، انتساب مقادیر و سازگاری انواع داده.

همچنین یک قابلیت ساده اصلاح خطا وجود دارد که تلاش می‌کند در انتهای خطوط غیرخالی که فاقد نقطه‌ویرگول هستند، `;` اضافه کند و سپس کد اصلاح‌شده را دوباره تحلیل کند.

**نکته مهم:** این پروژه یک تحلیلگر آموزشی است، نه یک کامپایلر کامل. برنامه کد ورودی را اجرا نمی‌کند و کد ماشین تولید نمی‌کند. همچنین از هیچ مدل هوش مصنوعی استفاده نشده است؛ تمام قوانین تحلیل و اصلاح خطا مستقیماً با پایتون پیاده‌سازی شده‌اند.

---

# ۱. قابلیت‌های زبان پشتیبانی‌شده

تحلیلگر از یک زبان برنامه‌نویسی کوچک با قابلیت‌های زیر پشتیبانی می‌کند:

| قابلیت | توضیحات | مثال |
|---|---|---|
| `int` | متغیرهای عدد صحیح | `int age = 20;` |
| `float` | متغیرهای اعشاری | `float price = 12.5;` |
| `string` | متغیرهای متنی | `string name = "Sara";` |
| تعریف متغیر | ایجاد متغیر جدید | `int score = 100;` |
| انتساب | تغییر مقدار متغیر | `score = 150;` |
| اعداد | اعداد صحیح و اعشاری | `10`، `3.5` |
| رشته‌ها | متن داخل دابل کوتیشن | `"Hello"` |
| عملیات ریاضی | جمع، تفریق، ضرب و تقسیم | `a + b` |
| پرانتز | گروه‌بندی عبارات | `(a + b) * 2` |
| نقطه‌ویرگول | پایان دستورات | `int x = 10;` |

### نمونه برنامه

```python
int age = 20;
float price = 12.5;
string name = "Sara";

age = age + 1;
price = price * 2;
```

این زبان عمداً ساده طراحی شده است تا درک مفاهیم کامپایلر آسان‌تر باشد.

---

# ۲. پیش‌نیازها

- Python 3
- بدون نیاز به نصب کتابخانه‌های خارجی

این پروژه از ماژول داخلی `re` پایتون برای کار با عبارات منظم استفاده می‌کند.

---

# ۳. نحوه اجرای پروژه

۱. کد برنامه را در فایلی با نام `mini_compiler.py` ذخیره کنید.

۲. ترمینال را در پوشه‌ای که فایل در آن قرار دارد باز کنید.

۳. دستور زیر را اجرا کنید:

```bash
python3 mini_compiler.py
```

۴. کد موردنظر را خط به خط وارد کنید.

۵. برای پایان دادن به ورودی، یک بار Enter را در یک خط خالی فشار دهید.

۶. نتایج تحلیل برنامه نمایش داده می‌شوند.

### نمونه ورودی

```python
int age = 20;
age = age + 1;
```

خروجی مورد انتظار:

```text
--- Lexical Analysis ---
No lexical errors found.

--- Syntax Analysis ---
No syntax errors found.

--- Semantic Analysis ---
No semantic errors found.

Code is valid!
```

اگر خطایی شناسایی شود، برنامه از کاربر می‌پرسد که آیا می‌خواهد قابلیت اصلاح نقطه‌ویرگول را امتحان کند یا خیر.

---

# ۴. نحوه عملکرد برنامه

این برنامه از ساختار کلی بخش ابتدایی یک کامپایلر پیروی می‌کند.

```text
          کد منبع (Source Code)
                    |
                    v
             تحلیل لغوی
          (Lexical Analysis)
                    |
                    v
             تحلیل نحوی
          (Syntax Analysis)
                    |
                    v
            تحلیل معنایی
         (Semantic Analysis)
                    |
                    v
             کد معتبر / خطا
                    |
                    v
           اصلاح اختیاری خطا
                    |
                    v
              تحلیل مجدد
```

هر مرحله به مرحله قبلی وابسته است:

- تحلیلگر لغوی، کاراکترهای کد منبع را به توکن تبدیل می‌کند.
- تحلیلگر نحوی، ترتیب توکن‌ها را بررسی کرده و برای عبارات، ساختارهای درخت‌مانند ایجاد می‌کند.
- تحلیلگر معنایی، تعریف متغیرها و سازگاری انواع داده را بررسی می‌کند.

اگر در تحلیل لغوی یا نحوی خطایی پیدا شود، برنامه مراحل بعدی را اجرا نمی‌کند.

---

# ۵. توضیح بخش‌های مختلف کد

## الف) الگوی توکن‌ها (Token Pattern)

برنامه از ماژول `re` پایتون استفاده می‌کند.

عبارت منظم یا Regular Expression الگویی است که برای شناسایی دنباله‌های مشخصی از کاراکترها استفاده می‌شود.

الگوی `TOKEN_PATTERN` انواع توکن‌های زیر را شناسایی می‌کند:

| نوع توکن | مفهوم | مثال |
|---|---|---|
| SPACE | کاراکترهای فاصله | فاصله، Tab و خط جدید |
| NUMBER | عدد صحیح یا اعشاری | `12`، `3.5` |
| STRING | متن داخل دابل کوتیشن | `"Hello"` |
| ID | نام متغیر یا کلمه کلیدی قبل از بررسی | `age`، `total` |
| SYMBOL | عملگرها و علائم مجاز | `=`، `+`، `;`، `(` |
| BAD | کاراکترهای غیرمجاز | `@`، `#` |

الگوها به ترتیب بررسی می‌شوند.

پس از شناسایی یک شناسه، تحلیلگر بررسی می‌کند که آیا مقدار آن یکی از انواع داده پشتیبانی‌شده است یا خیر:

- `int`
- `float`
- `string`

اگر چنین باشد، نوع توکن از `ID` به `TYPE` تغییر می‌کند.

## ب) تابع `lexer(code)` — تحلیل لغوی

این تابع کد منبع را دریافت می‌کند و دو نتیجه برمی‌گرداند:

- فهرستی از توکن‌ها.
- فهرستی از پیام‌های خطای لغوی.

هر توکن به شکل یک دیکشنری پایتون ذخیره می‌شود:

```python
{
    "type": "NUMBER",
    "value": "20",
    "line": 1
}
```

این سه فیلد عبارت‌اند از:

- `type`: نوع توکن.
- `value`: مقدار واقعی کاراکتر یا عبارت شناسایی‌شده.
- `line`: شماره خطی که توکن در آن قرار دارد.

برای مثال، کد زیر:

```python
int age = 20;
```

توکن‌هایی مشابه موارد زیر تولید می‌کند:

```text
(TYPE, int)
(ID, age)
(SYMBOL, =)
(NUMBER, 20)
(SYMBOL, ;)
```

فاصله‌ها نادیده گرفته می‌شوند، زیرا در این زبان صرفاً برای جدا کردن توکن‌ها استفاده می‌شوند.

تحلیلگر همچنین شماره خطوط را دنبال می‌کند تا بتواند محل دقیق خطاها را نمایش دهد.

در انتهای فهرست توکن‌ها، یک توکن ویژه با نام `EOF` اضافه می‌شود.

EOF مخفف End Of File یا پایان ورودی است.

تحلیلگر نحوی از این توکن برای تشخیص پایان کد استفاده می‌کند.

اگر کاراکتری با الگوی `BAD` مطابقت داشته باشد، یک خطای لغوی گزارش می‌شود.

## ج) تحلیل نحوی 

ایده اصلی بسیار ساده است:

**هر تابع تحلیلگر، فهرست توکن‌ها و موقعیت فعلی را دریافت می‌کند و پس از پردازش، نتیجه و موقعیت جدید را برمی‌گرداند.**

برای مثال:

```python
node, position = parse_factor(tokens, position)
```

در اینجا:

- `tokens`: فهرست توکن‌های تولیدشده توسط تحلیلگر لغوی.
- `position`: موقعیت توکنی که در حال حاضر بررسی می‌شود.
- `node`: نتیجه تحلیل.
- `position` جدید: موقعیتی که تابع بعدی باید از آن ادامه دهد.

### توابع اصلی تحلیل نحوی

| تابع | وظیفه |
|---|---|
| `current_token()` | برگرداندن توکن موجود در موقعیت فعلی |
| `eat()` | بررسی نوع مورد انتظار توکن و حرکت به توکن بعدی |
| `expect_symbol()` | بررسی وجود یک نماد مشخص مانند `=` یا `;` |
| `parse_program()` | خواندن دستورات تا رسیدن به EOF |
| `parse_statement()` | شناسایی تعریف متغیر یا انتساب مقدار |
| `parse_expression()` | پردازش جمع و تفریق |
| `parse_term()` | پردازش ضرب و تقسیم |
| `parse_factor()` | پردازش اعداد، رشته‌ها، متغیرها و پرانتزها |

### نحوه تحلیل عبارات ریاضی

تحلیلگر برای پردازش عبارات ریاضی از سه تابع استفاده می‌کند:

**۱. تابع `parse_expression()`**

مسئول پردازش:
- جمع (`+`)
- تفریق (`-`)

**۲. تابع `parse_term()`**

مسئول پردازش:
- ضرب (`*`)
- تقسیم (`/`)

**۳. تابع `parse_factor()`**

مسئول پردازش:
- اعداد
- رشته‌ها
- نام متغیرها
- عبارات داخل پرانتز

چرا از سه تابع مختلف استفاده می‌کنیم؟

این توابع برای پیاده‌سازی مفهوم **تقدم عملگرها (Operator Precedence)** استفاده می‌شوند.

عملیات ضرب و تقسیم باید قبل از جمع و تفریق پردازش شوند.

برای مثال:

```python
2 + 3 * 4
```

تحلیلگر این عبارت را به شکل زیر درک می‌کند:

```python
2 + (3 * 4)
```

نه به شکل:

```python
(2 + 3) * 4
```

### درک مراحل تحلیل یک عبارت

فرض کنید عبارت زیر را داریم:

```python
age + 5 * 2
```

مراحل پردازش به این صورت است:

۱. تابع `parse_expression()` تحلیل عبارت را شروع می‌کند.

۲. این تابع، `parse_term()` را فراخوانی می‌کند.

۳. تابع `parse_term()` از `parse_factor()` برای خواندن `age` استفاده می‌کند.

۴. سپس عملگر ضرب را شناسایی کرده و عبارت `5 * 2` را پردازش می‌کند.

۵. در نهایت، تابع `parse_expression()` دو بخش را با عملگر جمع ترکیب می‌کند.

### نمایش ساختار عبارات

تحلیلگر نحوی نتیجه را به شکل Tupleهایی ذخیره می‌کند که ساختاری شبیه درخت دارند.

برای مثال:

```python
("number", "20")
```

نمایانگر عدد ۲۰ است.

```python
("variable", "age")
```

نمایانگر متغیر `age` است.

```python
("bin", "+",
    ("variable", "age"),
    ("number", "1")
)
```

نمایانگر عبارت زیر است:

```python
age + 1
```

گره `bin` نشان‌دهنده یک عملیات دودویی است و شامل موارد زیر می‌شود:

- نوع گره (`bin`)
- عملگر (`+`)
- عملوند سمت چپ
- عملوند سمت راست

این ساختارها در مرحله تحلیل معنایی استفاده می‌شوند.

### مدیریت خطاها

اگر تحلیلگر با توکن غیرمنتظره‌ای مواجه شود، یک خطای `SyntaxError` همراه با پیام و شماره خط ایجاد می‌کند.

برای مثال، در کد زیر:

```python
int age = 20
```

نقطه‌ویرگول وجود ندارد و تحلیلگر به جای آن با توکن `EOF` مواجه می‌شود.

در نتیجه خطای نحوی گزارش می‌شود و تابع اصلی آن را نمایش می‌دهد.

## د) تابع `semantic_check(statements)` — تحلیل معنایی

ممکن است یک دستور از نظر ساختار نحوی صحیح باشد، اما قوانین زبان را نقض کند.

برای مثال:

```python
int age = "twenty";
```

ساختار این دستور صحیح است، اما متغیر به‌صورت عدد صحیح تعریف شده و مقدار متنی دریافت کرده است.

تحلیلگر معنایی این مشکل را شناسایی می‌کند.

### جدول نمادها (Symbol Table)

تحلیلگر معنایی از یک دیکشنری پایتون به نام `variables` به‌عنوان جدول نمادها استفاده می‌کند.

جدول نمادها اطلاعات مربوط به متغیرهای تعریف‌شده را ذخیره می‌کند.

برای مثال، پس از تحلیل کد زیر:

```python
int age = 20;
float price = 12.5;
```

دیکشنری به‌صورت مفهومی شامل اطلاعات زیر خواهد بود:

```python
{
    "age": "int",
    "price": "float"
}
```

این اطلاعات به تحلیلگر کمک می‌کند تا بررسی کند آیا متغیر وجود دارد و نوع داده آن چیست.

### تابع `expression_type()`

این تابع نوع داده یک عبارت را مشخص می‌کند.

قوانین آن به این صورت هستند:

| عبارت | نوع داده |
|---|---|
| عدد صحیح | `int` |
| عدد اعشاری | `float` |
| رشته متنی | `string` |
| متغیر تعریف‌شده | نوع ذخیره‌شده در جدول نمادها |
| عملیات ریاضی با اعداد صحیح | `int` |
| عملیات ریاضی شامل عدد اعشاری | `float` |

عملیات ریاضی فقط با عملوندهای عددی مجاز هستند.

برای مثال:

```python
int x = 10 + 5;
```

معتبر است.

اما:

```python
int x = "hello" + 5;
```

خطای معنایی ایجاد می‌کند، زیرا عملیات ریاضی نمی‌تواند از رشته متنی استفاده کند.

### چه خطاهایی بررسی می‌شوند؟

تحلیلگر معنایی موارد زیر را بررسی می‌کند:

۱. استفاده از متغیر قبل از تعریف آن.

۲. تعریف مجدد یک متغیر با نام تکراری.

۳. انتساب نوع داده ناسازگار.

۴. استفاده از رشته‌ها در عملیات ریاضی.

### سازگاری انواع داده

این پروژه از یک سیستم نوع‌دهی ساده استفاده می‌کند.

انتساب عدد صحیح به متغیر اعشاری مجاز است:

```python
float price = 10;
```

اما انتساب عدد اعشاری به متغیر عدد صحیح مجاز نیست:

```python
int age = 10.5;
```

همچنین انتساب رشته به متغیر عدد صحیح مجاز نیست:

```python
int age = "twenty";
```

## هـ) تابع `fix_missing_semicolons(code)` — اصلاح ساده خطا

این تابع یک قانون ساده برای اصلاح کد پیاده‌سازی می‌کند.

مراحل عملکرد آن:

۱. کد را به خطوط جداگانه تقسیم می‌کند.

۲. هر خط غیرخالی را بررسی می‌کند.

۳. اگر خط به نقطه‌ویرگول ختم نشده باشد، `;` به انتهای آن اضافه می‌کند.

۴. خطوط را دوباره به یک رشته واحد تبدیل می‌کند.

مثال:

قبل از اصلاح:

```python
int age = 20
age = age + 1
```

بعد از اصلاح:

```python
int age = 20;
age = age + 1;
```

این یک روش ساده مبتنی بر قوانین از پیش تعریف‌شده است، نه یک سیستم هوشمند برای اصلاح تمام خطاها.

ممکن است در بعضی شرایط، اضافه کردن نقطه‌ویرگول مناسب نباشد. به همین دلیل برنامه کد اصلاح‌شده را دوباره تحلیل می‌کند و موفقیت اصلاح را از قبل فرض نمی‌کند.

## و) تابع `analyze(code)` — تابع اصلی تحلیل

این تابع تمام مراحل تحلیل را به یکدیگر متصل می‌کند.

مراحل عملکرد آن:

۱. اجرای تحلیلگر لغوی.

۲. در صورت وجود خطای لغوی، نمایش خطاها و توقف.

۳. در صورت موفقیت تحلیل لغوی، اجرای تحلیلگر نحوی.

۴. در صورت وجود خطای نحوی، نمایش خطا و توقف.

۵. در صورت موفقیت تحلیل نحوی، اجرای تحلیلگر معنایی.

۶. نمایش خطاهای معنایی یا اعلام معتبر بودن کد.

این تابع دو مقدار ممکن برمی‌گرداند:

- `True`: هر سه مرحله تحلیل با موفقیت انجام شده‌اند.
- `False`: حداقل یک خطا شناسایی شده است.

این تابع بخش‌های مختلف پروژه را به یکدیگر متصل می‌کند.

## ز) بخش اصلی برنامه — تعامل با کاربر

برنامه از شرط زیر استفاده می‌کند:

```python
if __name__ == "__main__":
```

این شرط باعث می‌شود بخش تعاملی برنامه زمانی اجرا شود که فایل پایتون مستقیماً اجرا شده باشد.

وظایف بخش اصلی برنامه:

۱. دریافت کد از کاربر.

۲. خواندن ورودی خط به خط.

۳. تبدیل خطوط ورودی به یک رشته واحد.

۴. فراخوانی تابع `analyze(code)`.

۵. در صورت وجود خطا، پرسیدن اینکه آیا کاربر می‌خواهد اصلاح نقطه‌ویرگول را امتحان کند یا خیر.

۶. در صورت موافقت کاربر، نمایش کد اصلاح‌شده و تحلیل مجدد آن.

---

# ۶. نمونه تست‌ها

برای بررسی عملکرد برنامه می‌توان از نمونه‌های زیر استفاده کرد.

### تست ۱ — کد معتبر

ورودی:

```python
int age = 20;
float price = 12.5;
age = age + 1;
```

خروجی مورد انتظار:

```text
No lexical errors found.
No syntax errors found.
No semantic errors found.
Code is valid!
```

### تست ۲ — خطای لغوی

ورودی:

```python
int age = 20;
int score = 10 @ 2;
```

خروجی مورد انتظار:

```text
Lexical error at line 2: Invalid character '@'
```

### تست ۳ — خطای نحوی

ورودی:

```python
int age = 20
age = age + 1;
```

خروجی مورد انتظار:

خطای نحوی به دلیل نبود نقطه‌ویرگول در دستور اول.

قابلیت اصلاح می‌تواند برای اضافه کردن آن تلاش کند.

### تست ۴ — متغیر تعریف‌نشده

ورودی:

```python
int age = 20;
price = 12;
```

خروجی مورد انتظار:

```text
Semantic error at line 2:
Variable 'price' is not declared
```

### تست ۵ — خطای نوع داده

ورودی:

```python
int age = "twenty";
```

خروجی مورد انتظار:

```text
Semantic error at line 1:
Cannot assign string to int
```

### تست ۶ — تعریف مجدد متغیر

ورودی:

```python
int age = 20;
int age = 25;
```

خروجی مورد انتظار:

```text
Semantic error at line 2:
Variable 'age' is already declared
```

### تست ۷ — تقدم عملگرها

ورودی:

```python
int result = 2 + 3 * 4;
```

خروجی مورد انتظار:

عبارت از نظر نحوی معتبر است و نوع داده نتیجه آن `int` خواهد بود.

عملیات ضرب قبل از جمع پردازش می‌شود.

---

# ۷. محدودیت‌های پروژه

این پروژه عمداً برای آموزش مفاهیم ابتدایی کامپایلر طراحی شده است.

محدودیت‌های فعلی:

- فقط از زبان کوچک اختصاصی تعریف‌شده در این پروژه پشتیبانی می‌کند.
- از توابع، حلقه‌ها، شرط‌ها، آرایه‌ها و کامنت‌ها پشتیبانی نمی‌کند.
- از عملگرهای یکانی مانند `-5` پشتیبانی نمی‌کند.
- بازیابی کامل پس از خطاهای نحوی را پیاده‌سازی نکرده است.
- از یک قانون ساده برای اصلاح نقطه‌ویرگول استفاده می‌کند.
- کد تحلیل‌شده را اجرا نمی‌کند.
- کد ماشین یا بایت‌کد تولید نمی‌کند.
- از هیچ مدل هوش مصنوعی استفاده نمی‌کند.

این پروژه یک کامپایلر کامل نیست؛ بلکه مراحل اصلی بخش ابتدایی طراحی کامپایلر را نمایش می‌دهد.

---

# ۸. نحوه معرفی پروژه در کلاس

برای معرفی پروژه می‌توان از توضیح زیر استفاده کرد:

«من برای درس طراحی کامپایلر، یک تحلیلگر کامپایلر کوچک با استفاده از پایتون پیاده‌سازی کردم.

پایتون را انتخاب کردم، چون ساختار خوانا و امکانات داخلی آن مانند Regular Expressions، لیست‌ها، دیکشنری‌ها و توابع، باعث می‌شوند بتوانم روی مفاهیم کامپایلر تمرکز کنم.

این پروژه کد ورودی را در سه مرحله تحلیل می‌کند.

ابتدا تحلیلگر لغوی، کد منبع را به توکن تبدیل می‌کند. سپس تحلیلگر نحوی با استفاده از روش Recursive Descent Parsing، قواعد دستوری را بررسی کرده و عبارات را به شکل Tuple نمایش می‌دهد.

برخلاف نسخه قبلی که از کلاس استفاده می‌کرد، در این نسخه تحلیلگر نحوی با توابع ساده پیاده‌سازی شده است. هر تابع فهرست توکن‌ها و موقعیت فعلی را دریافت می‌کند و پس از پردازش، موقعیت جدید را برمی‌گرداند.

در نهایت، تحلیل معنایی با استفاده از جدول نمادها که توسط یک دیکشنری پیاده‌سازی شده است، تعریف متغیرها و سازگاری انواع داده را بررسی می‌کند.

همچنین یک قابلیت ساده اصلاح خطا اضافه کردم که تلاش می‌کند نقطه‌ویرگول‌های فراموش‌شده را اضافه کند. این قابلیت بر اساس قوانین از پیش تعریف‌شده در پایتون کار می‌کند و از هوش مصنوعی استفاده نمی‌کند. پس از اصلاح نیز برنامه کد را دوباره تحلیل می‌کند تا مشخص شود آیا اصلاح موفق بوده است یا خیر.»
