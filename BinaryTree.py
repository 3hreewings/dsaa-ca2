from ErrorHandling import ParseError, MathError
import re

class BinaryTree:
    def __init__(self, key, leftTree=None, rightTree=None):
        self.key = key
        self.leftTree = leftTree
        self.rightTree = rightTree
    
    def insertLeft(self, key):
        if self.leftTree == None:
            self.leftTree = BinaryTree(key)
        else:
            tree = BinaryTree(key, self)
            self.leftTree , tree.leftTree = tree, self.leftTree
            
    def insertRight(self, key):
        if self.rightTree == None:
            self.rightTree = BinaryTree(key)
        else:
            tree = BinaryTree(key, self)
            self.rightTree , tree.rightTree = tree, self.rightTree

    def printInorder(self):
        def inorderRecur(tree, y, out):
            nonlocal x
            if tree.leftTree != None:
                inorderRecur(tree.leftTree, y+1, out)
            while len(out) <= y + len(str(tree.key)):
                out.append([])
            for i, char in enumerate(str(tree.key)):
                while len(out[y+i]) <= x + 1:
                    out[y+i].append(' ')
                out[y+i][x] = char + ''
            x += 1
            if tree.rightTree != None:
                inorderRecur(tree.rightTree, y+1, out)
            y -= 1
        x = 0
        y = 0
        out = []
        inorderRecur(self, y, out)
        for row in out:
            print(''.join(row))

    def differentiate(self):
        if isinstance(self.key, int) or isinstance(self.key, float):
            return BinaryTree(0)  # Derivative of constant is 0
        elif self.key == 'x':  # Derivative of x is 1
            return BinaryTree(1)
        elif self.key == '+':  # Derivative of a sum is the sum of the derivatives
            return BinaryTree('+', self.leftTree.differentiate(), self.rightTree.differentiate())
        elif self.key == '-':  # Derivative of a difference is the difference of the derivatives
            return BinaryTree('-', self.leftTree.differentiate(), self.rightTree.differentiate())
        elif self.key == '*':  # Product rule: (f*g)' = f'*g + f*g'
            left_derivative = self.leftTree.differentiate()
            right_derivative = self.rightTree.differentiate()
            return BinaryTree('+', 
                              BinaryTree('*', left_derivative, self.rightTree),
                              BinaryTree('*', self.leftTree, right_derivative))
        elif self.key == '/':  # Quotient rule: (f/g)' = (f'*g - f*g') / g^2
            left_derivative = self.leftTree.differentiate()
            right_derivative = self.rightTree.differentiate()
            return BinaryTree('/', 
                              BinaryTree('-', 
                                         BinaryTree('*', left_derivative, self.rightTree),
                                         BinaryTree('*', self.leftTree, right_derivative)),
                              BinaryTree('**', self.rightTree, BinaryTree(2)))
        elif self.key == '**':  # Power rule: (x^n)' = n*x^(n-1)
            if isinstance(self.leftTree.key, int):  # If the base is a number, apply power rule
                return BinaryTree('*', 
                                  BinaryTree(self.leftTree.key - 1),
                                  BinaryTree('**', self.leftTree, BinaryTree(self.leftTree.key - 1)))
            else:
                raise ParseError("Exponentiation with variables other than 'x' is not supported")
        else:
            raise ParseError('Unexpected operator for differentiation', self.key)
    
    def differentiate(self):
        leftTree = self.leftTree
        rightTree = self.rightTree
        op = self.key
        
        if op == '+':
            return BinaryTree('+', leftTree.differentiate(), rightTree.differentiate())
        
        elif op == '-':
            return BinaryTree('-', leftTree.differentiate(), rightTree.differentiate())
        
        elif op == '*':  # Product rule: (f*g)' = f'*g + f*g'
            left_diff = leftTree.differentiate()
            right_diff = rightTree.differentiate()
            return BinaryTree('+', BinaryTree('*', left_diff, rightTree), BinaryTree('*', leftTree, right_diff))
        
        elif op == '/':  # Quotient rule: (f/g)' = (f'*g - f*g') / g^2
            left_diff = leftTree.differentiate()
            right_diff = rightTree.differentiate()
            numerator = BinaryTree('-', BinaryTree('*', left_diff, rightTree), BinaryTree('*', leftTree, right_diff))
            denominator = BinaryTree('**', rightTree, BinaryTree(2))
            return BinaryTree('/', numerator, denominator)
        
        elif op == '**':  # Power rule: (x^n)' = n*x^(n-1)
            if isinstance(rightTree.key, int):
                n = rightTree.key
                return BinaryTree('*', BinaryTree(n), BinaryTree('**', leftTree, BinaryTree(n - 1)))
            else:
                raise ParseError('Power exponent must be an integer')

        elif self.key == 'x':
            return BinaryTree(1)
        
        else:
            return BinaryTree(0)


    def evaluate(self, x=None):
        leftTree = self.leftTree
        rightTree = self.rightTree
        op = self.key
        leftKey = rightKey = None

        if leftTree != None and rightTree != None:
            if leftTree.key == 'x':
                leftKey = leftTree.key
                leftTree.key = x
            if rightTree.key == 'x':
                rightKey = rightTree.key
                rightTree.key = x

            leftVal = leftTree.evaluate(x)
            rightVal = rightTree.evaluate(x)

            if leftKey != None:
                leftTree.key = leftKey
            if rightKey != None:
                rightTree.key = rightKey

            if op == '+':
                return leftVal + rightVal
            elif op == '-':
                return leftVal - rightVal
            elif op == '*':
                return leftVal * rightVal
            elif op == '/':
                if rightVal == 0:
                    raise MathError('Cannot divide by 0')
                return leftVal / rightVal
            elif op == '**':
                return leftVal ** rightVal
            else:
                raise ParseError('Unexpected parse error - expression invalid')
        else:
            return self.key

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise Exception('Popping from empty stack')
        remove = self.head
        self.head = self.head.next
        self.size -= 1
        return remove.value
    
    def __str__(self):
        out = ''
        cur = self.head
        while cur:
            out += str(cur.value) + '->'
            cur = cur.next
        return out

def buildParseTree(tokens):
    stack = Stack()
    tree = BinaryTree('?')
    stack.push(tree)
    stack.push(tree)
    currentTree = tree
    for token in tokens:
        if token == '(':
            currentTree.insertLeft('?')
            stack.push(currentTree)
            currentTree = currentTree.leftTree
        elif token in ['+', '-', '*', '**', '/']:
            currentTree.key = token
            currentTree.insertRight('?')
            stack.push(currentTree)
            currentTree = currentTree.rightTree
        elif token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            currentTree.key = int(token)
            currentTree = stack.pop()
        elif '.' in token or (token[0] == '-' and '.' in token):
            currentTree.key = float(token)
            currentTree = stack.pop()
        elif token == 'x':
            currentTree.key = token
            currentTree = stack.pop()
        elif token == ')':
            currentTree = stack.pop()
        else:
            raise ValueError(token)
    return tree

def parser(expression, with_x=False):
    if len(expression) == 0:
        raise ParseError('Expression cannot be empty')

    if with_x == True:
        token_regex = r'\d+(?:\s*\d+)*(?:\s*\.\s*\d+(?:\s*\d+)*)?|\.\s*\d+(?:\s*\d+)*|x|\*\*|[+\-*/()]'
        invalid_characters = r'[^x0-9.+\-*/()\s]'
        number_regex = r'[\dx]'
    else:
        token_regex = r'\d+(?:\s*\d+)*(?:\s*\.\s*\d+(?:\s*\d+)*)?|\.\s*\d+(?:\s*\d+)*|\*\*|[+\-*/()]'
        invalid_characters = r'[^0-9.+\-*/()\s]'
        number_regex = r'\d'

    invalid_chars = [match.span() for match in re.finditer(invalid_characters, expression)] # Contains tuples of (start, end)
    if invalid_chars:
        raise ParseError('Invalid characters', expression, invalid_chars)
    
    if expression.strip()[0] != '(' or expression.strip()[-1] != ')':
        raise ParseError('Expression should start and end with parantheses')
    
    operators = {'+', '-', '*', '/', '**'}
    tokens = [(match.group(), *match.span()) for match in re.finditer(token_regex, expression)] # Contains tuples of (token, start, end)
    errors = [] # Contains tuples of (start, end)

    if tokens[0][0] == '-' and len(tokens) > 1 and re.search(number_regex, tokens[1][0]):
        tokens[0] = ('-' + tokens[1][0], tokens[0][1], tokens[1][2])
        tokens.pop(1)
    i = 1
    while i < len(tokens) - 1:
        prev_token, prev_start, prev_end = tokens[i - 1]
        cur_token, cur_start, cur_end = tokens[i]
        next_token, next_start, next_end = tokens[i + 1]
        if cur_token == '-' and (prev_token in operators or prev_token == '(') and re.search(number_regex, next_token):
            tokens[i] = ('-' + next_token, cur_start, next_end)
            tokens.pop(i + 1)
        else:
            i += 1

    # Check for whitespace in tokens
    for (token, start, end) in tokens:
        if ' ' in token:
            errors.append((start, end))

    for i in range(1, len(tokens) - 1):
        prev_token, prev_start, prev_end = tokens[i - 1]
        cur_token, cur_start, cur_end = tokens[i]
        next_token, next_start, next_end = tokens[i + 1]

        if cur_token in operators:
            # Check left side (must be a number or closing parenthesis)
            if prev_token != ')' and not re.search(number_regex, prev_token):
                errors.append((prev_end, cur_end))
            
            # Check right side (must be a number or opening parenthesis)
            if next_token != '(' and not re.search(number_regex, next_token):
                errors.append((cur_start, next_start))

    # Check that operators have closing parentheses or numbers on the left and opening parentheses or numbers on the right
    for i in range(1, len(tokens) - 1):
        prev_token, prev_start, prev_end = tokens[i - 1]
        cur_token, cur_start, cur_end = tokens[i]
        next_token, next_start, next_end = tokens[i + 1]
        if cur_token in operators:
            if prev_token != ')' and not re.search(number_regex, prev_token):
                errors.append((prev_end, cur_end))
            if next_token != '(' and not re.search(number_regex, next_token):
                errors.append((cur_start, next_start))

    # Check for matching parentheses
    paren_stack = []
    for (token, start, end) in tokens:
        if token == '(':
            paren_stack.append((start))
        elif token == ')':
            if not paren_stack:
                errors.append((start, end))
            else:
                paren_stack.pop()
    for position in paren_stack:
        errors.append((position, position))

    if errors:
        for error in errors:
            (start, end) = error
            error = (start + end) // 2
        raise ParseError('Invalid expression', expression, errors)

    return [token[0] for token in tokens]