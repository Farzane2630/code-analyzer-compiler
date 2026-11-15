
import re


# ==========================================
# 1. LEXICAL ANALYSIS
# ==========================================

TOKEN_PATTERN = re.compile(
    r'(?P<SPACE>\s+)'
    r'|(?P<NUMBER>\d+(\.\d+)?)'
    r'|(?P<STRING>"[^"\n]*")'
    r'|(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
    r'|(?P<SYMBOL>[=+\-*/();])'
    r'|(?P<BAD>.)'
)


def lexer(code):
    tokens = []
    errors = []
    line = 1

    for match in TOKEN_PATTERN.finditer(code):

        kind = match.lastgroup
        value = match.group()

        if kind == "SPACE":
            line += value.count("\n")
            continue

        if kind == "BAD":
            errors.append(
                f"Lexical error at line {line}: "
                f"Invalid character '{value}'"
            )
            continue

        if kind == "ID":
            if value in ("int", "float", "string"):
                kind = "TYPE"

        tokens.append({
            "type": kind,
            "value": value,
            "line": line
        })

    tokens.append({
        "type": "EOF",
        "value": "EOF",
        "line": line
    })

    return tokens, errors


# ==========================================
# 2. SYNTAX ANALYSIS
# ==========================================

def current_token(tokens, position):
    return tokens[position]


def eat(tokens, position, expected):
    token = current_token(tokens, position)

    if token["type"] != expected:
        raise SyntaxError(
            f"Syntax error at line {token['line']}: "
            f"Expected {expected}, got '{token['value']}'"
        )

    return token, position + 1


def expect_symbol(tokens, position, symbol):
    token = current_token(tokens, position)

    if token["type"] != "SYMBOL" or token["value"] != symbol:
        raise SyntaxError(
            f"Syntax error at line {token['line']}: "
            f"Expected '{symbol}'"
        )

    return position + 1


def parse_factor(tokens, position):
    token = current_token(tokens, position)

    if token["type"] == "NUMBER":
        return ("number", token["value"]), position + 1

    if token["type"] == "STRING":
        return ("string", token["value"]), position + 1

    if token["type"] == "ID":
        return ("variable", token["value"]), position + 1

    if token["type"] == "SYMBOL" and token["value"] == "(":
        position += 1

        node, position = parse_expression(tokens, position)

        position = expect_symbol(tokens, position, ")")

        return node, position

    raise SyntaxError(
        f"Syntax error at line {token['line']}: "
        f"Expected a value, got '{token['value']}'"
    )


def parse_term(tokens, position):
    node, position = parse_factor(tokens, position)

    while (
        current_token(tokens, position)["type"] == "SYMBOL"
        and current_token(tokens, position)["value"] in ("*", "/")
    ):
        operator = current_token(tokens, position)["value"]
        position += 1

        right, position = parse_factor(tokens, position)

        node = ("bin", operator, node, right)

    return node, position


def parse_expression(tokens, position):
    node, position = parse_term(tokens, position)

    while (
        current_token(tokens, position)["type"] == "SYMBOL"
        and current_token(tokens, position)["value"] in ("+", "-")
    ):
        operator = current_token(tokens, position)["value"]
        position += 1

        right, position = parse_term(tokens, position)

        node = ("bin", operator, node, right)

    return node, position


def parse_statement(tokens, position):
    token = current_token(tokens, position)

    # Variable declaration
    if token["type"] == "TYPE":

        var_type, position = eat(tokens, position, "TYPE")

        name, position = eat(tokens, position, "ID")

        position = expect_symbol(tokens, position, "=")

        expression, position = parse_expression(tokens, position)

        position = expect_symbol(tokens, position, ";")

        statement = (
            "declare",
            var_type["value"],
            name["value"],
            expression,
            token["line"]
        )

        return statement, position

    # Variable assignment
    elif token["type"] == "ID":

        name, position = eat(tokens, position, "ID")

        position = expect_symbol(tokens, position, "=")

        expression, position = parse_expression(tokens, position)

        position = expect_symbol(tokens, position, ";")

        statement = (
            "assign",
            name["value"],
            expression,
            token["line"]
        )

        return statement, position

    raise SyntaxError(
        f"Syntax error at line {token['line']}: "
        f"Unexpected '{token['value']}'"
    )


def parse_program(tokens):
    statements = []
    position = 0

    while current_token(tokens, position)["type"] != "EOF":

        statement, position = parse_statement(tokens, position)

        statements.append(statement)

    return statements


# ==========================================
# 3. SEMANTIC ANALYSIS
# ==========================================

def expression_type(node, variables, errors, line):

    kind = node[0]

    if kind == "number":

        if "." in node[1]:
            return "float"

        return "int"

    if kind == "string":
        return "string"

    if kind == "variable":

        name = node[1]

        if name not in variables:
            errors.append(
                f"Semantic error at line {line}: "
                f"Variable '{name}' is not declared"
            )

            return None

        return variables[name]

    if kind == "bin":

        left_type = expression_type(
            node[2], variables, errors, line
        )

        right_type = expression_type(
            node[3], variables, errors, line
        )

        if left_type is None or right_type is None:
            return None

        if left_type not in ("int", "float") or \
                right_type not in ("int", "float"):

            errors.append(
                f"Semantic error at line {line}: "
                f"Arithmetic requires numeric values"
            )

            return None

        if "float" in (left_type, right_type):
            return "float"

        return "int"


def semantic_check(statements):

    variables = {}
    errors = []

    for statement in statements:

        kind = statement[0]
        line = statement[-1]

        # Variable declaration
        if kind == "declare":

            _, var_type, name, expr, line = statement

            if name in variables:

                errors.append(
                    f"Semantic error at line {line}: "
                    f"Variable '{name}' is already declared"
                )

                continue

            actual_type = expression_type(
                expr, variables, errors, line
            )

            if actual_type is not None:

                if actual_type == var_type or (
                    var_type == "float" and actual_type == "int"
                ):

                    variables[name] = var_type

                else:

                    errors.append(
                        f"Semantic error at line {line}: "
                        f"Cannot assign {actual_type} to {var_type}"
                    )

        # Variable assignment
        elif kind == "assign":

            _, name, expr, line = statement

            if name not in variables:

                errors.append(
                    f"Semantic error at line {line}: "
                    f"Variable '{name}' is not declared"
                )

                continue

            actual_type = expression_type(
                expr, variables, errors, line
            )

            expected_type = variables[name]

            if actual_type is not None:

                if actual_type != expected_type and not (
                    expected_type == "float" and actual_type == "int"
                ):

                    errors.append(
                        f"Semantic error at line {line}: "
                        f"Cannot assign {actual_type} "
                        f"to {expected_type}"
                    )

    return errors


# ==========================================
# 4. SAFE ERROR CORRECTION
# ==========================================

def fix_missing_semicolons(code):

    lines = code.splitlines()
    fixed_lines = []

    for line in lines:

        stripped = line.rstrip()

        if stripped and not stripped.endswith(";"):
            stripped += ";"

        fixed_lines.append(stripped)

    return "\n".join(fixed_lines)


# ==========================================
# 5. MAIN ANALYSIS FUNCTION
# ==========================================

def analyze(code):

    # Lexical Analysis
    tokens, lexical_errors = lexer(code)

    print("\n--- Lexical Analysis ---")

    if lexical_errors:

        for error in lexical_errors:
            print(error)

        return False

    print("No lexical errors found.")

    print("Tokens:", [
        (token["type"], token["value"])
        for token in tokens
    ])

    # Syntax Analysis
    print("\n--- Syntax Analysis ---")

    try:

        statements = parse_program(tokens)

        print("No syntax errors found.")

    except SyntaxError as error:

        print(error)

        return False

    # Semantic Analysis
    print("\n--- Semantic Analysis ---")

    semantic_errors = semantic_check(statements)

    if semantic_errors:

        for error in semantic_errors:
            print(error)

        return False

    print("No semantic errors found.")

    print("\nCode is valid!")

    return True


# ==========================================
# 6. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("Enter your code. Press Enter on an empty line to finish.")

    lines = []

    while True:

        line = input()

        if line == "":
            break

        lines.append(line)

    code = "\n".join(lines)

    valid = analyze(code)

    if not valid:

        choice = input(
            "\nTry adding missing semicolons? (y/n): "
        ).strip().lower()

        if choice == "y":

            corrected_code = fix_missing_semicolons(code)

            print("\n--- Corrected Code ---")
            print(corrected_code)

            print("\n--- Re-analyzing ---")

            analyze(corrected_code)
