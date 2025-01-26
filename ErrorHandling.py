class ExpressionError(Exception):
    def __init__(self, message, expression=None, position=None):
        super().__init__(message)
        self.message = message
        self.expression = expression
        self.position = position

    def __str__(self):
        if self.expression and self.position is not None:
            return f"{self.message} at position {self.position} in expression '{self.expression}'"
        return self.message

class InvalidExpression(ExpressionError):
    def __init__(self, message, expression=None, position=None):
        super().__init__(message, expression, position)