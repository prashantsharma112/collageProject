def main():
    N = int(input("Enter a non-negative integer: "))

    factorial = 1  # Use int for potentially large factorials
    for i in range(1, N + 1):
        factorial *= i

    print("The factorial of " + str(N) + " is: " + str(factorial))

if __name__ == "__main__":
    main()