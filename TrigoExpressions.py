from TrigoTree import parseTrig, constructParseTree
from FileOperations import AccessFile
from ErrorHandling import InvalidExpression

class SortTrigoExpressions:
    def run(self, input_option=None, input_file=None, output_file=None):
        if input_option is None:
            input_option = self.get_input_option()
        
        if input_option == 1:
            expression = self.get_direct_input()
            expressions = [expression]
        elif input_option == 2:
            if input_file is None:
                input_file = input("Enter the input file path: ")
            if output_file is None:
                output_file = input("Enter the output file path: ")
            file = AccessFile(input_file, output_file)
            expressions = file.read_expressions()
        else:
            print("Invalid input option selected.")
            return

        if not expressions:
            print("No expressions found.")
            return

        evaluated_expressions = []
        try:
            for line in expressions:
                try:
                    value = self.evaluate_expression(line)
                    length = len(line.replace(" ", ""))  # accounts for possible spaces in expression
                    brackets = line.count('(') + line.count(')')
                    evaluated_expressions.append((value, length, brackets, line))
                except InvalidExpression as e:
                    print(f"Error evaluating expression '{line}': {e}")

            evaluated_expressions.sort(key=lambda x: (-x[0], x[1], x[2]))

            sorted_expressions = []
            current_value = None
            first_group = True
            for value, length, brackets, line in evaluated_expressions:
                if value != current_value:
                    current_value = value
                print(f"Expression: {line} = {value}")

            if input_option == 2:
                file.write_expressions(sorted_expressions)

            print("\n>>>Evaluation and sorting completed!")
        except Exception as e:
            print(f"Error: {e}")

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

    def evaluate_expression(self, expression):
        tokens = parseTrig(expression)
        tree = constructParseTree(tokens)
        return tree.evaluate()

    def __str__(self):
        return 'Trigonometric expressions (Phylicia Ng)'

# Main function to run the SortTrigoExpressions class
if __name__ == "__main__":
    lols = SortTrigoExpressions()
    # lols.run(input_option=1)
    lols.run(input_option=2, input_file="test.txt", output_file="out.txt")