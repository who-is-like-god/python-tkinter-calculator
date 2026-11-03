import operator


def calculate(expression):
    tokens = tokenize(expression)
    precedence = [
        ('*', '/', '%'),
        ('+', '-')
    ]
    operator_map = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '%': operator.mod,
    }

    for operators in precedence:
        while any(token in operators for token in tokens):
            for token in tokens:
                if token in operators:
                    index = tokens.index(token)
                    left = tokens[index - 1]
                    right = tokens[index + 1]

                    calculation = operator_map[token]
                    result = calculation(left, right)
                    tokens[index - 1: index + 2] = [result]
                    break

    return tokens[0]


def tokenize(expression):
    operators = ("+", "-", "*", "/", "%")

    if not expression:
        raise ValueError("Empty expression")

    if expression.endswith(operators):
        raise ValueError("Expression cannot ends with an operator")

    tokens = []
    current_number = ""

    for char in expression:
        if char not in '+-*/%':
            current_number += char
        else:
            if current_number == "":
                raise ValueError("Missing number before operator")
            tokens.append(float(current_number))
            tokens.append(char)
            current_number = ""
    tokens.append(float(current_number))
    # if tokens and isinstance(tokens[-1], str):
    #     raise ValueError("Expression cannot end with an operator")
    return tokens
