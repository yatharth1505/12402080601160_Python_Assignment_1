"""
Q3 - Recursive Expression Engine with Memoization and Cycle Detection
Supports non-negative integers, +, -, *, parentheses and variables.
"""
import re
import sys
from functools import lru_cache


TOKEN_RE = re.compile(r"\s*(?:(\d+)|([A-Za-z_]\w*)|([()+\-*]))")


class InvalidExpression(Exception):
    pass


class Parser:
    def __init__(self, text, resolver):
        self.text = text
        self.resolver = resolver
        self.pos = 0
        self.tokens = []
        self._tokenize()

    def _tokenize(self):
        while self.pos < len(self.text):
            match = TOKEN_RE.match(self.text, self.pos)
            if not match:
                raise InvalidExpression("Invalid token.")
            self.tokens.append(
                ("NUMBER", match.group(1)) if match.group(1) else
                ("NAME", match.group(2)) if match.group(2) else
                (match.group(3), match.group(3))
            )
            self.pos = match.end()
        self.tokens.append(("EOF", ""))

    def parse(self):
        self.index = 0
        value = self.expression()
        if self.tokens[self.index][0] != "EOF":
            raise InvalidExpression("Unexpected token.")
        return value

    def expression(self):
        value = self.term()
        while self.tokens[self.index][0] in ("+", "-"):
            op = self.tokens[self.index][0]
            self.index += 1
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def term(self):
        value = self.factor()
        while self.tokens[self.index][0] == "*":
            self.index += 1
            value *= self.factor()
        return value

    def factor(self):
        kind, value = self.tokens[self.index]

        if kind == "NUMBER":
            self.index += 1
            return int(value)

        if kind == "NAME":
            self.index += 1
            return self.resolver(value)

        if kind == "(":
            self.index += 1
            result = self.expression()
            if self.tokens[self.index][0] != ")":
                raise InvalidExpression("Missing closing parenthesis.")
            self.index += 1
            return result

        raise InvalidExpression("Expected number, variable or '('.")


def solve(data):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        raise InvalidExpression("Empty input.")

    v = int(lines[0])
    if len(lines) != v + 2:
        raise InvalidExpression("Incorrect number of lines.")

    definitions = {}
    for line in lines[1:v + 1]:
        if "=" not in line:
            raise InvalidExpression("Variable definition must contain '='.")
        name, expr = line.split("=", 1)
        name = name.strip()
        if not re.fullmatch(r"[A-Za-z_]\w*", name):
            raise InvalidExpression("Invalid variable name.")
        definitions[name] = expr.strip()

    target = lines[-1]
    state = {}       # 0 = unseen, 1 = visiting, 2 = done
    memo = {}

    def evaluate_variable(name):
        if name not in definitions:
            raise InvalidExpression(f"Unknown variable: {name}")
        if state.get(name, 0) == 1:
            raise RuntimeError("CYCLE")
        if state.get(name, 0) == 2:
            return memo[name]

        state[name] = 1
        value = Parser(definitions[name], evaluate_variable).parse()
        memo[name] = value
        state[name] = 2
        return value

    return str(Parser(target, evaluate_variable).parse())


def main():
    try:
        print(solve(sys.stdin.read()))
    except RuntimeError as exc:
        if str(exc) == "CYCLE":
            print("CYCLE")
        else:
            print("INVALID")
    except (ValueError, InvalidExpression):
        print("INVALID")


if __name__ == "__main__":
    main()
