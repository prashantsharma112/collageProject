import sys

if __name__ == "__main__":
    if len(sys.argv)!= 2:
        print("Usage: " + sys.argv[0] + " <number>")
        sys.exit(1)
    else:
        number = int(sys.argv[1])
        print(number)