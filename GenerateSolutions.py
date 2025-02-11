import operator
import re
from FileOperations import AccessFile
from ErrorHandling import ParseError

class Generate_Solutions:
    def run(self):
        file = AccessFile('None', None)

        numbers = input('Enter numbers separated by commas: ')
        errors = [match.span() for match in re.finditer(r'[^0-9,\s]', numbers)]
        if len(errors) != 0:
            print('Error:', ParseError('Invalid characters', numbers, errors))
            return

        numbers = list(map(int, input('Enter numbers separated by commas: ').split()))
        target = int(input('Enter the target value: '))
        solutions = self.__get_expressions(numbers, target)

        no_solutions = len(solutions)
        if no_solutions == 0:
            print('No solutions found!')
        else:
            print(f'Found {no_solutions} solutions!')
            if no_solutions <= 5:
                for solution in solutions:
                    print(solution)
            file.write_expressions(solutions)

    def __get_permutations(self, elements):
        if len(elements) == 0:
            return []
        if len(elements) == 1:
            return [elements]
        
        permutations = []
        for i, element in enumerate(elements):
            remaining = elements[:i] + elements[i+1:]
            for permutation in self.__get_permutations(remaining):
                permutations.append([element] + permutation)
        return permutations

    def __get_combinations(self, operators, length):
        if length == 0:
            return [[]]
        
        combinations = []
        for operator in operators:
            for combination in self.__get_combinations(operators, length - 1):
                combinations.append([operator] + combination)
        return combinations

    def __get_expressions(self, numbers, target):
        operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '**': operator.pow}
        expressions = []

        for permutation in self.__get_permutations(numbers):
            for operators_sequence in self.__get_combinations(list(operators.keys()), len(numbers) - 1):
                expression = str(permutation[0])
                result = permutation[0]
                try:
                    for i in range(1, len(permutation)):
                        expression = f'({expression} {operators_sequence[i-1]} {permutation[i]})'
                        result = operators[operators_sequence[i-1]](result, permutation[i])
                    if result == target:
                        expressions.append(expression)
                except (ZeroDivisionError, ValueError):
                    continue
        
        return expressions
    
    def __str__(self):
        return 'Generate solutions'