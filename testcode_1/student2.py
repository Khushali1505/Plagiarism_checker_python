def fact(x):
    if x == 1 or x == 0:
        return 1
    return x * fact(x - 1)

number = int(input("Enter a number: "))
result = fact(number)
print(f"The factorial of {number} is {result}")
