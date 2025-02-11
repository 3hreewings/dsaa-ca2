# =============================================================================
# Authors: Wang Jun Xian (2309011) & Phylicia Ng (2308908)
# Date: 12/2/2025
# Description: Evaluate expression - print expression binary tree and evaluate
# =============================================================================

from BinaryTree import parser, buildParseTree
from ErrorHandling import ParseError, MathError

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
        except (ParseError, MathError) as e:
            print(f"Error: {e}")

    def __str__(self):
        return 'Evaluate expression'