import sys

def main():
    if len(sys.argv)!= 2:
        print "Usage: " + sys.argv[0] + " radius"
        sys.exit(1)

    radius = float(sys.argv[1])
    area = Math.PI * radius * radius
    print "The area of the circle is: " + area

if __name__ == "__main__":
    main()