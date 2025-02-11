from TrigoTree import parseTrig, constructParseTree, pruneNodes
from FileOperations import AccessFile, getInputOption, getDP
from ErrorHandling import InvalidExpression

class TrigoExpressions:
    def run(self):
        input_option = getInputOption()
        decimal_places = getDP(self)
        if input_option == 1:
            expression = self.get_direct_input()
            try:
                value = self.evaluate_expression(expression)
                value = self.format_result(value, decimal_places)
                print(f"Expression: {expression} = {value}")
            except InvalidExpression as e:
                print(f"Error evaluating expression '{expression}': {e}")
            except Exception as e:
                print(f"Unexpected error evaluating expression '{expression}': {e}")
        elif input_option == 2:
            input_file = input("Enter the input file path: ")
            output_file = input("Enter the output file path: ")
            file = AccessFile(input_file, output_file)
            expressions = file.read_expressions()
            results = []
            for expression in expressions:
                try:
                    value = self.evaluate_expression(expression)
                    value = self.format_result(value, decimal_places)
                    results.append(value)
                except InvalidExpression as e:
                    print(f"Error evaluating expression '{expression}': {e}")
                    results.append(None)
                except Exception as e:
                    print(f"Unexpected error evaluating expression '{expression}': {e}")
                    results.append(None)
            file.write_expressions([f"{expr} = {res}" for expr, res in zip(expressions, results)])
            print("Expressions and their results have been written to the output file.")
            for expression, result in zip(expressions, results):
                print(f"Expression: {expression} = {result}")
        else:
            print("Invalid input option selected.")
            return

    def get_direct_input(self):
        expression = input("Enter expression: ")
        return expression

    def format_result(self, value, decimal_places):
        if isinstance(value, float):
            return round(value, decimal_places)
        return value

    def evaluate_expression(self, expression):
        tokens = parseTrig(expression)
        tree = constructParseTree(tokens)
        tree = pruneNodes(tree)
        print('\nExpression Tree:')
        tree.printInorder()
        return tree.evaluate()

    def __str__(self):
        return 'Trigonometric expressions (Phylicia Ng)'
