import sys

if __name__ == "__main__":
    if len(sys.argv)!= 3:
        print "Usage: " + sys.argv[0] + " first_number second_number third_number"
        sys.exit(1)

    first_number = int(sys.argv[1])
    second_number = int(sys.argv[2])
    third_number = int(sys.argv[3])

    print "The largest number is: " + (first_number + second_number + third_number)