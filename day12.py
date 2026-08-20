"""
Advanced Calculator
Day 12 of my 100 days coding challenge
Advanced Calculator that supports: +, -, *, /, ** (power), %, parentheses, and basic functions
"""

import sys
import re
import math
from typing import List

class Calculator:
    def __init__(self):
        self.supported_operations = {
            '+': self._add,
            '-': self._subtract,
            '*': self._multiply,
            '/': self._divide,
            '^': self._power,
            '%': self._modulo,
        }
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log10,
            'ln': math.log,
            'abs': abs,
            'floor': math.floor,
            'ceil': math.ceil,
            'factorial': math.factorial,
        }
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
        }

    def _add(self, a: float, b: float) -> float:
        return a + b

    def _subtract(self, a: float, b: float) -> float:
        return a - b

    def _multiply(self, a: float, b: float) -> float:
        return a * b

    def _divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return a / b

    def _power(self, a: float, b: float) -> float:
        return a ** b

    def _modulo(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Modulo by zero is not allowed")
        return a % b

    def _tokenize(self, expression: str) -> List[str]:
        """Convert expression string into tokens"""
        # Remove whitespace (empty space)
        expression = expression.replace(' ', '')
        
        # Handle negative numbers at start or after operators
        expression = re.sub(r'(?<=[\(+\-*/^])-', '~', expression)
        if expression.startswith('-'):
            expression = '~' + expression[1:]
        
        # Tokenize
        pattern = r'(\d+\.\d+|\d+|[+\-*/()^%~]|[a-zA-Z_]+)'
        tokens = re.findall(pattern, expression)
        
        # Replace ~ with actual negative sign for parsing
        return tokens

    def _parse_number(self, token: str) -> float:
        """Convert token to number, handling constants"""
        if token in self.constants:
            return self.constants[token]
        try:
            return float(token)
        except ValueError:
            return None # type: ignore

    def _shunting_yard(self, tokens: List[str]) -> List[str]:
        """Convert infix expression to postfix (RPN) using shunting-yard algorithm"""
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '%': 2}
        associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R', '%': 'L'}
        
        output = []
        operators = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Handle negative numbers (prefixed with ~)
            if token == '~':
                # Look ahead to get the number
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    num = self._parse_number(next_token)
                    if num is not None:
                        output.append(str(-num))
                        i += 2
                        continue
                    else:
                        # Handle function with negative argument
                        output.append(token)
                        i += 1
                        continue
                else:
                    output.append(token)
                    i += 1
                    continue
            
            # Check if token is a number
            num = self._parse_number(token)
            if num is not None:
                output.append(str(num))
            elif token in self.functions:
                operators.append(token)
            elif token in self.supported_operations:
                while (operators and operators[-1] != '(' and
                       (precedence.get(operators[-1], 0) > precedence[token] or
                        (precedence.get(operators[-1], 0) == precedence[token] and
                         associativity[token] == 'L'))):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if operators and operators[-1] == '(':
                    operators.pop()
                # Check if there's a function before the parentheses
                if operators and operators[-1] in self.functions:
                    output.append(operators.pop())
            else:
                raise ValueError(f"Unknown token: {token}")
            
            i += 1
        
        # Pop remaining operators
        while operators:
            if operators[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operators.pop())
        
        return output

    def _evaluate_postfix(self, postfix: List[str]) -> float:
        """Evaluate postfix (RPN) expression"""
        stack = []
        
        for token in postfix:
            # Check if token is a number
            try:
                num = float(token)
                stack.append(num)
                continue
            except ValueError:
                pass
            
            # Handle negative marker
            if token == '~':
                if not stack:
                    raise ValueError("Invalid expression: negative sign without operand")
                stack.append(-stack.pop())
                continue
            
            # Handle functions
            if token in self.functions:
                if not stack:
                    raise ValueError(f"Function {token} requires an argument")
                arg = stack.pop()
                try:
                    result = self.functions[token](arg)
                    stack.append(result)
                except ValueError as e:
                    raise ValueError(f"Error in {token}({arg}): {e}")
                continue
            
            # Handle operators
            if token in self.supported_operations:
                if len(stack) < 2:
                    raise ValueError(f"Operator {token} requires two operands")
                b = stack.pop()
                a = stack.pop()
                try:
                    result = self.supported_operations[token](a, b)
                    stack.append(result)
                except Exception as e:
                    raise ValueError(f"Error in {a} {token} {b}: {e}")
                continue
            
            raise ValueError(f"Unknown token in evaluation: {token}")
        
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        
        return stack[0]

    def evaluate(self, expression: str) -> float:
        """Main method to evaluate an expression"""
        if not expression or expression.isspace():
            raise ValueError("Empty expression")
        
        try:
            tokens = self._tokenize(expression)
            postfix = self._shunting_yard(tokens)
            result = self._evaluate_postfix(postfix)
            return result
        except ZeroDivisionError as e:
            raise e
        except ValueError as e:
            raise ValueError(f"Invalid expression: {e}")
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {e}")

def interactive_mode():
    """Run calculator in interactive mode"""
    calc = Calculator()
    print("=" * 60)
    print("Supported operations: +, -, *, /, ^ (power), % (modulo)")
    print("Supported functions: sin, cos, tan, sqrt, log, ln, abs, floor, ceil, factorial")
    print("Constants: pi, e, tau")
    print("Type 'help' for more info, 'quit' or 'exit' to quit")
    print("=" * 60)
    
    # Load history
    history = []
    history_file = ".calculator_history.txt"
    try:
        with open(history_file, 'r') as f:
            history = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        pass
    
    while True:
        try:
            # Show prompt with history number
            prompt = f"In [{len(history)}]: " if history else ">>> "
            expr = input(prompt).strip()
            
            if not expr:
                continue
            
            # Handle special commands
            if expr.lower() in ['quit', 'exit', 'q']:
                break
            elif expr.lower() == 'help':
                print("\nExamples:")
                print("  2 + 3 * 4")
                print("  (2 + 3) * 4")
                print("  sin(pi/2)")
                print("  sqrt(16) + 3^2")
                print("  factorial(5)")
                print("  log(100) + ln(e)")
                print("  abs(-5) * 2")
                print("  floor(3.7) + ceil(4.2)")
                print("  10 % 3")
                print("\nYou can also use variables from previous results:")
                print("  ans = 5 + 3")
                print("  ans * 2")
                print("  _ (previous result)")
                continue
            elif expr.lower() == 'history':
                for i, e in enumerate(history):
                    print(f"{i}: {e}")
                continue
            elif expr.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
            # Handle variable assignment
            if '=' in expr and not expr.startswith('='):
                parts = expr.split('=', 1)
                var_name = parts[0].strip()
                var_expr = parts[1].strip()
                
                # Check if variable name is valid (not a function name)
                if var_name in calc.functions or var_name in calc.supported_operations:
                    print(f"Cannot assign to reserved name: {var_name}")
                    continue
                
                try:
                    result = calc.evaluate(var_expr)
                    calc.constants[var_name] = result
                    print(f"{var_name} = {result}")
                    history.append(expr)
                except Exception as e:
                    print(f"Error: {e}")
                continue
            
            # Replace '_' with last result
            if expr.startswith('_'):
                if history:
                    try:
                        last_result = float(history[-1].split('=')[-1].strip())
                        expr = expr.replace('_', str(last_result))
                    except:
                        pass
            
            # Evaluate expression
            result = calc.evaluate(expr)
            print(f"= {result}")
            
            # Store in history
            history.append(f"{expr} = {result}")
            
            # Save history
            try:
                with open(history_file, 'w') as f:
                    f.write('\n'.join(history[-100:]))  # Keep last 100 entries
            except:
                pass
            
        except KeyboardInterrupt:
            print("\nInterrupted. Type 'quit' to exit.")
            continue
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point with command-line argument support"""
    if len(sys.argv) > 1:
        # Command-line mode
        calc = Calculator()
        expression = ' '.join(sys.argv[1:])
        try:
            result = calc.evaluate(expression)
            print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    import os
    main()