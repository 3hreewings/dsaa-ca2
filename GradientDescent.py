from BinaryTree import parser, buildParseTree
from ErrorHandling import ParseError, MathError

class GradientDescent:
    def run(self):
        expression = input('Enter an expression to solve for x (Gradient Descent Algorithm): ')
        try:
            tokens = parser(expression, with_x=True)
            tree = buildParseTree(tokens)
            tree_deriv = tree.differentiate()

            print('\nExpression Tree:')
            tree.printInorder()
            print('\nDerivative Tree:')
            tree_deriv.printInorder()

            prompts = [
                'Starting value of x: ',
                'Learning Rate: ',
                'Epsilon: '
            ]
            variables = []

            for prompt in prompts:
                while True:
                    value = input(prompt)
                    try:
                        value = float(value)
                        variables.append(value)
                        break
                    except ValueError:
                        print('Please input a valid number (integer or float)!\n')
            while True:
                max_iter = input('Maximum Iterations: ')
                try:
                    max_iter = int(max_iter)
                    variables.append(max_iter)
                    break
                except ValueError:
                    print('Please input a valid integer!\n')
            x, learning_rate, epsilon, max_iter = variables
            diff = 1
            iter = 1

            while diff > epsilon and iter < max_iter:
                x_new = x - learning_rate * tree_deriv.evaluate(x)
                diff = abs(x_new - x)
                iter = iter + 1
                x = x_new

            print('Iteration ', iter, '\nLocal Minimum: ', x, '\nf(x) is: ', tree.evaluate(x))
        except (ParseError, MathError) as e:
            print(f'Error: {e}')

    def __str__(self):
        return 'Evaluate expression'
    
# (((4*(x**2))-(4*x))+3)