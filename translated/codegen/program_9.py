import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    else:
        N = int(input("Enter a non-negative integer: "))
    print("The factorial of " + N + " is: " + factorial(N))