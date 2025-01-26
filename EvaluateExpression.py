from BinaryTree import parser, buildParseTree
from ErrorHandling import InvalidExpression

class EvaluateExpression:
    def run(self, expression=None):
        if expression is None:
            expression = input('Enter an expression to evaluate: ')
        try:
            tokens = parser(expression)
            tree = buildParseTree(tokens)
            print('\nExpression Tree:')
            tree.printInorder()
            print(f'Expression evaluates to:\n{tree.evaluate()}')
        except InvalidExpression as e:
            print(f"Error: {e}")

    def __str__(self):
        return 'Evaluate expression'