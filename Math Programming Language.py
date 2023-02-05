# Importing required libraries
import re
import time
import tkinter as tk

# Defining the Token class to store tokens
class LangCompiler:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.index = 0

    def lexer(self):
        # Tokenize the code
        # Split the code into individual tokens for +, -, *, /, numbers, etc.
        # Store the tokens in the self.tokens list
        token_specification = [
            ('NUMBER',  r'\d+(\.\d+)?'),  # Integer or decimal number
            ('PLUS',    r'\+'),           # Plus operator
            ('MINUS',   r'-'),            # Minus operator
            ('TIMES',   r'\*'),           # Multiply operator
            ('DIVIDE',  r'/'),            # Divide operator
            ('LPAREN',  r'\('),           # Left parenthesis
            ('RPAREN',  r'\)'),           # Right parenthesis
            ('COUNT',   r'count'),        # Count keyword
            ('NAME',    r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Variable name
            ('EQUALS',  r'='),            # Equals operator
            ('WS',      r'\s+'),          # Whitespace (ignored)
        ]
        tok_regex = '|'.join('(?P<%s>%s)' %
                             pair for pair in token_specification)
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            # Function to skip whitespaces
            if kind == 'WS':
                continue
            self.tokens.append((kind, value))
        self.tokens.append(('EOF', ''))

    def parser(self):
        # Parse the tokens into an abstract syntax tree (AST)
        # Use the tokens to construct a tree representation of the code's structure
        def expression():
            return addition()

        def addition():
            left = multiplication()
            while self.tokens[self.index][0] in ('PLUS', 'MINUS'):
                op_token = self.tokens[self.index]
                if op_token[0] == 'PLUS':
                    self.index += 1
                    left = ('ADD', left, multiplication())
                elif op_token[0] == 'MINUS':
                    self.index += 1
                    left = ('SUB', left, multiplication())
            return left

        def multiplication():
            left = primary()
            while self.tokens[self.index][0] in ('TIMES', 'DIVIDE'):
                op_token = self.tokens[self.index]
                if op_token[0] == 'TIMES':
                    self.index += 1
                    left = ('MUL', left, primary())
                elif op_token[0] == 'DIVIDE':
                    self.index += 1
                    left = ('DIV', left, primary()) 
            return left 
    
        def primary():  
            token = self.tokens[self.index]
            if token[0] == 'NUMBER':
                self.index += 1
                return ('NUM', float(token[1]))
            elif token[0] == 'LPAREN':
                self.index += 1
                result = expression()
                self.index += 1  # skip RPAREN
                return result
            elif token[0] == 'COUNT':
                self.index += 1
                return ('COUNT', expression())
            else:
                # Function to raise an error in case of invalid input
                raise Exception(f'Unexpected token: {token[0]}')

        return expression()
    
    def run(self):
        # Run the code
        # Execute the code represented by the AST
        def eval_expression(node):
            node_type = node[0]
            if node_type == 'NUM':
                return node[1]
            elif node_type == 'ADD':
                return eval_expression(node[1]) + eval_expression(node[2])
            elif node_type == 'SUB':
                return eval_expression(node[1]) - eval_expression(node[2])
            elif node_type == 'MUL':
                return eval_expression(node[1]) * eval_expression(node[2])
            elif node_type == 'DIV':
                return eval_expression(node[1]) / eval_expression(node[2])
            elif node_type == 'COUNT':
                result = eval_expression(node[1])
                return result
        ast = self.parser()
        return eval_expression(ast)

# Defining the Interpreter class to interpret the tokens
def window_of_start():
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Math Programming Language By Barry", font=(
        "Arial", 20), bg="green")
    text1 = tk.Label(root, text="\n\nHelp : You can count your syntaxt with entering 'count 5+1/2+(4*1)'",
                     font=("Arial", 14))
    text2 = tk.Label(root, text="\nThis Language support : + , - , * , / ,()\n",
                     font=("Arial", 14))
    text3 = tk.Label(
        root, text="Please enter your mathematical expression : ", font=("Arial", 18), bg="yellow")
    label.pack()
    text1.pack()
    text2.pack()
    text3.pack()

    input_field = tk.Entry(root)
    input_field.pack()

    def run_compiler():
        try:
            user_input = input_field.get()
            compiler = LangCompiler(user_input)
            compiler.lexer()
            result = compiler.run()
            for widget in root.winfo_children():
                widget.destroy()
            labell = tk.Label(root, text="\nYour Answer is : ",
                              font=("Arial", 20), fg="Green")
            textt1 = tk.Label(root, text=result, font=("Arial", 14))
            labell.pack()
            textt1.pack()

            def rerun():
                if int(input_rerun.get()) == 1:
                    window_of_start()
                else:

                    root.destroy()

            textt2 = tk.Label(root, text="\n\nThanks for Using my Language , Type 0 to Exit or 1 to Rerun", font=(
                "Arial", 14), fg="Blue")
            textt2.pack()
            input_rerun = tk.Entry(root)
            input_rerun.pack()

            run_button1 = tk.Button(root, text="Done", command=rerun)
            run_button1.pack()

        except:
            # Handle invalid input
            print("Error: Invalid mathematical expression")
            time.sleep(1)

    # Create a button for running the code
    run_button = tk.Button(root, text="Run", command=run_compiler)
    run_button.pack()


# # It makes the run definition to not be used by module but it uses as script
if __name__ == "__main__":

    # Create the main window
    root = tk.Tk()
    root.title("Math Calculator")

# Add a label with the text "Hi Welcome To my Language"
    label = tk.Label(root, text="Hi Welcome To my Language",
                     font=("Arial", 16))
    label.pack()

# Add a button with text "Continue"
    button = tk.Button(root, text="Continue", command=window_of_start)
    button.pack()

    root.mainloop()
