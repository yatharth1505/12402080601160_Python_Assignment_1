"""
Q7 - Interactive Formula Validator with Custom Exceptions
Supported operators: +, -, *, /, %
"""
import operator
import re


class FormulaError(Exception):
    pass


class InvalidFormatError(FormulaError):
    pass


class UnknownVariableError(FormulaError):
    pass


class DivisionByZeroError(FormulaError):
    pass


class UnsupportedOperatorError(FormulaError):
    pass


class Calculator:
    ASSIGNMENT = re.compile(r"^([A-Za-z_]\w*)\s*=\s*(.+)$")
    FORMULA = re.compile(
        r"^\s*([A-Za-z_]\w*|-?\d+(?:\.\d+)?|[+-]?\d*\.\d+)\s*"
        r"([+\-*/%])\s*"
        r"([A-Za-z_]\w*|-?\d+(?:\.\d+)?|[+-]?\d*\.\d+)\s*$"
    )

    def __init__(self):
        self.variables = {}

    def operand(self, token):
        if re.fullmatch(r"[A-Za-z_]\w*", token):
            if token not in self.variables:
                raise UnknownVariableError(f"Unknown variable: {token}")
            return self.variables[token]
        try:
            return float(token)
        except ValueError as exc:
            raise InvalidFormatError("Invalid operand.") from exc

    def evaluate(self, expression):
        match = self.FORMULA.fullmatch(expression)
        if not match:
            # Explicitly report unsupported operators such as **.
            if "**" in expression:
                raise UnsupportedOperatorError("Operator '**' is not supported.")
            raise InvalidFormatError(
                "Expected: operand operator operand."
            )

        left_token, op, right_token = match.groups()
        left = self.operand(left_token)
        right = self.operand(right_token)

        if op == "/" and right == 0:
            raise DivisionByZeroError("Division by zero is not allowed.")
        if op == "%" and right == 0:
            raise DivisionByZeroError("Modulo by zero is not allowed.")

        operations = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "%": operator.mod,
        }
        return operations[op](left, right)

    def assignment(self, line):
        match = self.ASSIGNMENT.fullmatch(line)
        if not match:
            raise InvalidFormatError("Invalid assignment format.")

        name, value = match.groups()
        # A simple assignment accepts a numeric value or a stored variable.
        if re.fullmatch(r"[A-Za-z_]\w*", value.strip()):
            value = self.operand(value.strip())
        else:
            try:
                value = float(value.strip())
            except ValueError as exc:
                raise InvalidFormatError(
                    "Assignment value must be a number or variable."
                ) from exc

        self.variables[name] = value


def display_number(value):
    return str(int(value)) if value.is_integer() else str(value)


def main():
    calc = Calculator()

    while True:
        try:
            line = input().strip()
        except EOFError:
            break

        if not line:
            continue
        if line.lower() == "quit":
            break

        try:
            if "=" in line and not any(op in line.split("=", 1)[0] for op in "+-*/%"):
                calc.assignment(line)
                continue

            result = calc.evaluate(line)
            print(display_number(result))
        except FormulaError as exc:
            print(type(exc).__name__)
            # The assignment's sample expects the exception type; the message
            # is kept available for a developer if needed.
            # print(f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
