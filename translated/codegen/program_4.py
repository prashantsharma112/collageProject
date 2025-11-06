import sys

def main():
    if len(sys.argv)!= 3:
        print "Usage: " + sys.argv[0] + " <Principal amount> <Rate of interest> <Time (in years)>"
        sys.exit(1)
    P = float(sys.argv[1])
    R = float(sys.argv[2])
    T = float(sys.argv[3])
    interest = (P * R * T) / 100
    print "Simple Interest is: " + interest

if __name__ == "__main__":
    main()