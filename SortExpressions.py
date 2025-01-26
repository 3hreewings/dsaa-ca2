from BinaryTree import parser, buildParseTree
from FileOperations import AccessFile
from ErrorHandling import InvalidExpression

class SortExpressions:
    def run(self, input_file=None, output_file=None):
        file = AccessFile(input_file, output_file)
        expressions = file.read_expressions()

        if not expressions:
            print("No expressions found in the input file.")
            return

        print(">>>Evaluation and sorting started:")

        # Evaluate expressions
        evaluated_expressions = []
        for expr in expressions:
            try:
                value = self.evaluate_expression(expr)
                length = len(expr.replace(" ", ""))  # accounts for possible spaces in expression
                brackets = expr.count('(') + expr.count(')')
                evaluated_expressions.append((value, length, brackets, expr))
            except InvalidExpression as e:
                print(f"Error evaluating expression '{expr}': {e}")
            except Exception as e:
                print(f"Unexpected error evaluating expression '{expr}': {e}")

        evaluated_expressions.sort(key=lambda x: (-x[0], x[1], x[2]))

        sorted_expressions = []
        current_value = None
        for value, length, brackets, expr in evaluated_expressions:
            if value != current_value:
                if current_value is not None:
                    print()
                current_value = value
                print(f"*** Expressions with value=> {value}")
            print(f"{expr}==>{value}")
            sorted_expressions.append(f"{expr}==>{value}")

        file.write_expressions(sorted_expressions)

        print("\n>>>Evaluation and sorting completed!")

    def evaluate_expression(self, expression):
        tokens = parser(expression)
        tree = buildParseTree(tokens)
        return tree.evaluate()

    def __str__(self):
        return 'Sort expressions'