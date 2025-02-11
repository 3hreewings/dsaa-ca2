import re
import math
from ErrorHandling import ParseError, MathError

class BinaryTree:
    def __init__(self, key, leftTree=None, rightTree=None):
        self.key = key
        self.leftTree = leftTree
        self.rightTree = rightTree

    def insertLeft(self, key):
        if self.leftTree is None:
            self.leftTree = BinaryTree(key)
        else:
            tree = BinaryTree(key, self.leftTree)
            self.leftTree = tree

    def insertRight(self, key):
        if self.rightTree is None:
            self.rightTree = BinaryTree(key)
        else:
            tree = BinaryTree(key, None, self.rightTree)
            self.rightTree = tree

    def printInorder(self):
        def inorderRecur(tree, out):
            if tree:
                inorderRecur(tree.leftTree, out)
                out.append(str(tree.key))
                inorderRecur(tree.rightTree, out)
        out = []
        inorderRecur(self, out)
        print(" ".join(out))
    
    def evaluate(self):
        leftTree = self.leftTree
        rightTree = self.rightTree
        op = self.key
        if leftTree is not None and rightTree is not None:
            if op == '+':
                return leftTree.evaluate() + rightTree.evaluate()
            elif op == '-':
                return leftTree.evaluate() - rightTree.evaluate()
            elif op == '*':
                return leftTree.evaluate() * rightTree.evaluate()
            elif op == '/':
                right_val = rightTree.evaluate()
                if right_val == 0:
                    raise MathError('Cannot divide by 0')
                return leftTree.evaluate() / right_val
            elif op == '**':
                return leftTree.evaluate() ** rightTree.evaluate()
            else:
                raise ParseError('Unexpected operator in expression', op, [])
        elif leftTree is not None and op in ['sin', 'cos', 'tan']:
            if op == 'sin':
                return math.sin(leftTree.evaluate())
            elif op == 'cos':
                return math.cos(leftTree.evaluate())
            elif op == 'tan':
                return math.tan(leftTree.evaluate())
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

def constructParseTree(tokens):
    stack = Stack()
    tree = BinaryTree('?')
    stack.push(tree)
    stack.push(tree)
    currentTree = tree
    for token_tuple in tokens:
        token = token_tuple[0]
        if token == '(':
            currentTree.insertLeft('?')
            stack.push(currentTree)
            currentTree = currentTree.leftTree
        elif token in ['sin', 'cos', 'tan']:
            currentTree.key = token
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
        elif token == ')':
            currentTree = stack.pop()
        else:
            raise ValueError(f"Unexpected token: {token}")
    return tree

def pruneNodes(tree):
    if tree is None:
        return None
    tree.leftTree = pruneNodes(tree.leftTree)
    tree.rightTree = pruneNodes(tree.rightTree)
    if tree.key == '?' and tree.leftTree is not None and tree.rightTree is None:
        return tree.leftTree
    return tree

def combine_negative_tokens(tokens, trig_functions):
    new_tokens = []
    i = 0
    while i < len(tokens):
        token, start, end = tokens[i]
        if (token == '-' and i + 1 < len(tokens) and 
            (i == 0 or new_tokens[-1][0] in ['(', '+', '-', '*', '/', '**'] or new_tokens[-1][0] in trig_functions)):
            next_token, nstart, nend = tokens[i + 1]
            if next_token.replace('.', '', 1).isdigit():
                combined = '-' + next_token
                new_tokens.append((combined, start, nend))
                i += 2
                continue
        new_tokens.append((token, start, end))
        i += 1
    return new_tokens

def parseTrig(expression):
    if len(expression.strip()) == 0:
        raise ParseError('Expression cannot be empty', expression, [])
    token_regex = r'-?\d+(?:\.\d+)?|\*\*|[+\-*/()]|sin|cos|tan'
    binary_operators = {'+', '-', '*', '/', '**'}
    trig_functions = {'sin', 'cos', 'tan'}
    tokens = [(match.group(), *match.span()) for match in re.finditer(token_regex, expression)]
    tokens = combine_negative_tokens(tokens, trig_functions)
    
    errors = []
    if expression.strip()[0] != '(' or expression.strip()[-1] != ')':
        raise ParseError('Expression should start and end with parentheses', expression, [])
    invalid_matches = [
        (m.start(), m.end()) for m in re.finditer(r'[A-Za-z]+', expression)
        if m.group() not in trig_functions
    ]
    if invalid_matches:
        raise ParseError('Invalid characters in expression', expression, invalid_matches)
    
    if tokens and tokens[0][0] == '-' and len(tokens) > 1 and re.search(r'\d', tokens[1][0]):
        tokens[0] = ('-' + tokens[1][0], tokens[0][1], tokens[1][2])
        tokens.pop(1)
    
    for i, (token, start, end) in enumerate(tokens):
        if token in trig_functions:
            if i + 1 >= len(tokens) or tokens[i + 1][0] != '(':
                errors.append((start, end))
    
    paren_stack = []
    for (token, start, end) in tokens:
        if token == '(':
            paren_stack.append(start)
        elif token == ')':
            if not paren_stack:
                errors.append((start, end))
            else:
                paren_stack.pop()
    for position in paren_stack:
        errors.append((position, position))
    
    for i in range(1, len(tokens) - 1):
        prev_token, prev_start, prev_end = tokens[i - 1]
        cur_token, cur_start, cur_end = tokens[i]
        next_token, next_start, next_end = tokens[i + 1]
        if cur_token in binary_operators:
            if prev_token != ')' and not re.search(r'\d', prev_token):
                errors.append((prev_end, cur_end))
            if next_token != '(' and not re.search(r'\d', next_token):
                errors.append((cur_start, next_start))
    
    if errors:
        raise ParseError('Invalid expression', expression, errors)
    
    return tokens

