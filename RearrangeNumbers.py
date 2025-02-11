from TrigoTree import parseTrig, constructParseTree, pruneNodes
from FileOperations import AccessFile, getInputOption, getDP
from ErrorHandling import InvalidExpression
import re

class RearrangeExpression:
    def run(self):
        input_option = getInputOption()
        decimal_places = getDP(self)
        if input_option == 1:
            expression = self.directInput()
            sorted_expression = self.sortNumbers(expression)
            print(f"Original expression: {expression}")
            print(f"Sorted expression: {sorted_expression}")
            result = self.evaluate_expression(sorted_expression)
            result = self.format_result(result, decimal_places)
            print(f"Result: {result}")
        elif input_option == 2:
            input_file = input("Enter the input file path: ")
            output_file = input("Enter the output file path: ")
            file = AccessFile(input_file, output_file)
            expressions = file.read_expressions()
            sorted_expressions = [self.sortNumbers(expr) for expr in expressions]
            results = [self.evaluate_expression(expr) for expr in sorted_expressions]
            results = [self.format_result(res, decimal_places) for res in results]
            file.write_expressions(sorted_expressions)
            print("\nSorted expressions and their results have been written to the output file.")
            for original_expr, sorted_expr, result in zip(expressions, sorted_expressions, results):
                print(f"\nOriginal expression: {original_expr}")
                print(f"Sorted expression: {sorted_expr}")
                print(f"Result: {result}")
        else:
            print("Invalid input option selected.")
            return

    def directInput(self):
        expression = input("Enter expression: ")
        return expression

    def sortNumbers(self, expression):
        # Extract numbers from the expression
        numbers = re.findall(r'\d+', expression)
        numbers = [int(num) for num in numbers]

        # Sort the numbers using bubble sort
        sorted_numbers = self.bubbleSort(numbers)

        # Replace the numbers in the expression with sorted numbers
        sorted_expression = re.sub(r'\d+', '{}', expression)
        sorted_expression = sorted_expression.format(*sorted_numbers)

        return sorted_expression

    def bubbleSort(self, numbers):
        n = len(numbers)
        for i in range(n):
            for j in range(0, n-i-1):
                if numbers[j] < numbers[j+1]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
        return numbers

    def evaluate_expression(self, expression):
        tokens = parseTrig(expression)
        tree = constructParseTree(tokens)
        tree = pruneNodes(tree)
        return tree.evaluate()

    def format_result(self, value, decimal_places):
        if isinstance(value, float):
            return round(value, decimal_places)
        return value

    def __str__(self):
        return 'Rearrange expressions by number size'

lols = RearrangeExpression()
lols.run()