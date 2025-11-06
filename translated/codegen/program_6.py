import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    else:
        N = int(raw_input("Enter an integer to see its multiplication table: "))

    print("--- Table of " + N + " ---");