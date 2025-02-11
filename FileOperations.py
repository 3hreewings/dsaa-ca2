class AccessFile:
    def __init__(self, input_file=None, output_file=None):
        if input_file is None:
            input_file = input("Enter the input file path: ")
        if output_file is None:
            output_file = input("Enter the output file path: ")
        self.input_file = input_file
        self.output_file = output_file

    def read_expressions(self):
        try:
            with open(self.input_file, 'r') as infile:
                expressions = infile.readlines()
            return [expr.strip().replace(' ', '') for expr in expressions]
        except FileNotFoundError:
            print(f"Error: The file '{self.input_file}' was not found.")
            return []
        except Exception as e:
            print(f"Unexpected error while reading file '{self.input_file}': {e}")
            return []

    def write_expressions(self, expressions):
        try:
            with open(self.output_file, 'w') as outfile:
                for expr in expressions:
                    outfile.write(expr + '\n')
        except Exception as e:
            print(f"Unexpected error while writing to file '{self.output_file}': {e}")
            

def getInputOption():
    while True:
        print("\nSelect input option:")
        print("1. Direct input")
        print("2. File input")
        option = input("\nEnter your choice (1 or 2): ")
        if option in ['1', '2']:
            return int(option)
        else:
            print("Invalid choice. Please enter 1 or 2.")
            
def getDP(self):
    while True:
        try:
            decimal_places = int(input("\nEnter the number of decimal places for the result (0 - 15): "))
            if decimal_places < 0 or decimal_places > 15:
                raise ValueError
            return decimal_places
        except ValueError:
            print("Please enter a valid integer within the range (0 - 15).")