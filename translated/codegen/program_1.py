import sys

if __name__ == "__main__":
    if len(sys.argv)!= 3:
        print "Usage: " + sys.argv[0] + " num1 num2"
        sys.exit(1)

    num1 = int(sys.argv[1])
    num2 = int(sys.argv[2])

    sum = num1 + num2;
    print "The sum is: " + sum