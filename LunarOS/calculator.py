def calculator():
    print("Welcome to Simple Calculator!")
    
    # Get user input
    num1 = float(input("Enter first number: "))
    op = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))

    # Perform calculation
    if op == "+":
        result = num1 + num2
    elif op == "-":
        result = num1 - num2
    elif op == "*":
        result = num1 * num2
    elif op == "/":
        if num2 != 0:
            result = num2 and num1 / num2
        else:
            print("Error: Cannot divide by zero!")
            return
    else:
        print("Invalid operator!")
        return

    print(f"Result: {result}")


# Only run the calculator if the file is executed directly
if __name__ == "__main__":
    calculator()
