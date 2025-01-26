# Task 1 - Node and Stack

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

# Task 1 - BinaryTree

class BinaryTree():
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

    def printInorder(self, level):
        if self.leftTree != None:
            self.leftTree.printInorder(level + 1)
        print(str(level * '-') + str(self.key))
        if self.rightTree != None:
            self.rightTree.printInorder(level + 1)
    
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
                rightEvaluate = rightTree.evaluate()
                if rightEvaluate == 0:
                    return 'Cannot divide by zero'
                else:
                    return leftTree.evaluate() / rightEvaluate
            elif op == '**':
                return leftTree.evaluate() ** rightTree.evaluate()
        else:
            return self.key
        
# Task 1 - Parser

class Parser():
    def parse(self, expression):
        tokens = []
        token = ''
        operators = ['/', '*', '-', '+', '(', ')', ' ', '.']
        for x in expression:
            if not x.isdigit() and x not in operators:
                return 'Please enter a valid expression!'
            if x == ' ':
                pass
            elif x == '-' and token == '' and (not tokens or tokens[-1] in '(*'):
                token += x
            elif x.isdigit() or x == '.':
                token += x
            elif x == '*' and tokens [-1] == '*':
                tokens[-1] += x
            else:
                if token != '':
                    tokens.append(token)
                    token = ''
                tokens.append(x)
        return tokens
    
    def buildParseTree(self, tokens):
        stack = Stack()
        tree = BinaryTree('?')
        stack.push(tree)
        stack.push(tree)
        currentTree = tree
        try:
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
        except:
            print('Please enter a valid expresion!')
            return
        return tree
    
# Task 1 - Program

exp = '((200 + (4*3.14)) / (2**3) )'
parser = Parser()
tokens = parser.parse(exp)
tree = parser.buildParseTree(tokens)
print (f'The expression: {exp} evaluates to: {tree.evaluate()}')

# Task 2

class BST(BinaryTree):
    def __init__(self, key, leftTree = None, rightTree = None):
        super().__init__(key, leftTree, rightTree)

    def add(self, key):
        curNode = self
        while True:
            if key < curNode.key:
                if curNode.leftTree == None:
                    curNode.leftTree = BST(key)
                    break
                else:
                    curNode = curNode.leftTree
            elif key > curNode.key:
                if curNode.rightTree == None:
                    curNode.rightTree = BST(key)
                    break
                else:
                    curNode = curNode.rightTree

    def __contains__(self, key):
        curNode = self
        while curNode != None:
            if key == curNode.key:  
                return True
            elif key < curNode.key:
                curNode = curNode.leftTree
            else:
                curNode = curNode.rightTree
        return False

items = [55,30,73,64,89,59,70,25,71]
tree = BST(items[0])
for i in range(1, len(items)):
    tree.add(items[i])
tree.printInorder(0)
print(55 in tree)
print(70 in tree)
print(5 in tree)
print(1000 in tree)

# Task 3

class BST2(BinaryTree):
    def __init__(self, key, leftTree=None, rightTree=None):
        super().__init__(key, leftTree, rightTree)

    def add(self, key):
        curNode = self
        while True:
            if key < curNode.key:
                if curNode.leftTree == None:
                    curNode.leftTree = BST2(key)
                    break
                curNode = curNode.leftTree
            elif key > curNode.key:
                if curNode.rightTree == None:
                    curNode.rightTree = BST2(key)
                    break
                elif key < curNode.rightTree.key:
                    curNode.rightTree, curNode.rightTree.rightTree = BST2(key), curNode.rightTree
                    break
                curNode = curNode.rightTree

import random
items = [1,3,2,6,5,4,9,8,7]

random.shuffle(items)
print('List shuffled as:', items, '\n')
print('BST2 - Using squeeze in between add function')
tree = BST2(items[0])
for i in range(1, len(items)):
    tree.add(items[i])
tree.printInorder(0)

print()

print('BST using add as leafs function')
tree = BST(items[0])
for i in range(1, len(items)):
    tree.add(items[i])
tree.printInorder(0)