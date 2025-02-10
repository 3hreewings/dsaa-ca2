from BinaryTree import parser, buildParseTree
from ErrorHandling import ParseError, MathError

class EvaluateExpression:
    def run(self, expression=None):
        if expression is None:
            expression = input('Enter an expression to evaluate: ')
        try:
            tokens = parser(expression)
            tree = buildParseTree([token[0] for token in tokens])
            print('\nExpression Tree:')
            tree.printInorder()
            print(f'Expression evaluates to:\n{tree.evaluate()}')
        except (ParseError, MathError) as e:
            print(f"Error: {e}")

    def __str__(self):
        return 'Evaluate expression'