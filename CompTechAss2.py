import sys

# Global variable for the token
token = ' '

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def error(msg):
    sys.stderr.write(f"Error: {msg}\n")
    sys.exit(1)

def match(expected_token):
    global token
    if token == expected_token:
        token = sys.stdin.read(1)
    else:
        error(f"Expected '{expected_token}' but found '{token}'")

def expr():
    global token
    left = term()
    while token in ('+', '-'):
        op = token
        match(token)
        right = term()
        left = TreeNode(op, left, right)
    return left

def term():
    global token
    left = factor()
    while token == '*':
        op = token
        match(token)
        right = factor()
        left = TreeNode(op, left, right)
    return left

def factor():
    global token
    if token == '(':
        match('(')
        tree = expr()
        match(')')
        return tree
    elif token.isdigit():
        temp = 0
        while token.isdigit():
            temp = temp * 10 + int(token)
            token = sys.stdin.read(1)
        return TreeNode(str(temp))
    else:
        error(f"Unexpected token '{token}'")

def evaluate_tree(tree):
    if tree.value == '+':
        return evaluate_tree(tree.left) + evaluate_tree(tree.right)
    elif tree.value == '-':
        return evaluate_tree(tree.left) - evaluate_tree(tree.right)
    elif tree.value == '*':
        return evaluate_tree(tree.left) * evaluate_tree(tree.right)
    else:
        return int(tree.value)

def print_parse_tree(tree, indent=""):
    if tree is not None:
        if isinstance(tree.value, int):
            print(indent + str(tree.value))
        else:
            print(indent + tree.value)
        print_parse_tree(tree.left, indent + "  ")
        print_parse_tree(tree.right, indent + "  ")

def main():
    global token
    print("A RECURSIVE-DESCENT CALCULATOR.")
    print("\t the valid operations are +, - and *")
    print("Enter the calculation string, e.g. '34+6*56'")
    token = sys.stdin.read(1)
    if token == '\n':
        error("Empty input")
    tree = expr()
    if token == '\n':
        print("Parse Tree:")
        print_parse_tree(tree)
        result = evaluate_tree(tree)
        print("Result =", result)
    else:
        error(f"Unexpected token '{token}'")

if __name__ == "__main__":
    main()
