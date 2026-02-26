def factorial_iterative(n):
    ans = 1
    for i in range(1, n + 1):
        ans *= i
    return ans

n = int(input("Enter any number: "))
print("Factorial =", factorial_iterative(n))

