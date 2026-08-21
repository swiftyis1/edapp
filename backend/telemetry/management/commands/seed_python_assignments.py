import json
from django.core.management.base import BaseCommand
from telemetry.models import PythonAssignment

class Command(BaseCommand):
    help = "Seeds the database with Module 0 through Module 3 Python assignments, using clean interactive example tags and explicit assert prefix check structures."

    def handle(self, *args, **options):
        assignments_data = [
{
                "title": "Exercise 0: Welcome & Platform Orientation",
                "slug": "system_orientation",
                "module": 0,
                "prompt": (
                    "### Welcome to the Python Learning Workspace!\n"
                    "This environment is designed to help you learn and experiment with Python programming. "
                    "Let's walk through how to use the system, key conceptual tools, and what you will learn in this course.\n\n"
                    "### 1. How to Use Our System\n"
                    "*   **Code Editor**: The editor panel (main.py) is where you write your Python code. "
                    "It features code highlighting, auto-indentation, and syntax auto-completions.\n"
                    "*   **Run Code Button**: Executes your current script in a WebAssembly sandbox (directly in your browser). "
                    "The output will display in the console terminal below.\n"
                    "*   **Submit & Grade Button**: Evaluates your code against autograding assertions and registers your grade.\n"
                    "*   **Reset Starter Code Button**: Located next to main.py, this button discards all current edits and reverts "
                    "the editor back to the assignment's original starter code template.\n"
                    "*   **Try in Editor Button**: In exercises containing examples, clicking this button loads the example "
                    "code directly into the editor for you to run and play with.\n\n"
                    "### 2. Comments in Python\n"
                    "A comment is a line of notes written for human readers. Python completely ignores comments when executing code. "
                    "To write a comment in Python, start the line with the `#` symbol.\n\n"
                    "Example:\n"
                    "  # This is a comment. Python will not execute this line!\n"
                    "  x = 5  # You can also add comments to the end of a code line\n\n"
                    "### 3. Algorithms & Pseudocode\n"
                    "*   **Algorithm**: A step-by-step logical sequence of instructions designed to solve a specific problem or perform a task.\n"
                    "*   **Pseudocode**: An informal, plain-English description of an algorithm. You write pseudocode to map out the "
                    "logical steps of your program before translating it into actual Python code.\n"
                    "Example of Pseudocode:\n"
                    "  Read base and exponent\n"
                    "  Raise base to power of exponent\n"
                    "  Print the formatted result string\n\n"
                    "### 4. What You Will Achieve & Learn\n"
                    "By the end of this curriculum, you will master:\n"
                    "1. Variables, expressions, and string operations.\n"
                    "2. Selection structures (if/else) and loop iterations.\n"
                    "3. Function designs, parameter passing, and variable scopes.\n"
                    "4. Object-Oriented Programming (OOP) class designs, encapsulations, inheritance, and polymorphism.\n"
                    "5. 1D sequences, list mutators, slices, and 2D grid matrix traversals.\n"
                    "6. Binary search, custom sorting algorithms, and recursion mechanics.\n\n"
                    "### Task Instructions\n"
                    "1. Read the orientation guide above.\n"
                    "2. Write a Python comment in the editor using the `#` character (e.g. `# Hello Python comment`).\n"
                    "3. Click **Submit & Grade** to complete your system orientation!"
                ),
                "starter_code": (
                    "# Write a Python comment below to test the editor\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "assert '#' in __student_code__", "msg": "You must write a comment in the editor starting with the '#' character."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 1: Variable Assignment",
                "slug": "var_assignment",
                "module": 1,
                "prompt": (
                    "### Curriculum: Variables & Printing\n"
                    "In Python, a variable is a named storage location that holds data. "
                    "You assign a value to a variable using the assignment operator =. "
                    "Python is dynamically typed, meaning you do not need to specify the data type "
                    "when creating the variable.\n\n"
                    "To display the value of a variable on the console, use the built-in print() function.\n\n"
                    "### Example Code\n"
                    "Load this example code to see variables and print statements in action:\n"
                    "<example_code>\n"
                    "message = \"Hello World\"\n"
                    "count = 10\n"
                    "print(message)\n"
                    "print(count)\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Create a variable named `name` and assign it your name as a string (e.g. `\"Alex\"`).\n"
                    "2. Create another variable named `age` and assign it your age as an integer (e.g. `17`).\n"
                    "3. Print both variables on separate lines."
                ),
                "starter_code": (
                    "# Exercise 1: Variables & Expressions\n"
                    "# 1. Create a variable 'name' and assign a string value.\n"
                    "# 2. Create a variable 'age' and assign an integer value.\n"
                    "# 3. Print both variables.\n\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "assert isinstance(name, str)", "msg": "Variable 'name' must be a string."},
                        {"code": "assert len(name) > 0", "msg": "Variable 'name' cannot be empty."},
                        {"code": "assert isinstance(age, int)", "msg": "Variable 'age' must be an integer."},
                        {"code": "assert age > 0", "msg": "Variable 'age' must be a positive number."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 2: Basic Arithmetic",
                "slug": "arithmetic_ops",
                "module": 1,
                "prompt": (
                    "### Curriculum: Arithmetic Operators\n"
                    "Python uses standard symbols for arithmetic calculations:\n"
                    "*   Addition: +\n"
                    "*   Subtraction: -\n"
                    "*   Multiplication: *\n"
                    "*   Division (float result): /\n"
                    "*   Modulo (remainder of division): %\n\n"
                    "### Example Code\n"
                    "Load and run this example code to calculate values and print their results:\n"
                    "<example_code>\n"
                    "sum_result = 5 + 3\n"
                    "rem_result = 7 % 3\n"
                    "print(sum_result)  # Output will show 8\n"
                    "print(rem_result)  # Output will show 1\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. You are given variables `num1 = 15` and `num2 = 4`.\n"
                    "2. Calculate the sum, product, and remainder (modulo) of `num1` divided by `num2`.\n"
                    "3. Assign them to variables `sum_val`, `prod_val`, and `rem_val` respectively, and print them."
                ),
                "starter_code": (
                    "# Exercise 2: Basic Arithmetic\n"
                    "num1 = 15\n"
                    "num2 = 4\n\n"
                    "# Write your calculations here\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "assert sum_val == 19", "msg": "Variable 'sum_val' must equal 19 (15 + 4)."},
                        {"code": "assert prod_val == 60", "msg": "Variable 'prod_val' must equal 60 (15 * 4)."},
                        {"code": "assert rem_val == 3", "msg": "Variable 'rem_val' must equal 3 (15 % 4)."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 3: Type Casting",
                "slug": "type_casting",
                "module": 1,
                "prompt": (
                    "### Curriculum: Type Conversion (Casting)\n"
                    "Sometimes data is read in one format (like text) but needed in another (like numbers). "
                    "Converting a value from one data type to another is called type casting.\n"
                    "In Python, you cast values using type conversion functions:\n"
                    "*   int(x) converts x to an integer.\n"
                    "*   float(x) converts x to a float.\n"
                    "*   str(x) converts x to a string.\n\n"
                    "### Example Code\n"
                    "Load and run this example code to see how text conversions behave:\n"
                    "<example_code>\n"
                    "numeric_str = \"100\"\n"
                    "number = int(numeric_str)\n"
                    "print(number)  # Output will show the integer 100\n"
                    "print(type(number))  # Output will show <class 'int'>\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. You are given two string variables: `str_num = '42'` and `str_float = '3.14'`.\n"
                    "2. Cast `str_num` to an integer named `int_val` and `str_float` to a float named `float_val`.\n"
                    "3. Calculate and print their sum."
                ),
                "starter_code": (
                    "# Exercise 3: Type Casting\n"
                    "str_num = '42'\n"
                    "str_float = '3.14'\n\n"
                    "# Cast the variables and calculate the sum\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "assert int_val == 42", "msg": "Variable 'int_val' must be the integer 42."},
                        {"code": "assert isinstance(int_val, int)", "msg": "Variable 'int_val' must be of type 'int'."},
                        {"code": "assert float_val == 3.14", "msg": "Variable 'float_val' must be the float 3.14."},
                        {"code": "assert isinstance(float_val, float)", "msg": "Variable 'float_val' must be of type 'float'."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 4: String Interpolation",
                "slug": "string_concat",
                "module": 1,
                "prompt": (
                    "### Curriculum: Formatted Strings (f-strings)\n"
                    "Formatted string literals, or f-strings, let you embed variables directly "
                    "inside string literals using curly braces {}. To create an f-string, prefix the string with an 'f' before the opening quote.\n\n"
                    "### Example Code\n"
                    "Load and run this example to see f-string syntax in action:\n"
                    "<example_code>\n"
                    "fruit = \"apple\"\n"
                    "qty = 5\n"
                    "message = f\"I bought {qty} {fruit}s.\"\n"
                    "print(message)  # Prints: I bought 5 apples.\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Create a variable `item` and set it to `'laptop'`.\n"
                    "2. Create a variable `price` and set it to `899.99`.\n"
                    "3. Use python f-strings to print exactly the sentence:\n"
                    "   `The price of the laptop is $899.99.`"
                ),
                "starter_code": (
                    "# Exercise 4: String Interpolation\n"
                    "# 1. Create variable 'item' and set to 'laptop'\n"
                    "# 2. Create variable 'price' and set to 899.99\n"
                    "# 3. Print the formatted message using an f-string\n\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "assert item == 'laptop'", "msg": "Variable 'item' must be set to 'laptop'."},
                        {"code": "assert price == 899.99", "msg": "Variable 'price' must be set to 899.99."}
                    ],
                    "io_tests": [
                        {"inputs": [], "expected_output": "The price of the laptop is $899.99."}
                    ]
                }
            },
{
                "title": "Exercise 5: Input & Math Calculations",
                "slug": "input_math",
                "module": 1,
                "prompt": (
                    "### Curriculum: Reading Console Input\n"
                    "The input() function reads a line of text entered by the user in the console terminal. "
                    "Crucial detail: input() always returns a string. If you need to perform calculations on "
                    "the input, you must cast it to a numerical type (int or float) first.\n\n"
                    "### Example Code\n"
                    "Load this code and type a number into the terminal when prompted to test it:\n"
                    "<example_code>\n"
                    "user_text = input(\"Enter a number: \")\n"
                    "value = float(user_text)\n"
                    "print(f\"You entered: {value}\")\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Read a floating-point number from user console input using `input()`.\n"
                    "2. Multiply the input number by 1.5, and print the result as a float."
                ),
                "starter_code": (
                    "# Exercise 5: Input & Math Calculations\n"
                    "# 1. Prompt the user and read a floating-point number\n"
                    "# 2. Multiply by 1.5 and print the result\n\n"
                ),
                "test_suite": {
                    "assertions": [],
                    "io_tests": [
                        {"inputs": ["10.0"], "expected_output": "15.0"},
                        {"inputs": ["4.5"], "expected_output": "6.75"}
                    ]
                }
            },
{
                "title": "Module 1 Assessment: Powers & Formatting",
                "slug": "unit1_assessment",
                "module": 1,
                "prompt": (
                    "### Summative Assessment: Module 1\n"
                    "This task acts as a summative assessment evaluating your variables, casting, input capture, "
                    "math operations, and string formatting skills. No curriculum help or example code is provided for this exercise.\n\n"
                    "### Task Instructions\n"
                    "1. Read a base number from console input using `input()`.\n"
                    "2. Read an exponent number from console input using a second `input()`.\n"
                    "3. Convert both inputs to floating-point numbers (`float`).\n"
                    "4. Calculate the base raised to the exponent power using `**` or Python's built-in `pow()` function.\n"
                    "5. Print a message using f-strings exactly in this format:\n"
                    "   `[base] raised to the power of [exponent] is [result].` (e.g., `4.0 raised to the power of 2.0 is 16.0.`)\n"
                ),
                "starter_code": (
                    "# Module 1 Assessment: Powers & Formatting\n"
                    "# Write your code here to read base/exponent, calculate result, and print formatted output\n"
                ),
                "test_suite": {
                    "assertions": [],
                    "io_tests": [
                        {"inputs": ["2.0", "3.0"], "expected_output": "2.0 raised to the power of 3.0 is 8.0."},
                        {"inputs": ["5.0", "0.0"], "expected_output": "5.0 raised to the power of 0.0 is 1.0."}
                    ]
                }
            },
{
                "title": "Exercise 6: Selection & Even/Odd",
                "slug": "if_statement",
                "module": 2,
                "prompt": (
                    "### Curriculum: Conditionals (if/else)\n"
                    "Conditionals let you control execution paths based on Boolean conditions (expressions evaluating to True or False). "
                    "In Python, this is written using if, elif (else if), and else blocks, with indentation defining the code blocks.\n\n"
                    "### Example Code\n"
                    "Load this code and run it to see how conditional logic evaluates grades:\n"
                    "<example_code>\n"
                    "score = 85\n"
                    "if score >= 90:\n"
                    "    print(\"Grade A\")\n"
                    "elif score >= 80:\n"
                    "    print(\"Grade B\")\n"
                    "else:\n"
                    "    print(\"Grade C\")\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `check_even(num)` that returns `True` if `num` is even, and `False` otherwise.\n"
                    "2. You MUST utilize an `if` statement structure in your implementation."
                ),
                "starter_code": (
                    "# Exercise 6: Selection & Even/Odd\n"
                    "def check_even(num):\n"
                    "    # Write your check_even function here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.If) for node in ast.walk(tree))", "msg": "You must use an if statement in your code."},
                        {"code": "assert check_even(4) is True", "msg": "check_even(4) should return True."},
                        {"code": "assert check_even(7) is False", "msg": "check_even(7) should return False."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 7: Logical Operators",
                "slug": "logical_operators",
                "module": 2,
                "prompt": (
                    "### Curriculum: Boolean Logic (and, or, not)\n"
                    "Logical operators let you combine multiple Boolean conditions:\n"
                    "*   and: Returns True if both expressions are True.\n"
                    "*   or: Returns True if at least one expression is True.\n"
                    "*   not: Reverses the Boolean state of the expression.\n"
                    "You can also use comparison chaining (e.g. 10 < x < 20) in Python.\n\n"
                    "### Example Code\n"
                    "Load and run this code to see logical checks evaluate numerical bounds:\n"
                    "<example_code>\n"
                    "x = 5\n"
                    "y = 10\n"
                    "if x > 0 and y > 0:\n"
                    "    print(\"Both numbers are positive\")\n"
                    "if 1 < x < 10:\n"
                    "    print(\"x is between 1 and 10\")\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `is_teenager(age)` that returns `True` if `age` is between 13 and 19 (inclusive), and `False` otherwise.\n"
                    "2. You MUST use logical operators (`and`, `or`, `not`) or comparison chaining."
                ),
                "starter_code": (
                    "# Exercise 7: Logical Operators\n"
                    "def is_teenager(age):\n"
                    "    # Write your is_teenager function here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.BoolOp) for node in ast.walk(tree)) or any(isinstance(node, ast.Compare) and len(node.ops) > 1 for node in ast.walk(tree))", "msg": "You must use logical operators or comparison chaining in your code."},
                        {"code": "assert is_teenager(15) is True", "msg": "is_teenager(15) should return True."},
                        {"code": "assert is_teenager(12) is False", "msg": "is_teenager(12) should return False."},
                        {"code": "assert is_teenager(20) is False", "msg": "is_teenager(20) should return False."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 8: While Loop",
                "slug": "while_loop",
                "module": 2,
                "prompt": (
                    "### Curriculum: While Loops\n"
                    "A while loop repeatedly executes a block of code as long as its condition remains True. "
                    "Make sure the loop body modifies a variable so that the loop condition eventually becomes False, avoiding infinite loops.\n\n"
                    "### Example Code\n"
                    "Load and run this code to see a count down from 5 to 1:\n"
                    "<example_code>\n"
                    "count = 5\n"
                    "while count > 0:\n"
                    "    print(count)\n"
                    "    count -= 1\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `count_digits(n)` that returns the number of digits in a positive integer `n`.\n"
                    "2. You MUST use a `while` loop to repeatedly divide the number by 10 (`n //= 10` or `n = n // 10`)."
                ),
                "starter_code": (
                    "# Exercise 8: While Loop\n"
                    "def count_digits(n):\n"
                    "    # Write your count_digits function here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.While) for node in ast.walk(tree))", "msg": "You must use a while loop in your code."},
                        {"code": "assert count_digits(12345) == 5", "msg": "count_digits(12345) should return 5."},
                        {"code": "assert count_digits(7) == 1", "msg": "count_digits(7) should return 1."},
                        {"code": "assert count_digits(100) == 3", "msg": "count_digits(100) should return 3."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 9: For Loop Summation",
                "slug": "for_loop",
                "module": 2,
                "prompt": (
                    "### Curriculum: For Loops & Range\n"
                    "A for loop in Python iterates over a sequence (like a list or a range of numbers). "
                    "The range(stop) function generates a sequence starting at 0 and up to (but not including) stop.\n\n"
                    "### Example Code\n"
                    "Load and run this code to print the square numbers of 0 to 4:\n"
                    "<example_code>\n"
                    "for i in range(5):\n"
                    "    print(f\"{i} squared is {i**2}\")\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `sum_multiples(n)` that returns the sum of all multiples of 3 or 5 less than `n` (exclusive).\n"
                    "2. You MUST use a `for` loop."
                ),
                "starter_code": (
                    "# Exercise 9: For Loop Summation\n"
                    "def sum_multiples(n):\n"
                    "    # Write your sum_multiples function here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.For) for node in ast.walk(tree))", "msg": "You must use a for loop in your code."},
                        {"code": "assert sum_multiples(10) == 23", "msg": "sum_multiples(10) should return 23."},
                        {"code": "assert sum_multiples(16) == 60", "msg": "sum_multiples(16) should return 60."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 10: Nested Loops Grid",
                "slug": "nested_loop",
                "module": 2,
                "prompt": (
                    "### Curriculum: Nested Loops\n"
                    "Nested loops occur when a loop is placed inside another loop. This is common for working with multi-dimensional "
                    "structures, like coordinate grids, board layouts, or matrix dimensions.\n\n"
                    "### Example Code\n"
                    "Load and run this code to generate coordinate pairs for a 2x3 grid:\n"
                    "<example_code>\n"
                    "for r in range(2):\n"
                    "    for c in range(3):\n"
                    "        print(f\"Row {r}, Col {c}\")\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `grid_pattern(rows, cols)` that returns a string representing a grid of row and column coordinate pairs.\n"
                    "2. For example, `grid_pattern(2, 3)` should return exactly:\n"
                    "   `\"(0,0)(0,1)(0,2)\\n(1,0)(1,1)(1,2)\\n\"`.\n"
                    "3. You MUST use nested `for` loops in your code."
                ),
                "starter_code": (
                    "# Exercise 10: Nested Loops Grid\n"
                    "def grid_pattern(rows, cols):\n"
                    "    # Write your grid_pattern function here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); for_loops = [node for node in ast.walk(tree) if isinstance(node, ast.For)]; assert any(any(isinstance(child, ast.For) for child in ast.walk(f) if child is not f) for f in for_loops)", "msg": "You must use nested for loops in your code."},
                        {"code": "assert grid_pattern(2, 3) == \"(0,0)(0,1)(0,2)\\n(1,0)(1,1)(1,2)\\n\"", "msg": "grid_pattern(2, 3) should return correct coordinates pattern."},
                        {"code": "assert grid_pattern(1, 1) == \"(0,0)\\n\"", "msg": "grid_pattern(1, 1) should return correct coordinates pattern."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Module 2 Assessment: Even Squares Accumulator",
                "slug": "unit2_assessment",
                "module": 2,
                "prompt": (
                    "### Summative Assessment: Module 2\n"
                    "This task acts as a summative assessment evaluating your conditionals, logical comparison, and "
                    "loop structures. No curriculum help or example code is provided for this exercise.\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `sum_even_squares(n)` that calculates and returns the sum of the squares of all even numbers from 2 up to `n` (inclusive).\n"
                    "2. For example, `sum_even_squares(6)` should calculate `2^2 + 4^2 + 6^2 = 4 + 16 + 36 = 56` and return `56`.\n"
                    "3. You MUST use a loop (`for` or `while`) and an `if` statement structure in your implementation."
                ),
                "starter_code": (
                    "# Module 2 Assessment: Even Squares Accumulator\n"
                    "def sum_even_squares(n):\n"
                    "    # Write your code here to calculate sum of even squares up to n\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.If) for node in ast.walk(tree))", "msg": "You must use an if statement in your code."},
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.For) or isinstance(node, ast.While) for node in ast.walk(tree))", "msg": "You must use a loop structure (for or while) in your code."},
                        {"code": "assert sum_even_squares(6) == 56", "msg": "sum_even_squares(6) should return 56 (4 + 16 + 36)."},
                        {"code": "assert sum_even_squares(3) == 4", "msg": "sum_even_squares(3) should return 4 (2^2)."},
                        {"code": "assert sum_even_squares(1) == 0", "msg": "sum_even_squares(1) should return 0."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 11: Welcome & Function Declaration",
                "slug": "func_declaration",
                "module": 3,
                "prompt": (
                    "### Curriculum: Python Functions\n"
                    "Functions are reusable blocks of code that perform a specific task. "
                    "You define a function using the def keyword, followed by the function name, parentheses (), and a colon :.\n\n"
                    "To return a value from a function back to where it was called, use the return statement. Once a return statement is executed, the function exits immediately.\n\n"
                    "### Example Code\n"
                    "Load this example code to see how a value-returning function works:\n"
                    "<example_code>\n"
                    "def get_pi():\n"
                    "    return 3.14159\n\n"
                    "pi_val = get_pi()\n"
                    "print(pi_val)\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function named `welcome_message` that prints the exact string `\"Welcome to Module 3!\"` (this is a void function, so it does not return a value).\n"
                    "2. Write a function named `get_lucky_number` that returns the integer `7`."
                ),
                "starter_code": (
                    "# Exercise 11: Welcome & Function Declaration\n"
                    "# Define welcome_message and get_lucky_number below\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]; assert 'welcome_message' in funcs", "msg": "You must define a welcome_message function."},
                        {"code": "import ast; tree = ast.parse(__student_code__); funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]; assert 'get_lucky_number' in funcs", "msg": "You must define a get_lucky_number function."},
                        {"code": "assert get_lucky_number() == 7", "msg": "get_lucky_number() should return 7."}
                    ],
                    "io_tests": [
                        {"inputs": [], "expected_output": "Welcome to Module 3!"}
                    ]
                }
            },
{
                "title": "Exercise 12: Parameters & Arguments",
                "slug": "param_passing",
                "module": 3,
                "prompt": (
                    "### Curriculum: Function Parameters\n"
                    "Parameters are variables listed inside the parentheses of a function definition. They act as placeholders for values passed into the function when it is called (arguments).\n\n"
                    "### Example Code\n"
                    "Load this code to see multiple parameters and basic calculations:\n"
                    "<example_code>\n"
                    "def format_name(first, last):\n"
                    "    return f\"{last}, {first}\"\n\n"
                    "print(format_name(\"John\", \"Doe\"))\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function named `calculate_rectangle_area(length, width)` that takes two parameters and returns their product.\n"
                    "2. Write a function named `introduce_student(name, grade)` that returns an f-string exactly in this format:\n"
                    "   `\"[name] is in grade [grade].\"` (e.g. `introduce_student(\"Alex\", 12)` should return `\"Alex is in grade 12.\"`)."
                ),
                "starter_code": (
                    "# Exercise 12: Parameters & Arguments\n"
                    "# Define calculate_rectangle_area and introduce_student below\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "assert calculate_rectangle_area(5, 4) == 20", "msg": "calculate_rectangle_area(5, 4) should return 20."},
                        {"code": "assert calculate_rectangle_area(10, 3.5) == 35.0", "msg": "calculate_rectangle_area(10, 3.5) should return 35.0."},
                        {"code": "assert introduce_student('Blake', 11) == 'Blake is in grade 11.'", "msg": "introduce_student('Blake', 11) should return 'Blake is in grade 11.'"}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 13: Scope Rules & Local Variables",
                "slug": "scoping_rules",
                "module": 3,
                "prompt": (
                    "### Curriculum: Scope & Namespaces\n"
                    "Scope refers to the region of a program where a variable is accessible.\n"
                    "*   Local Scope: Variables created inside a function belong to that function's local scope and cannot be accessed outside it.\n"
                    "*   Global Scope: Variables created in the main body of the script belong to the global scope and are accessible everywhere.\n"
                    "Good practice is to avoid modifying or referring to global variables inside local functions, as this creates side effects. You must not use the `global` keyword.\n\n"
                    "### Example Code\n"
                    "Load this example code to see how local variables are isolated inside functions:\n"
                    "<example_code>\n"
                    "x = 10  # Global variable\n\n"
                    "def add_five(n):\n"
                    "    x = 5  # Local variable 'x' (does not change the global 'x'!)\n"
                    "    return n + x\n\n"
                    "print(add_five(10))  # Prints 15\n"
                    "print(x)             # Prints 10 (global x is unchanged)\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "You are given a global variable `multiplier = 2`.\n"
                    "1. Write a function `multiply_by_five(n)` that multiplies the input parameter `n` by `5` and returns the result.\n"
                    "2. Inside the function, you MUST declare a local variable `factor = 5` and use it. You MUST NOT access or modify the global variable `multiplier` inside the function.\n"
                    "3. You must not use the `global` keyword."
                ),
                "starter_code": (
                    "# Exercise 13: Scope Rules & Local Variables\n"
                    "multiplier = 2\n\n"
                    "def multiply_by_five(n):\n"
                    "    # Write your function here using a local variable factor = 5\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); func = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == 'multiply_by_five'][0]; assert not any(isinstance(c, ast.Global) for c in ast.walk(func))", "msg": "You must not use the 'global' keyword inside your function."},
                        {"code": "import ast; tree = ast.parse(__student_code__); func = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == 'multiply_by_five'][0]; names = [n.id for n in ast.walk(func) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)]; assert 'multiplier' not in names", "msg": "You must not read the global variable 'multiplier' inside your function."},
                        {"code": "assert multiply_by_five(10) == 50", "msg": "multiply_by_five(10) should return 50."},
                        {"code": "assert multiply_by_five(3) == 15", "msg": "multiply_by_five(3) should return 15."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 14: Standard Math Library",
                "slug": "math_library",
                "module": 3,
                "prompt": (
                    "### Curriculum: Standard Libraries & Math Module\n"
                    "Python has a built-in library of modules that provide useful functions. To use a module, you must import it using the import keyword.\n"
                    "The math module provides mathematical functions for floating-point calculations, such as:\n"
                    "*   math.sqrt(x): Returns the square root of x.\n"
                    "*   math.ceil(x): Rounds a number UP to the nearest integer.\n"
                    "*   math.floor(x): Rounds a number DOWN to the nearest integer.\n\n"
                    "### Example Code\n"
                    "Load this example code to see how to import and use the math library:\n"
                    "<example_code>\n"
                    "import math\n"
                    "val = 4.7\n"
                    "print(math.floor(val))  # Prints 4\n"
                    "print(math.ceil(val))   # Prints 5\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `hypotenuse(a, b)` that calculates the hypotenuse of a right-angled triangle using the formula: `sqrt(a^2 + b^2)`.\n"
                    "2. You MUST use the `math` library functions (`math.sqrt` or `math.pow`) for calculations.\n"
                    "3. Write another function `round_up(x)` that returns the value of `x` rounded up to the nearest integer using `math.ceil`."
                ),
                "starter_code": (
                    "# Exercise 14: Standard Math Library\n"
                    "import math\n\n"
                    "def hypotenuse(a, b):\n"
                    "    # Write your hypotenuse function here\n"
                    "    pass\n\n"
                    "def round_up(x):\n"
                    "    # Write your round_up function here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.Import) and any(alias.name == 'math' for alias in node.names) or isinstance(node, ast.ImportFrom) and node.module == 'math' for node in ast.walk(tree))", "msg": "You must import the math module."},
                        {"code": "assert hypotenuse(3, 4) == 5.0", "msg": "hypotenuse(3, 4) should return 5.0."},
                        {"code": "assert hypotenuse(5, 12) == 13.0", "msg": "assert hypotenuse(5, 12) should return 13.0."},
                        {"code": "assert round_up(4.1) == 5", "msg": "round_up(4.1) should return 5."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 15: Random Generator Simulation",
                "slug": "random_gen",
                "module": 3,
                "prompt": (
                    "### Curriculum: Random Library\n"
                    "The random module provides tools to generate pseudo-random numbers and selections:\n"
                    "*   random.randint(a, b): Returns a random integer N such that a <= N <= b.\n"
                    "*   random.choice(seq): Returns a random element from a non-empty sequence (like a list or tuple).\n\n"
                    "### Example Code\n"
                    "Load this example to see how to generate random numbers:\n"
                    "<example_code>\n"
                    "import random\n"
                    "roll = random.randint(1, 6)  # Simulates rolling a 6-sided die\n"
                    "print(roll)\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `roll_dice(sides)` that returns a random integer from `1` to `sides` (inclusive) using `random.randint`.\n"
                    "2. Write a function `pick_card()` that randomly returns one of these four string values: `'Hearts'`, `'Diamonds'`, `'Clubs'`, or `'Spades'` using `random.choice`.\n"
                    "3. You MUST import the `random` module."
                ),
                "starter_code": (
                    "# Exercise 15: Random Generator Simulation\n"
                    "import random\n\n"
                    "def roll_dice(sides):\n"
                    "    # Write your roll_dice function here\n"
                    "    pass\n\n"
                    "def pick_card():\n"
                    "    # Write your pick_card function here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.Import) and any(alias.name == 'random' for alias in node.names) or isinstance(node, ast.ImportFrom) and node.module == 'random' for node in ast.walk(tree))", "msg": "You must import the random module."},
                        {"code": "assert all(1 <= roll_dice(6) <= 6 for _ in range(50))", "msg": "roll_dice(6) should always return an integer between 1 and 6."},
                        {"code": "assert set(pick_card() for _ in range(50)) == {'Hearts', 'Diamonds', 'Clubs', 'Spades'}", "msg": "pick_card() should return a random suit from the list."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Module 3 Assessment: Sphere Calculations",
                "slug": "unit3_assessment",
                "module": 3,
                "prompt": (
                    "### Summative Assessment: Module 3\n"
                    "This task acts as a summative assessment evaluating your custom function declarations, parameter passing, return values, "
                    "and standard library usage. No curriculum helper explanations or examples are provided for this exercise.\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `sphere_volume(radius)` that calculates and returns the volume of a sphere using the formula: `(4/3) * pi * radius^3`.\n"
                    "2. Write a function `sphere_surface_area(radius)` that calculates and returns the surface area of a sphere using the formula: `4 * pi * radius^2`.\n"
                    "3. You MUST use the constant `math.pi` from the `math` library for the value of pi.\n"
                    "4. Round both returned results to exactly 2 decimal places using Python's built-in `round(value, 2)` function before returning them."
                ),
                "starter_code": (
                    "# Module 3 Assessment: Sphere Calculations\n"
                    "import math\n\n"
                    "def sphere_volume(radius):\n"
                    "    # Write your sphere_volume function here\n"
                    "    pass\n\n"
                    "def sphere_surface_area(radius):\n"
                    "    # Write your sphere_surface_area function here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.Import) and any(alias.name == 'math' for alias in node.names) or isinstance(node, ast.ImportFrom) and node.module == 'math' for node in ast.walk(tree))", "msg": "You must import the math module."},
                        {"code": "assert sphere_volume(3) == 113.1", "msg": "sphere_volume(3) should return 113.1 (rounded to 2 decimal places)."},
                        {"code": "assert sphere_surface_area(3) == 113.1", "msg": "sphere_surface_area(3) should return 113.1."},
                        {"code": "assert sphere_volume(1.5) == 14.14", "msg": "sphere_volume(1.5) should return 14.14."},
                        {"code": "assert sphere_surface_area(1.5) == 28.27", "msg": "sphere_surface_area(1.5) should return 28.27."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 16: Class Blueprints",
                "slug": "class_blueprint",
                "module": 4,
                "prompt": (
                    "### Curriculum: Class Blueprints & Objects\n"
                    "In Object-Oriented Programming (OOP), a **class** is a blueprint or template for creating objects. "
                    "An **object** is an instance of a class. Classes bundle attributes (variables) and behaviors (methods) together.\n\n"
                    "You define a class using the `class` keyword, followed by the class name (usually CamelCase) and a colon :.\n\n"
                    "### Example Code\n"
                    "Load this example code to see how a simple class is declared with class-level attributes:\n"
                    "<example_code>\n"
                    "class Car:\n"
                    "    color = \"Red\"\n"
                    "    speed = 0\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Declare a class named `Book`.\n"
                    "2. The class should have two class-level variables: `title` set to the empty string `\"\"` and `author` set to the empty string `\"\"`."
                ),
                "starter_code": (
                    "# Exercise 16: Class Blueprints\n"
                    "# Define the Book class below\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.ClassDef) and node.name == 'Book' for node in ast.walk(tree))", "msg": "You must declare a class named 'Book'."},
                        {"code": "b = Book(); assert b.title == ''", "msg": "A new Book instance must have 'title' initialized to an empty string."},
                        {"code": "b = Book(); assert b.author == ''", "msg": "A new Book instance must have 'author' initialized to an empty string."},
                        {"code": "b = Book(); b.title = 'Test'; assert b.title == 'Test'", "msg": "Assigning title to a Book instance should work correctly."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 17: Constructors",
                "slug": "init_constructor",
                "module": 4,
                "prompt": (
                    "### Curriculum: The __init__ Constructor\n"
                    "The `__init__` method is a special method (constructor) that Python runs automatically whenever you create a new instance of a class. "
                    "You use it to initialize instance attributes (variables specific to that object).\n\n"
                    "The first parameter of any class method, including `__init__`, is always `self`. It represents the active object instance itself, "
                    "allowing you to store attributes on the object using `self.attribute_name = value`.\n\n"
                    "### Example Code\n"
                    "Load this example code to see a constructor setting a name field:\n"
                    "<example_code>\n"
                    "class Dog:\n"
                    "    def __init__(self, name):\n"
                    "        self.name = name\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Declare a class named `Student`.\n"
                    "2. Implement an `__init__(self, name, grade)` constructor that sets instance variables `self.name` and `self.grade` to the incoming parameters."
                ),
                "starter_code": (
                    "# Exercise 17: Constructors\n"
                    "# Define the Student class below with constructor\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.ClassDef) and node.name == 'Student' for node in ast.walk(tree))", "msg": "You must declare a class named 'Student'."},
                        {"code": "s = Student('Alex', 11); assert s.name == 'Alex'", "msg": "The constructor must set self.name correctly."},
                        {"code": "s = Student('Alex', 11); assert s.grade == 11", "msg": "The constructor must set self.grade correctly."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 18: Instance Methods",
                "slug": "instance_methods",
                "module": 4,
                "prompt": (
                    "### Curriculum: Class Instance Methods\n"
                    "Instance methods are functions declared inside a class that take `self` as the first parameter. "
                    "They allow objects to perform behaviors, and can read and modify the object's instance variables.\n\n"
                    "### Example Code\n"
                    "Load this example to see a Counter class mutating its internal count variable:\n"
                    "<example_code>\n"
                    "class Counter:\n"
                    "    def __init__(self):\n"
                    "        self.count = 0\n"
                    "    def increment(self):\n"
                    "        self.count += 1\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Declare a class named `BankAccount`.\n"
                    "2. Implement an `__init__(self, owner, balance)` constructor to initialize `self.owner` and `self.balance`.\n"
                    "3. Implement a method `deposit(self, amount)` that adds the incoming `amount` to `self.balance`.\n"
                    "4. Implement a method `withdraw(self, amount)` that subtracts the incoming `amount` from `self.balance`."
                ),
                "starter_code": (
                    "# Exercise 18: Instance Methods\n"
                    "# Define the BankAccount class below\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.ClassDef) and node.name == 'BankAccount' for node in ast.walk(tree))", "msg": "You must declare a class named 'BankAccount'."},
                        {"code": "a = BankAccount('Charlie', 100); assert a.owner == 'Charlie' and a.balance == 100", "msg": "Constructor should set owner and balance correctly."},
                        {"code": "a = BankAccount('Charlie', 100); a.deposit(50); assert a.balance == 150", "msg": "deposit(50) must increase balance to 150."},
                        {"code": "a = BankAccount('Charlie', 100); a.withdraw(30); assert a.balance == 70", "msg": "withdraw(30) must decrease balance to 70."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 19: Private Variables",
                "slug": "private_variables",
                "module": 4,
                "prompt": (
                    "### Curriculum: Encapsulation & Data Hiding\n"
                    "Encapsulation is the practice of hiding an object's internal details and only exposing what is safe. "
                    "In Python, prefixing an attribute name with double underscores (e.g. `self.__passcode`) triggers **name mangling**.\n\n"
                    "This makes the attribute private and prevents direct access from outside the class (e.g. attempting to read `obj.__passcode` directly will raise an AttributeError).\n\n"
                    "### Example Code\n"
                    "Load this example code to see private variables in action:\n"
                    "<example_code>\n"
                    "class User:\n"
                    "    def __init__(self, username, password):\n"
                    "        self.username = username\n"
                    "        self.__password = password  # Private attribute\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Declare a class named `SmartPhone`.\n"
                    "2. Implement `__init__(self, brand, passcode)` where `brand` is public (`self.brand`), but `passcode` is private (`self.__passcode`)."
                ),
                "starter_code": (
                    "# Exercise 19: Private Variables\n"
                    "# Define the SmartPhone class below with private passcode\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.ClassDef) and node.name == 'SmartPhone' for node in ast.walk(tree))", "msg": "You must declare a class named 'SmartPhone'."},
                        {"code": "p = SmartPhone('Apple', '1234'); assert p.brand == 'Apple'", "msg": "Brand must be a public attribute."},
                        {"code": "p = SmartPhone('Apple', '1234'); assert not hasattr(p, '__passcode')", "msg": "passcode must be private and not directly accessible as __passcode."},
                        {"code": "p = SmartPhone('Apple', '1234'); assert hasattr(p, '_SmartPhone__passcode')", "msg": "passcode must be mangled to _SmartPhone__passcode."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 20: Getters & Setters",
                "slug": "getters_setters",
                "module": 4,
                "prompt": (
                    "### Curriculum: Accessor & Mutator Methods\n"
                    "To safely interact with private attributes, we write **getters** (accessor methods) to read them and "
                    "**setters** (mutator methods) to update them. Setters are especially useful because they can run validations "
                    "before changing the value.\n\n"
                    "### Example Code\n"
                    "Load this example code showing accessors and mutators validation checks:\n"
                    "<example_code>\n"
                    "class Temperature:\n"
                    "    def __init__(self, celsius):\n"
                    "        self.__celsius = celsius\n"
                    "    def get_celsius(self):\n"
                    "        return self.__celsius\n"
                    "    def set_celsius(self, value):\n"
                    "        if value >= -273.15:\n"
                    "            self.__celsius = value\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Declare a class named `Employee`.\n"
                    "2. Implement `__init__(self, name, salary)` where `salary` is private (`self.__salary`).\n"
                    "3. Implement a getter method `get_salary(self)` that returns the private salary.\n"
                    "4. Implement a setter method `set_salary(self, amount)` that updates the private salary only if `amount` is positive. If `amount` is 0 or negative, it should make no change to the salary."
                ),
                "starter_code": (
                    "# Exercise 20: Getters & Setters\n"
                    "# Define the Employee class below\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.ClassDef) and node.name == 'Employee' for node in ast.walk(tree))", "msg": "You must declare a class named 'Employee'."},
                        {"code": "e = Employee('Blake', 50000); assert e.get_salary() == 50000", "msg": "get_salary() must return the private salary value."},
                        {"code": "e = Employee('Blake', 50000); e.set_salary(60000); assert e.get_salary() == 60000", "msg": "set_salary(60000) should increase salary successfully."},
                        {"code": "e = Employee('Blake', 50000); e.set_salary(-1000); assert e.get_salary() == 50000", "msg": "set_salary(-1000) must make no change (salary must remain 50000)."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Module 4 Assessment: Class Blueprint & Operations",
                "slug": "unit4_assessment",
                "module": 4,
                "prompt": (
                    "### Summative Assessment: Module 4\n"
                    "This task acts as a summative assessment evaluating your custom class blueprint, constructor, private variable encapsulation, "
                    "and accessor/mutator validations. No curriculum helper explanations or examples are provided for this exercise.\n\n"
                    "### Task Instructions\n"
                    "1. Declare a class named `Car`.\n"
                    "2. Implement `__init__(self, model, speed)` where `model` is public and `speed` is private (`self.__speed`).\n"
                    "3. Implement a getter method `get_speed(self)` that returns the private speed.\n"
                    "4. Implement a method `accelerate(self, increment)` that adds the incoming `increment` value to the private speed attribute.\n"
                    "5. Implement a method `brake(self, decrement)` that subtracts the incoming `decrement` value from the private speed attribute. "
                    "However, speed must never drop below 0. If the decrement would make the speed negative, set the speed to exactly 0."
                ),
                "starter_code": (
                    "# Module 4 Assessment: Class Blueprint & Operations\n"
                    "# Write your Car class implementation here\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.ClassDef) and node.name == 'Car' for node in ast.walk(tree))", "msg": "You must declare a class named 'Car'."},
                        {"code": "c = Car('Model S', 0); assert c.get_speed() == 0", "msg": "get_speed() must return correct speed."},
                        {"code": "c = Car('Model S', 0); c.accelerate(40); assert c.get_speed() == 40", "msg": "accelerate(40) should increase speed to 40."},
                        {"code": "c = Car('Model S', 50); c.brake(20); assert c.get_speed() == 30", "msg": "brake(20) should decrease speed to 30."},
                        {"code": "c = Car('Model S', 10); c.brake(30); assert c.get_speed() == 0", "msg": "brake(30) should set speed to 0 and avoid negative speed values."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 21: Simple Inheritance",
                "slug": "simple_inheritance",
                "module": 5,
                "prompt": (
                    "### Curriculum: Class Inheritance\n"
                    "Inheritance allows a new class (subclass or child class) to inherit attributes and methods "
                    "from an existing class (superclass or parent class). This promotes code reuse.\n\n"
                    "You declare a subclass by passing the parent class name in parentheses when defining the subclass: "
                    "`class ChildClass(ParentClass):`.\n\n"
                    "### Example Code\n"
                    "Load this example code to see how a Child inherits fields from a Parent class:\n"
                    "<example_code>\n"
                    "class Parent:\n"
                    "    value = 10\n"
                    "class Child(Parent):\n"
                    "    pass\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Declare a class named `Animal` with a class-level variable `species` set to the string `\"Unknown\"`.\n"
                    "2. Declare a subclass named `Dog` that inherits from `Animal`."
                ),
                "starter_code": (
                    "# Exercise 21: Simple Inheritance\n"
                    "# Define Animal and Dog classes below\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]; assert 'Animal' in classes and 'Dog' in classes", "msg": "You must declare classes named 'Animal' and 'Dog'."},
                        {"code": "assert issubclass(Dog, Animal)", "msg": "Class 'Dog' must inherit from 'Animal'."},
                        {"code": "d = Dog(); assert d.species == 'Unknown'", "msg": "Dog instance must inherit species attribute from Animal."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 22: The super() Constructor Call",
                "slug": "super_call",
                "module": 5,
                "prompt": (
                    "### Curriculum: Calling Parent Constructor\n"
                    "Inside a subclass's `__init__` constructor, you can call the parent class's constructor "
                    "using the `super()` function. This ensures that the parent class attributes are correctly initialized.\n\n"
                    "Syntax: `super().__init__(arguments)`\n\n"
                    "### Example Code\n"
                    "Load this example code to see a subclass calling its parent constructor:\n"
                    "<example_code>\n"
                    "class Parent:\n"
                    "    def __init__(self, name):\n"
                    "        self.name = name\n"
                    "class Child(Parent):\n"
                    "    def __init__(self, name, age):\n"
                    "        super().__init__(name)\n"
                    "        self.age = age\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "You are given a base class `Person`:\n"
                    "```python\n"
                    "class Person:\n"
                    "    def __init__(self, name):\n"
                    "        self.name = name\n"
                    "```\n"
                    "1. Declare a subclass `Teacher` that inherits from `Person`.\n"
                    "2. Implement `__init__(self, name, subject)` in `Teacher`. Use `super()` to initialize `name` in the parent constructor, and set `self.subject` in the subclass."
                ),
                "starter_code": (
                    "# Exercise 22: The super() Constructor Call\n"
                    "class Person:\n"
                    "    def __init__(self, name):\n"
                    "        self.name = name\n\n"
                    "# Define the Teacher class below inheriting from Person\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.ClassDef) and node.name == 'Teacher' for node in ast.walk(tree))", "msg": "You must declare a class named 'Teacher'."},
                        {"code": "assert issubclass(Teacher, Person)", "msg": "Teacher must inherit from Person."},
                        {"code": "t = Teacher('Smith', 'Science'); assert t.name == 'Smith'", "msg": "t.name must be set correctly via the super() constructor call."},
                        {"code": "t = Teacher('Smith', 'Science'); assert t.subject == 'Science'", "msg": "t.subject must be set correctly inside Teacher."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 23: Method Overriding",
                "slug": "method_override",
                "module": 5,
                "prompt": (
                    "### Curriculum: Overriding Parent Methods\n"
                    "Method overriding occurs when a subclass defines a method with the same name and signature as a method in the parent class. "
                    "When called, the subclass's version of the method overrides (replaces) the parent's version.\n\n"
                    "### Example Code\n"
                    "Load this example code to see overriding in action:\n"
                    "<example_code>\n"
                    "class Bird:\n"
                    "    def fly(self):\n"
                    "        return \"Flaps wings\"\n"
                    "class Penguin(Bird):\n"
                    "    def fly(self):\n"
                    "        return \"Cannot fly, swims instead\"\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Declare a base class `Vehicle` with a method `make_sound(self)` that returns the string `\"Vroom\"`.\n"
                    "2. Declare a subclass `Bicycle` that inherits from `Vehicle` and overrides `make_sound(self)` to return the string `\"Ring Ring\"`.\n"
                    "3. Declare a subclass `Car` that inherits from `Vehicle` and overrides `make_sound(self)` to return the string `\"Honk Honk\"`."
                ),
                "starter_code": (
                    "# Exercise 23: Method Overriding\n"
                    "# Define Vehicle, Bicycle, and Car classes below\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "assert issubclass(Bicycle, Vehicle)", "msg": "Bicycle must inherit from Vehicle."},
                        {"code": "assert issubclass(Car, Vehicle)", "msg": "Car must inherit from Vehicle."},
                        {"code": "v = Vehicle(); assert v.make_sound() == 'Vroom'", "msg": "Vehicle.make_sound() must return 'Vroom'."},
                        {"code": "b = Bicycle(); assert b.make_sound() == 'Ring Ring'", "msg": "Bicycle.make_sound() must return 'Ring Ring'."},
                        {"code": "c = Car(); assert c.make_sound() == 'Honk Honk'", "msg": "Car.make_sound() must return 'Honk Honk'."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 24: Polymorphic Collections",
                "slug": "polymorphic_list",
                "module": 5,
                "prompt": (
                    "### Curriculum: Polymorphism\n"
                    "Polymorphism allows objects of different classes to be treated as objects of a common superclass. "
                    "When you iterate through a list of mixed objects and invoke a shared method name, Python dynamically executes "
                    "the specific overridden method corresponding to each object's actual class.\n\n"
                    "### Example Code\n"
                    "Load this example code to see polymorphic execution:\n"
                    "<example_code>\n"
                    "class Dog:\n"
                    "    def speak(self): return \"Woof\"\n"
                    "class Cat:\n"
                    "    def speak(self): return \"Meow\"\n\n"
                    "animals = [Dog(), Cat()]\n"
                    "for a in animals:\n"
                    "    print(a.speak())  # woof, then meow\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. You are given classes `Vehicle`, `Bicycle`, and `Car` in the environment.\n"
                    "2. Implement a function `make_noises(vehicle_list)` that takes a list of vehicle objects, calls `make_sound()` on each object, collects their string return values into a list, and returns that list."
                ),
                "starter_code": (
                    "# Exercise 24: Polymorphic Collections\n"
                    "class Vehicle:\n"
                    "    def make_sound(self): return 'Vroom'\n"
                    "class Bicycle(Vehicle):\n"
                    "    def make_sound(self): return 'Ring Ring'\n"
                    "class Car(Vehicle):\n"
                    "    def make_sound(self): return 'Honk Honk'\n\n"
                    "def make_noises(vehicle_list):\n"
                    "    # Write your function here to return list of sounds\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'make_noises' for node in ast.walk(tree))", "msg": "You must define a function named 'make_noises'."},
                        {"code": "vehicles = [Vehicle(), Bicycle(), Car(), Bicycle()]; assert make_noises(vehicles) == ['Vroom', 'Ring Ring', 'Honk Honk', 'Ring Ring']", "msg": "make_noises() must collect and return the correct sounds list polymorphically."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Exercise 25: isinstance() Type Verification",
                "slug": "isinstance_checks",
                "module": 5,
                "prompt": (
                    "### Curriculum: Checking Inheritance Class Types\n"
                    "The built-in function `isinstance(object, classinfo)` checks if an object is an instance of a specified class, "
                    "or an instance of a subclass of that class. It returns `True` or `False`.\n\n"
                    "### Example Code\n"
                    "Load this example code showing isinstance checks:\n"
                    "<example_code>\n"
                    "class Parent: pass\n"
                    "class Child(Parent): pass\n\n"
                    "c = Child()\n"
                    "print(isinstance(c, Child))   # True\n"
                    "print(isinstance(c, Parent))  # True\n"
                    "print(isinstance(c, str))     # False\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. You are given classes `Animal`, `Dog(Animal)`, and `Cat(Animal)`.\n"
                    "2. Write a function `count_dogs(animal_list)` that takes a list of animal objects, counts how many of those objects are instances of `Dog` (or any subclass inheriting from `Dog`) using `isinstance`, and returns that integer count."
                ),
                "starter_code": (
                    "# Exercise 25: isinstance() Type Verification\n"
                    "class Animal: pass\n"
                    "class Dog(Animal): pass\n"
                    "class Cat(Animal): pass\n\n"
                    "def count_dogs(animal_list):\n"
                    "    # Write your count_dogs function here using isinstance\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); func = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == 'count_dogs'][0]; assert any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id == 'isinstance' for c in ast.walk(func))", "msg": "You must use the isinstance() function inside count_dogs."},
                        {"code": "animals = [Dog(), Cat(), Dog(), Animal(), Cat()]; assert count_dogs(animals) == 2", "msg": "count_dogs() must return the count of Dog instances."}
                    ],
                    "io_tests": []
                }
            },
{
                "title": "Module 5 Assessment: Subclasses & Polymorphism",
                "slug": "unit5_assessment",
                "module": 5,
                "prompt": (
                    "### Summative Assessment: Module 5\n"
                    "This task acts as a summative assessment evaluating your subclass declarations, constructor overrides with `super()`, method overriding, "
                    "and traversing polymorphic collections. No curriculum helper explanations or examples are provided for this exercise.\n\n"
                    "### Task Instructions\n"
                    "1. Declare a base class named `Shape` with a method `area(self)` that returns `0.0`.\n"
                    "2. Declare a subclass named `Rectangle` that inherits from `Shape`. Implement `__init__(self, width, height)` and override `area(self)` to return `width * height`.\n"
                    "3. Declare a subclass named `Circle` that inherits from `Shape`. Implement `__init__(self, radius)` and override `area(self)` to return exactly `3.14 * radius * radius`.\n"
                    "4. Write a function `total_area(shapes_list)` that calculates and returns the sum of the areas of all shape objects in the incoming list."
                ),
                "starter_code": (
                    "# Module 5 Assessment: Subclasses & Polymorphism\n"
                    "# Write your Shape, Rectangle, Circle, and total_area implementations here\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "assert issubclass(Rectangle, Shape)", "msg": "Rectangle must inherit from Shape."},
                        {"code": "assert issubclass(Circle, Shape)", "msg": "Circle must inherit from Shape."},
                        {"code": "r = Rectangle(4, 5); assert r.area() == 20.0", "msg": "Rectangle(4, 5).area() should return 20.0."},
                        {"code": "c = Circle(10); assert c.area() == 314.0", "msg": "Circle(10).area() should return 314.0."},
                        {"code": "shapes = [Rectangle(3, 4), Circle(5), Rectangle(2, 5)]; assert abs(total_area(shapes) - 100.5) < 0.01", "msg": "total_area() must sum up the areas polymorphically (12 + 78.5 + 10 = 100.5)."}
                    ],
                    "io_tests": []
                }
            }
,
            # ==========================================
            # MODULE 6: 1D LISTS & DATA TRAVERSAL
            # ==========================================
            {
                "title": "Exercise 26: List Mutators",
                "slug": "list_mutators",
                "module": 6,
                "prompt": (
                    "### Curriculum: Python List Mutators\n"
                    "Lists in Python are mutable, meaning their elements can be changed, added, or removed after creation. "
                    "Some key methods for mutating lists include:\n"
                    "*   `list.append(item)`: Adds an item to the end of the list.\n"
                    "*   `list.insert(index, item)`: Inserts an item at a specific index.\n"
                    "*   `list.sort()`: Sorts the elements of the list in-place (ascending order by default).\n"
                    "*   `list.pop(index)`: Removes and returns the item at the specified index (defaults to the last item).\n\n"
                    "### Example Code\n"
                    "Load this example code to see list mutations in action:\n"
                    "<example_code>\n"
                    "colors = [\"blue\", \"green\"]\n"
                    "colors.append(\"red\")\n"
                    "colors.insert(0, \"yellow\")\n"
                    "colors.sort()\n"
                    "print(colors)\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `modify_list(lst)` that mutates the incoming list `lst` as follows:\n"
                    "   - Appends the integer `10` to the end of the list.\n"
                    "   - Inserts the integer `0` at index `0`.\n"
                    "   - Sorts the list in ascending order.\n"
                    "   - Returns the modified list."
                ),
                "starter_code": (
                    "# Exercise 26: List Mutators\n"
                    "def modify_list(lst):\n"
                    "    # Write your list mutation code here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'modify_list' for node in ast.walk(tree))", "msg": "You must define a function named 'modify_list'."},
                        {"code": "assert modify_list([5, 3]) == [0, 3, 5, 10]", "msg": "modify_list([5, 3]) should return [0, 3, 5, 10]."},
                        {"code": "assert modify_list([1]) == [0, 1, 10]", "msg": "modify_list([1]) should return [0, 1, 10]."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Exercise 27: List Slicing",
                "slug": "list_slice",
                "module": 6,
                "prompt": (
                    "### Curriculum: Python List Slicing\n"
                    "List slicing allows you to extract sub-sequences from a list using the colon `:` syntax.\n"
                    "Syntax: `list[start:end:step]`\n"
                    "*   `start`: Index where the slice begins (inclusive, defaults to 0).\n"
                    "*   `end`: Index where the slice ends (exclusive, defaults to end of list).\n"
                    "*   `step`: The index increment (defaults to 1).\n\n"
                    "### Example Code\n"
                    "Load this example code to see slicing in action:\n"
                    "<example_code>\n"
                    "nums = [10, 20, 30, 40, 50]\n"
                    "print(nums[0:3])   # [10, 20, 30] (indices 0 to 2)\n"
                    "print(nums[-2:])   # [40, 50] (last two elements)\n"
                    "print(nums[::2])   # [10, 30, 50] (every second element)\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `get_slices(lst)` that returns a tuple containing exactly three sub-slices of `lst`:\n"
                    "   - The first slice must contain the first 3 elements of `lst`.\n"
                    "   - The second slice must contain the last 2 elements of `lst`.\n"
                    "   - The third slice must contain every second element of `lst` (step of 2), starting from index 0."
                ),
                "starter_code": (
                    "# Exercise 27: List Slicing\n"
                    "def get_slices(lst):\n"
                    "    # Return a tuple of (first_3, last_2, every_second)\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'get_slices' for node in ast.walk(tree))", "msg": "You must define a function named 'get_slices'."},
                        {"code": "assert get_slices([10, 20, 30, 40, 50, 60]) == ([10, 20, 30], [50, 60], [10, 30, 50])", "msg": "get_slices() returned incorrect slices for [10, 20, 30, 40, 50, 60]."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Exercise 28: Traversing Lists",
                "slug": "list_traversal",
                "module": 6,
                "prompt": (
                    "### Curriculum: List Traversals\n"
                    "Traversing a list means visiting each element in sequence using loops. You can traverse a list by element value "
                    "or by index indices:\n"
                    "*   By Value: `for item in lst:`\n"
                    "*   By Index: `for i in range(len(lst)):`\n\n"
                    "### Example Code\n"
                    "Load this example code showing traversal to calculate list average:\n"
                    "<example_code>\n"
                    "nums = [4, 6, 8]\n"
                    "total = 0\n"
                    "for x in nums:\n"
                    "    total += x\n"
                    "avg = total / len(nums)\n"
                    "print(avg)  # 6.0\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `find_stats(numbers)` that returns a tuple containing: `(total_sum, min_value)`.\n"
                    "   - `total_sum`: The sum of all numbers in the list.\n"
                    "   - `min_value`: The minimum number in the list.\n"
                    "2. You MUST use a loop to traverse the list. You MUST NOT use Python's built-in `sum()` or `min()` functions."
                ),
                "starter_code": (
                    "# Exercise 28: Traversing Lists\n"
                    "def find_stats(numbers):\n"
                    "    # Write your loop traversal here. Do NOT use sum() or min()\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); func = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == 'find_stats'][0]; assert not any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id in ('sum', 'min') for c in ast.walk(func))", "msg": "You must calculate sum and min manually using loops. Do not call sum() or min()."},
                        {"code": "import ast; tree = ast.parse(__student_code__); func = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == 'find_stats'][0]; assert any(isinstance(c, (ast.For, ast.While)) for c in ast.walk(func))", "msg": "You must use a loop to traverse the list."},
                        {"code": "assert find_stats([10, 2, 8, 5]) == (25, 2)", "msg": "find_stats([10, 2, 8, 5]) should return (25, 2)."},
                        {"code": "assert find_stats([-3, 0, 4]) == (1, -3)", "msg": "find_stats([-3, 0, 4]) should return (1, -3)."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Exercise 29: List Comprehensions",
                "slug": "list_comprehension",
                "module": 6,
                "prompt": (
                    "### Curriculum: Python List Comprehensions\n"
                    "List comprehensions provide a concise way to create lists from existing sequences.\n"
                    "Syntax: `[expression for item in list if condition]`\n\n"
                    "### Example Code\n"
                    "Load this example code to generate squares of odd numbers:\n"
                    "<example_code>\n"
                    "nums = [1, 2, 3, 4]\n"
                    "odd_squares = [x**2 for x in nums if x % 2 != 0]\n"
                    "print(odd_squares)  # [1, 9]\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `get_even_squares(numbers)` that returns a list containing the squared value of all **even** numbers in the input list.\n"
                    "2. You MUST use a **list comprehension** to generate the result."
                ),
                "starter_code": (
                    "# Exercise 29: List Comprehensions\n"
                    "def get_even_squares(numbers):\n"
                    "    # Write your list comprehension here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); func = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == 'get_even_squares'][0]; assert any(isinstance(c, ast.ListComp) for c in ast.walk(func))", "msg": "You must use a list comprehension structure in your function."},
                        {"code": "assert get_even_squares([1, 2, 3, 4]) == [4, 16]", "msg": "get_even_squares([1, 2, 3, 4]) should return [4, 16]."},
                        {"code": "assert get_even_squares([5, 7]) == []", "msg": "get_even_squares([5, 7]) should return []."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Exercise 30: List Reversing",
                "slug": "list_reversing",
                "module": 6,
                "prompt": (
                    "### Curriculum: Reversing Lists In-Place\n"
                    "Reversing a list means reversing the order of its elements. If you modify the original list directly "
                    "rather than creating a copy, it is called an **in-place** operation.\n"
                    "In Python, you can reverse a list in-place using the `list.reverse()` method.\n\n"
                    "### Example Code\n"
                    "Load this example code to see in-place reversal:\n"
                    "<example_code>\n"
                    "fruits = [\"apple\", \"banana\"]\n"
                    "fruits.reverse()\n"
                    "print(fruits)  # [\'banana\', \'apple\']\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `reverse_in_place(lst)` that reverses the order of elements in `lst` **in-place** (modifying the original list) and returns the list."
                ),
                "starter_code": (
                    "# Exercise 30: List Reversing\n"
                    "def reverse_in_place(lst):\n"
                    "    # Reverse lst in-place and return it\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'reverse_in_place' for node in ast.walk(tree))", "msg": "You must define a function named 'reverse_in_place'."},
                        {"code": "x = [1, 2, 3]; y = reverse_in_place(x); assert y is x and y == [3, 2, 1]", "msg": "reverse_in_place must modify the list in-place and return the same list object."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Module 6 Assessment: List Operations & Processing",
                "slug": "unit6_assessment",
                "module": 6,
                "prompt": (
                    "### Summative Assessment: Module 6\n"
                    "This task acts as a summative assessment evaluating your list slicing, loops traversals, list mutator methods, "
                    "and list comprehensions. No curriculum helper explanations or examples are provided for this exercise.\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `process_dataset(data)` that performing the following sequence of operations:\n"
                    "   - Discards the first and last elements of `data` using list slicing.\n"
                    "   - Calculates the sum of all remaining **positive** numbers (numbers > 0) in the sliced list using a loop.\n"
                    "   - Returns a list containing: the squared value of that sum as the first element, followed by all the elements in the sliced list in reverse order."
                ),
                "starter_code": (
                    "# Module 6 Assessment: List Operations & Processing\n"
                    "def process_dataset(data):\n"
                    "    # Write your implementation here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'process_dataset' for node in ast.walk(tree))", "msg": "You must define a function named 'process_dataset'."},
                        {"code": "assert process_dataset([10, 2, -3, 4, 20]) == [36, 4, -3, 2]", "msg": "process_dataset([10, 2, -3, 4, 20]) should return [36, 4, -3, 2]. (Sum of 2 and 4 is 6, squared is 36. Sliced elements reversed is [4, -3, 2])."},
                        {"code": "assert process_dataset([1, -2, -3, 4]) == [0, -3, -2]", "msg": "process_dataset([1, -2, -3, 4]) should return [0, -3, -2]."}
                    ],
                    "io_tests": []
                }
            }
,
            # ==========================================
            # MODULE 7: 2D LISTS & MATRIX GRIDS
            # ==========================================
            {
                "title": "Exercise 31: 2D Grid Creation",
                "slug": "grid_creation",
                "module": 7,
                "prompt": (
                    "### Curriculum: Representing 2D Lists in Python\n"
                    "A 2D list (or matrix) in Python is represented as a list containing other lists. "
                    "For example, a grid with 2 rows and 3 columns can be defined as:\n"
                    "`grid = [[1, 2, 3], [4, 5, 6]]`\n\n"
                    "**Crucial Warning:** When initializing a grid dynamically, never use multiplication on lists of lists like "
                    "`[[0] * cols] * rows`. This creates rows that reference the *exact same list object* in memory. Modifying an element "
                    "in one row will modify it in all rows! Instead, always use list comprehensions or nested loops:\n"
                    "`grid = [[0 for _ in range(cols)] for _ in range(rows)]`\n\n"
                    "### Example Code\n"
                    "Load this example code to see grid reference issues:\n"
                    "<example_code>\n"
                    "# Safe Grid creation\n"
                    "rows, cols = 3, 3\n"
                    "grid = [[0 for _ in range(cols)] for _ in range(rows)]\n"
                    "grid[0][0] = 99\n"
                    "print(grid)  # Only row 0 column 0 changes\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `create_grid(rows, cols, fill_value)` that returns a new 2D list of the specified dimensions filled with `fill_value`.\n"
                    "2. You MUST construct the list such that row references are independent (modifying `grid[0][0]` must NOT modify `grid[1][0]`)."
                ),
                "starter_code": (
                    "# Exercise 31: 2D Grid Creation\n"
                    "def create_grid(rows, cols, fill_value):\n"
                    "    # Create and return a rows x cols grid filled with fill_value\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'create_grid' for node in ast.walk(tree))", "msg": "You must define a function named 'create_grid'."},
                        {"code": "assert create_grid(3, 4, 0) == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]", "msg": "create_grid(3, 4, 0) returned incorrect board layout."},
                        {"code": "g = create_grid(2, 2, 0); g[0][0] = 5; assert g[1][0] == 0", "msg": "Grid rows must not share reference. Ensure you are not multiplying list rows."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Exercise 32: Row Sums",
                "slug": "row_sum",
                "module": 7,
                "prompt": (
                    "### Curriculum: Row-Major 2D List Traversals\n"
                    "To traverse a 2D list row by row (row-major order), you can iterate through the outer list, where each element is an "
                    "entire row (a 1D list). You can then calculate statistics or process elements row by row.\n\n"
                    "### Example Code\n"
                    "Load this example code to see row traversals:\n"
                    "<example_code>\n"
                    "matrix = [[1, 2], [3, 4]]\n"
                    "for row in matrix:\n"
                    "    print(sum(row))  # Prints 3, then 7\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `get_row_sums(matrix)` that accepts a 2D list `matrix` of numbers and returns a **list** containing the sum of all elements in each row."
                ),
                "starter_code": (
                    "# Exercise 32: Row Sums\n"
                    "def get_row_sums(matrix):\n"
                    "    # Return list of row sums\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'get_row_sums' for node in ast.walk(tree))", "msg": "You must define a function named 'get_row_sums'."},
                        {"code": "assert get_row_sums([[1, 2], [3, 4], [5, 6]]) == [3, 7, 11]", "msg": "get_row_sums([[1, 2], [3, 4], [5, 6]]) should return [3, 7, 11]."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Exercise 33: Column Sums",
                "slug": "column_sum",
                "module": 7,
                "prompt": (
                    "### Curriculum: Column-Major 2D List Traversals\n"
                    "To traverse a 2D list column by column (column-major order), you iterate index-by-index through the length of the rows. "
                    "For a grid with `cols` columns, the column index `col` goes from `0` to `cols - 1`, and the row index `row` goes from `0` to `rows - 1`. "
                    "We access element coordinates via `grid[row][col]`.\n\n"
                    "### Example Code\n"
                    "Load this example code to calculate column sums:\n"
                    "<example_code>\n"
                    "matrix = [[1, 2], [3, 4]]\n"
                    "num_rows = len(matrix)\n"
                    "num_cols = len(matrix[0])\n"
                    "col_sums = []\n"
                    "for col in range(num_cols):\n"
                    "    total = 0\n"
                    "    for row in range(num_rows):\n"
                    "        total += matrix[row][col]\n"
                    "    col_sums.append(total)\n"
                    "print(col_sums)  # [4, 6]\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `get_col_sums(matrix)` that accepts a 2D list `matrix` and returns a **list** containing the sum of each column. "
                    "Assume all rows are of equal length."
                ),
                "starter_code": (
                    "# Exercise 33: Column Sums\n"
                    "def get_col_sums(matrix):\n"
                    "    # Return list of column sums\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'get_col_sums' for node in ast.walk(tree))", "msg": "You must define a function named 'get_col_sums'."},
                        {"code": "assert get_col_sums([[1, 2], [3, 4], [5, 6]]) == [9, 12]", "msg": "get_col_sums([[1, 2], [3, 4], [5, 6]]) should return [9, 12]."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Exercise 34: Matrix Diagonals",
                "slug": "diagonal_check",
                "module": 7,
                "prompt": (
                    "### Curriculum: Square Matrix Diagonals\n"
                    "A square matrix has two primary diagonals:\n"
                    "1.  **Main Diagonal**: Extends from the top-left to the bottom-right corner. The row index equals the column index (`matrix[i][i]`).\n"
                    "2.  **Secondary Diagonal**: Extends from the top-right to the bottom-left corner. For matrix size `N`, the element coordinate is `matrix[i][N - 1 - i]`.\n\n"
                    "### Example Code\n"
                    "Load this example code to see diagonal indexing:\n"
                    "<example_code>\n"
                    "matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\n"
                    "n = len(matrix)\n"
                    "main = [matrix[i][i] for i in range(n)]\n"
                    "sec = [matrix[i][n - 1 - i] for i in range(n)]\n"
                    "print(main, sec)  # [1, 5, 9] [3, 5, 7]\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `get_diagonals(matrix)` that accepts a square 2D list `matrix` and returns a **tuple** containing two lists: `(main_diagonal, secondary_diagonal)`."
                ),
                "starter_code": (
                    "# Exercise 34: Matrix Diagonals\n"
                    "def get_diagonals(matrix):\n"
                    "    # Return tuple of lists: (main_diagonal, secondary_diagonal)\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'get_diagonals' for node in ast.walk(tree))", "msg": "You must define a function named 'get_diagonals'."},
                        {"code": "assert get_diagonals([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == ([1, 5, 9], [3, 5, 7])", "msg": "get_diagonals() returned incorrect diagonals."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Exercise 35: Grid Boundary Check",
                "slug": "boundary_search",
                "module": 7,
                "prompt": (
                    "### Curriculum: Grid Boundary Checking\n"
                    "When traversing grids in applications (such as game boards or mazes), you must check that coordinates "
                    "`(row, col)` do not fall outside the boundaries of the grid. "
                    "For a grid with `M` rows and `N` columns, the coordinate is valid if and only if:\n"
                    "`0 <= row < M` and `0 <= col < N`\n\n"
                    "### Example Code\n"
                    "Load this example code demonstrating boundary validation:\n"
                    "<example_code>\n"
                    "grid = [[1, 2], [3, 4], [5, 6]]\n"
                    "rows = len(grid)\n"
                    "cols = len(grid[0])\n"
                    "r, c = 3, 1\n"
                    "is_valid = (0 <= r < rows) and (0 <= c < cols)\n"
                    "print(is_valid)  # False (row index 3 is out of bounds)\n"
                    "</example_code>\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `is_in_bounds(row, col, rows, cols)` that returns `True` if `(row, col)` resides within the bounds of a grid with dimensions `rows` by `cols`, and `False` otherwise."
                ),
                "starter_code": (
                    "# Exercise 35: Grid Boundary Check\n"
                    "def is_in_bounds(row, col, rows, cols):\n"
                    "    # Return True if in grid bounds, False otherwise\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'is_in_bounds' for node in ast.walk(tree))", "msg": "You must define a function named 'is_in_bounds'."},
                        {"code": "assert is_in_bounds(0, 0, 3, 3) is True", "msg": "is_in_bounds(0, 0, 3, 3) should be True."},
                        {"code": "assert is_in_bounds(3, 2, 3, 3) is False", "msg": "is_in_bounds(3, 2, 3, 3) should be False."},
                        {"code": "assert is_in_bounds(-1, 2, 3, 3) is False", "msg": "is_in_bounds(-1, 2, 3, 3) should be False."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Module 7 Assessment: Matrix Analysis",
                "slug": "unit7_assessment",
                "module": 7,
                "prompt": (
                    "### Summative Assessment: Module 7\n"
                    "This task acts as a summative assessment evaluating your multi-dimensional array creation, coordinate accesses, "
                    "diagonal extractions, loops traversals, and boundary validations. No curriculum helper explanations or examples are provided for this exercise.\n\n"
                    "### Task Instructions\n"
                    "1. Write a function `analyze_matrix(matrix)` that accepts a 2D list `matrix` of numbers.\n"
                    "2. The function must verify if the matrix is **square** (number of rows equals the number of columns of row 0). If the matrix is NOT square (or has 0 rows), return `None`.\n"
                    "3. If the matrix IS square, calculate and return a **dictionary** containing:\n"
                    "   - `\"diagonal_sum\"`: The sum of elements along the main diagonal (`matrix[i][i]`).\n"
                    "   - `\"boundary_sum\"`: The sum of all elements along the outer border of the matrix. "
                    "Be careful not to double-count corner elements!"
                ),
                "starter_code": (
                    "# Module 7 Assessment: Matrix Analysis\n"
                    "def analyze_matrix(matrix):\n"
                    "    # Write your implementation here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'analyze_matrix' for node in ast.walk(tree))", "msg": "You must define a function named 'analyze_matrix'."},
                        {"code": "assert analyze_matrix([[1, 2], [3, 4], [5, 6]]) is None", "msg": "analyze_matrix should return None for non-square matrix."},
                        {"code": "assert analyze_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == {'diagonal_sum': 15, 'boundary_sum': 40}", "msg": "analyze_matrix returned incorrect sum values. (Main diagonal sum: 1+5+9=15. Outer border sum: 1+2+3+4+6+7+8+9=40)."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Module 8: Binary Search",
                "slug": "binary_search",
                "module": 8,
                "prompt": (
                    "### Lesson: Binary Search\n"
                    "Binary search is an efficient algorithm for finding an item from a sorted list of items. "
                    "It works by repeatedly dividing in half the portion of the list that could contain the item, "
                    "until you've narrowed down the possible locations to just one.\n\n"
                    "### Task Instructions\n"
                    "Write a function `binary_search(arr, target)` that accepts a **sorted** list of numbers `arr` "
                    "and a target number `target`. Implement the binary search algorithm to search for `target` "
                    "in `arr`. Return the 0-based index of the target if it exists, or `-1` if it is not in the list.\n\n"
                    "Do NOT use Python's built-in `list.index()` or `bisect` library."
                ),
                "starter_code": (
                    "# Module 8: Binary Search\n"
                    "def binary_search(arr, target):\n"
                    "    # Write your implementation here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert not any(isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom) for node in ast.walk(tree))", "msg": "You should implement binary search manually without imports."},
                        {"code": "assert binary_search([1, 3, 5, 7, 9], 5) == 2", "msg": "binary_search([1, 3, 5, 7, 9], 5) should return index 2."},
                        {"code": "assert binary_search([1, 3, 5, 7, 9], 2) == -1", "msg": "binary_search([1, 3, 5, 7, 9], 2) should return -1."},
                        {"code": "assert binary_search([1, 3, 5, 7, 9], 9) == 4", "msg": "binary_search([1, 3, 5, 7, 9], 9) should return index 4."},
                        {"code": "assert binary_search([], 3) == -1", "msg": "binary_search([], 3) on empty list should return -1."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Module 8: Selection Sort",
                "slug": "selection_sort",
                "module": 8,
                "prompt": (
                    "### Lesson: Selection Sort\n"
                    "Selection sort sorts an array by repeatedly finding the minimum element (considering ascending order) "
                    "from the unsorted part and putting it at the beginning.\n\n"
                    "### Task Instructions\n"
                    "Write a function `selection_sort(arr)` that takes an unsorted list `arr` and sorts it in-place using "
                    "the Selection Sort algorithm. The function must return the sorted list.\n\n"
                    "Do NOT use Python's built-in `.sort()` or `sorted()` functions."
                ),
                "starter_code": (
                    "# Module 8: Selection Sort\n"
                    "def selection_sort(arr):\n"
                    "    # Write your implementation here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert 'sort' not in __student_code__", "msg": "You must implement the sorting algorithm manually without using built-in sort functions."},
                        {"code": "assert selection_sort([3, 1, 4, 1, 5, 9, 2]) == [1, 1, 2, 3, 4, 5, 9]", "msg": "selection_sort([3, 1, 4, 1, 5, 9, 2]) did not return sorted list."},
                        {"code": "assert selection_sort([]) == []", "msg": "selection_sort([]) should return an empty list."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Module 8: Insertion Sort",
                "slug": "insertion_sort",
                "module": 8,
                "prompt": (
                    "### Lesson: Insertion Sort\n"
                    "Insertion sort works similarly to the way you sort playing cards in your hands. "
                    "The array is virtually split into a sorted and an unsorted part. Values from the unsorted part "
                    "are picked and placed at the correct position in the sorted part.\n\n"
                    "### Task Instructions\n"
                    "Write a function `insertion_sort(arr)` that takes an unsorted list `arr` and sorts it in-place "
                    "using the Insertion Sort algorithm. Return the sorted list.\n\n"
                    "Do NOT use Python's built-in `.sort()` or `sorted()` functions."
                ),
                "starter_code": (
                    "# Module 8: Insertion Sort\n"
                    "def insertion_sort(arr):\n"
                    "    # Write your implementation here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert 'sort' not in __student_code__", "msg": "You must implement the sorting algorithm manually without using built-in sort functions."},
                        {"code": "assert insertion_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]", "msg": "insertion_sort([5, 2, 9, 1, 5, 6]) did not return sorted list."},
                        {"code": "assert insertion_sort([10]) == [10]", "msg": "insertion_sort([10]) should return [10]."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Module 8: Recursive Factorial",
                "slug": "recursive_factorial",
                "module": 8,
                "prompt": (
                    "### Lesson: Recursion & Factorials\n"
                    "A recursive function is a function that calls itself. Every recursive function must have "
                    "a **base case** to stop the recursion, and a **recursive step** that moves closer to the base case.\n\n"
                    "### Task Instructions\n"
                    "Write a recursive function `recursive_factorial(n)` that returns the factorial of a non-negative integer `n`.\n"
                    "- Base case: if `n <= 1`, return `1`.\n"
                    "- Recursive step: return `n * recursive_factorial(n - 1)`.\n\n"
                    "You must NOT use loops or external math libraries."
                ),
                "starter_code": (
                    "# Module 8: Recursive Factorial\n"
                    "def recursive_factorial(n):\n"
                    "    # Write your implementation here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.Call) and getattr(node.func, 'id', None) == 'recursive_factorial' for node in ast.walk(tree))", "msg": "Your function must call itself recursively."},
                        {"code": "assert recursive_factorial(5) == 120", "msg": "recursive_factorial(5) should return 120."},
                        {"code": "assert recursive_factorial(0) == 1", "msg": "recursive_factorial(0) should return 1."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Module 8: Recursive Fibonacci",
                "slug": "recursive_fibonacci",
                "module": 8,
                "prompt": (
                    "### Lesson: Recursive Fibonacci\n"
                    "The Fibonacci sequence is defined such that each number is the sum of the two preceding ones, "
                    "starting from 0 and 1.\n\n"
                    "### Task Instructions\n"
                    "Write a recursive function `recursive_fibonacci(n)` that returns the n-th Fibonacci number.\n"
                    "- Base cases:\n"
                    "  - if `n == 0`, return `0`.\n"
                    "  - if `n == 1`, return `1`.\n"
                    "- Recursive step: return `recursive_fibonacci(n - 1) + recursive_fibonacci(n - 2)`."
                ),
                "starter_code": (
                    "# Module 8: Recursive Fibonacci\n"
                    "def recursive_fibonacci(n):\n"
                    "    # Write your implementation here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.Call) and getattr(node.func, 'id', None) == 'recursive_fibonacci' for node in ast.walk(tree))", "msg": "Your function must call itself recursively."},
                        {"code": "assert recursive_fibonacci(0) == 0", "msg": "recursive_fibonacci(0) should return 0."},
                        {"code": "assert recursive_fibonacci(1) == 1", "msg": "recursive_fibonacci(1) should return 1."},
                        {"code": "assert recursive_fibonacci(6) == 8", "msg": "recursive_fibonacci(6) should return 8."}
                    ],
                    "io_tests": []
                }
            },
            {
                "title": "Module 8 Assessment: Recursive Sorting & Search",
                "slug": "unit8_assessment",
                "module": 8,
                "prompt": (
                    "### Summative Assessment: Module 8\n"
                    "This task acts as a summative assessment evaluating your knowledge of sorting, binary search, and recursive base-cases. No curriculum helper explanations or examples are provided for this exercise.\n\n"
                    "### Task Instructions\n"
                    "Write a function `search_and_sort_stats(arr)` that accepts a list of unsorted numbers `arr`:\n"
                    "1. First, check if the list has fewer than 2 elements. If so, return a dictionary: `{\"sorted_list\": arr, \"median\": arr[0] if arr else None, \"target_index\": -1}`.\n"
                    "2. Implement an in-place sorting algorithm (either selection or insertion sort) to sort `arr` in ascending order.\n"
                    "3. Calculate the median of the sorted list. If the list length is odd, the median is the middle element. If even, the median is the average of the two middle elements.\n"
                    "4. Implement a binary search to find the index of the median value in the sorted list. If the median value is not in the list, return `-1` for `target_index`.\n"
                    "5. Return a dictionary with: `\"sorted_list\"`, `\"median\"`, and `\"target_index\"`."
                ),
                "starter_code": (
                    "# Module 8 Assessment: Recursive Sorting & Search\n"
                    "def search_and_sort_stats(arr):\n"
                    "    # Write your implementation here\n"
                    "    pass\n"
                ),
                "test_suite": {
                    "assertions": [
                        {"code": "import ast; tree = ast.parse(__student_code__); assert any(isinstance(node, ast.FunctionDef) and node.name == 'search_and_sort_stats' for node in ast.walk(tree))", "msg": "You must define a function named 'search_and_sort_stats'."},
                        {"code": "assert search_and_sort_stats([]) == {'sorted_list': [], 'median': None, 'target_index': -1}", "msg": "Incorrect return for empty list."},
                        {"code": "assert search_and_sort_stats([3, 1, 2]) == {'sorted_list': [1, 2, 3], 'median': 2, 'target_index': 1}", "msg": "Incorrect return for odd length list."},
                        {"code": "assert search_and_sort_stats([4, 1, 3, 2]) == {'sorted_list': [1, 2, 3, 4], 'median': 2.5, 'target_index': -1}", "msg": "Incorrect return for even length list where median is average and not in list."}
                    ],
                    "io_tests": []
                }
            }
        ]

        self.stdout.write("Seeding Python Assignments...")
        for data in assignments_data:
            assignment, created = PythonAssignment.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "prompt": data["prompt"],
                    "starter_code": data["starter_code"],
                    "test_suite": data["test_suite"],
                    "module": data["module"]
                }
            )
            self.stdout.write(f"  -> {'Created' if created else 'Updated'} assignment: {assignment.title} (Module {assignment.module})")
        self.stdout.write(self.style.SUCCESS("Successfully seeded all Python assignments!"))
