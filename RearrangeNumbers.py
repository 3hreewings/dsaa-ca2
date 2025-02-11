from TrigoTree import parseTrig, constructParseTree
from FileOperations import AccessFile
from ErrorHandling import InvalidExpression
import re

class RearrangeExpression:
    def run(self):
        input_option = self.get_input_option()
        if input_option == 1:
            expression = self.get_direct_input()
            sorted_expression = self.sort_expression_by_number_size(expression)
            print(f"Sorted expression: {sorted_expression}")
            result = self.evaluate_expression(sorted_expression)
            print(f"Result: {result}")
        elif input_option == 2:
            input_file = input("Enter the input file path: ")
            output_file = input("Enter the output file path: ")
            file = AccessFile(input_file, output_file)
            expressions = file.read_expressions()
            sorted_expressions = [self.sort_expression_by_number_size(expr) for expr in expressions]
            results = [self.evaluate_expression(expr) for expr in sorted_expressions]
            file.write_expressions(sorted_expressions)
            print("Sorted expressions and their results have been written to the output file.")
            for expr, result in zip(sorted_expressions, results):
                print(f"{expr} => {result}")
        else:
            print("Invalid input option selected.")
            return

    def get_input_option(self):
        while True:
            print("Select input option:")
            print("1. Direct input")
            print("2. File input")
            option = input("Enter your choice (1 or 2): ")
            if option in ['1', '2']:
                return int(option)
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def get_direct_input(self):
        expression = input("Enter expression: ")
        return expression

    def sort_expression_by_number_size(self, expression):
        # Extract numbers from the expression
        numbers = re.findall(r'\d+', expression)
        numbers = [int(num) for num in numbers]

        # Bubble sort the numbers in descending order
        n = len(numbers)
        for i in range(n):
            for j in range(0, n-i-1):
                if numbers[j] < numbers[j+1]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]

        # Replace the numbers in the expression with sorted numbers
        sorted_expression = re.sub(r'\d+', '{}', expression)
        sorted_expression = sorted_expression.format(*numbers)

        return sorted_expression

    def evaluate_expression(self, expression):
        tokens = parseTrig(expression)
        tree = constructParseTree(tokens)
        return tree.evaluate()

    def __str__(self):
        return 'Rearrange expressions by number size'


    