from ErrorHandling import InvalidExpression

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
    
    def evaluate(self):
        leftTree = self.leftTree
        rightTree = self.rightTree
        op = self.key
        if leftTree != None and rightTree != None:
            if op == '+':
                return leftTree.evaluate() + rightTree.evaluate()
            elif op == '-':
                return leftTree.evaluate() - rightTree.evaluate()
            elif op == '*':
                return leftTree.evaluate() * rightTree.evaluate()
            elif op == '/':
                return leftTree.evaluate() / rightTree.evaluate()
            elif op == '**':
                return leftTree.evaluate() ** rightTree.evaluate()
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
        elif '.' in token:
            currentTree.key = float(token)
            currentTree = stack.pop()
        elif token == ')':
            currentTree = stack.pop()
        else:
            raise ValueError(token)
    return tree

from ErrorHandling import InvalidExpression

def parser(expression):
    if not expression:
        raise InvalidExpression("Expression cannot be empty", expression)

    tokens = []
    token = ''
    operators = ['/', '*', '-', '+', '(', ')', ' ', '.']
    open_parentheses = 0

    if expression[0] != '(':
        raise InvalidExpression("Expression must start with an opening parenthesis", expression, 0)

    for i, x in enumerate(expression):
        if not x.isdigit() and x not in operators:
            raise InvalidExpression(f"Invalid character '{x}' in expression", expression, i)
        if x == ' ':
            continue  # Ignore spaces
        elif x == '(':
            open_parentheses += 1
            tokens.append(x)
        elif x == ')':
            if open_parentheses == 0:
                raise InvalidExpression(f"Unmatched closing parenthesis at position {i}", expression, i)
            open_parentheses -= 1
            tokens.append(x)
        elif x in ['+', '-', '*', '/']:
            if x == '-' and (not tokens or tokens[-1] in ['(', '+', '-', '*', '/']):
                # Handle unary minus
                token += x
            elif not tokens or tokens[-1] in operators or tokens[-1] == '(':
                raise InvalidExpression(f"Invalid operator usage at position {i}", expression, i)
            else:
                if token:
                    tokens.append(token)
                    token = ''
                tokens.append(x)
        elif x.isdigit() or x == '.':
            token += x
        elif x == '*' and tokens and tokens[-1] == '*':
            tokens[-1] += x
        else:
            if token != '':
                tokens.append(token)
                token = ''
            tokens.append(x)
    if token != '':
        tokens.append(token)
    if open_parentheses != 0:
        raise InvalidExpression("Unmatched opening parenthesis", expression)
    if tokens[-1] in operators:
        raise InvalidExpression("Expression cannot end with an operator", expression)
    return tokens
