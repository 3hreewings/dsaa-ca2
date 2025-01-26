class ExpressionError(Exception):
    """Base class for exceptions in this module."""
    pass

class InvalidExpressionError(ExpressionError):
    """Exception raised for errors in the input expression."""
    def __init__(self, message="Invalid expression"):
        self.message = message
        super().__init__(self.message)