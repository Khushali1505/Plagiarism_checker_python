number = int(input("Enter a number: "))

flag = True
if number <= 1:
    flag = False
else:
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            flag = False
            break

if flag:
    print("Prime number")
else:
    print("Not a prime number")
