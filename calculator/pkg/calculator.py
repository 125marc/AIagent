# calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        print("evaluate: start", expression)
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        result = self._evaluate_infix(tokens)
        print("evaluate: end", result)
        return result

    def _evaluate_infix(self, tokens):
        print("_evaluate_infix: start", tokens)
        values = []
        operators = []

        for token in tokens:
            print("token:", token, "values:", values, "operators:", operators)
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        print("_evaluate_infix: end", values[0])
        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))

# Test the calculator
if __name__ == "__main__":
    try:
        calc = Calculator()
        result = calc.evaluate("2 + 3")
        print(result)
    except Exception as e:
        print(f"Error: {e}")