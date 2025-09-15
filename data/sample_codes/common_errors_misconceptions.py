# Common Python misconceptions and errors for testing

# Error 1: Mutable default arguments
def add_item_bad(item, target_list=[]):
    target_list.append(item)
    return target_list

# Error 2: Late binding closures
functions = []
for i in range(5):
    functions.append(lambda: i)  # Will always return 4

# Error 3: Mixing tabs and spaces
def mixed_indentation():
    if True:
        print("Using spaces")
	print("Using tab")  # This line uses tab

# Error 4: Confusion between is and ==
a = [1, 2, 3]
b = [1, 2, 3]
if a is b:  # Should use == for value comparison
    print("Lists are identical")

# Error 5: Modifying list during iteration
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # Dangerous!

# Error 6: Variable scope confusion
def scope_confusion():
    if True:
        x = "inside if"
    print(x)  # x is still accessible in Python

# Error 7: String concatenation in loop
def inefficient_concat(words):
    result = ""
    for word in words:
        result = result + word + " "  # Should use join()
    return result

# Error 8: Not understanding truthiness
def check_empty(value):
    if len(value) == 0:  # Could just use 'if not value:'
        return True
    return False