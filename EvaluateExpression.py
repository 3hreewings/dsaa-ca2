from BinaryTree import parser, buildParseTree

class EvaluateExpression:
    def run(self):
        expression = input('Enter an expression to evaluate: ')
        tokens = parser(expression)
        if isinstance(tokens, str):
            print(tokens)
            return
        tree = buildParseTree(tokens)
        print('\nExpression Tree:')
        tree.printInorder()
        print(f'Expression evaluates to:\n{tree.evaluate()}')

    def __str__(self):
        return 'Evaluate expression'