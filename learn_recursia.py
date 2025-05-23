def func1(x, lst):
    if x > 0:
        x -= 1
        lst.append(x)
        return func1(x, lst)  # Ensure the return value of the recursive call is passed up the chain
    else:
        return x, lst

def factorial(n):
    if n == 1:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case


print(factorial(3))

""""
x = 3
lst = []
x2, lst2 = func1(x, lst)
print(x2, lst2)
"""