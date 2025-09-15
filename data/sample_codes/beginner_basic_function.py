# Beginner level - basic functions and variables
def greet_user(name):
    message = "Hello, " + name + "!"
    return message

def add_numbers(a, b):
    result = a + b
    return result

# Using the functions
user_name = "Alice"
greeting = greet_user(user_name)
print(greeting)

num1 = 10
num2 = 20
sum_result = add_numbers(num1, num2)
print("Sum:", sum_result)