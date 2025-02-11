# =============================================================================
# Authors: Wang Jun Xian (2309011) & Phylicia Ng (2308908)
# Date: 12/2/2025
# Description: Contains exception classes for errors
# =============================================================================

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

class ParseError(ExpressionError):
    def __init__(self, message, expression=None, position=None):
        super().__init__(message, expression, position)

    def __str__(self):
        if self.expression and self.position is not None:
            arrowline = list(' ' * (len(self.expression)))
            for start, end in self.position:
                arrowline[(start + end) // 2] = '^'
            return '\n' + self.expression + '\n' + ''.join(arrowline) + '\n' + self.message
        return self.message
    
class MathError(ExpressionError):
    def __init__(self, message):
        super().__init__(message, None, None)