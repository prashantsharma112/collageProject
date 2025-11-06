import sys

def main():
    if len(sys.argv)!= 2:
        print "Usage: " + sys.argv[0] + " temperature"
        sys.exit(1)

    temperature = float(sys.argv[1])
    print "Temperature is " + str(temperature)

if __name__ == "__main__":
    main()