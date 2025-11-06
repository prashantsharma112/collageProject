N = int(input("Enter a non-negative integer: "))

factorial = 1
for i in range(1, N + 1):
    factorial *= i

print(f"The factorial of {N} is: {factorial}")
