# =============================================================================
# Authors: Wang Jun Xian (2309011) & Phylicia Ng (2308908)
# Date: 12/2/2025
# Description: Sort Expressions - sort expressions by evaluation, length and brackets
# =============================================================================

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

        print(">>>Evaluation and sorting started:\n")

        evaluated_expressions = []
        for line in expressions:
            try:
                value = self.evaluate_expression(line)
                length = len(line.replace(" ", ""))  # accounts for possible spaces in expression
                brackets = line.count('(') + line.count(')')
                evaluated_expressions.append((value, length, brackets, line))
            except InvalidExpression as e:
                print(f"Error evaluating expression '{line}': {e}")
            except Exception as e:
                print(f"Unexpected error evaluating expression '{line}': {e}")

        evaluated_expressions.sort(key=lambda x: (-x[0], x[1], x[2]))

        sorted_expressions = []
        current_value = None
        first_group = True
        for value, length, brackets, line in evaluated_expressions:
            if value != current_value:
                if not first_group:
                    sorted_expressions.append('\n')
                    print()
                first_group = False
                current_value = value
                print(f"*** Expressions with value= {value}")
                sorted_expressions.append(f"*** Expressions with value= {value}")
            print(f"{line}==>{value}")
            sorted_expressions.append(f"{line}==>{value}")

        file.write_expressions(sorted_expressions)

        print("\n>>>Evaluation and sorting completed!")

    def evaluate_expression(self, expression):
        tokens = parser(expression)
        tree = buildParseTree(tokens)
        return tree.evaluate()

    def __str__(self):
        return 'Sort expressions'