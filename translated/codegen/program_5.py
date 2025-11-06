import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: " + sys.argv[0] + " <infile> <outfile>"
        sys.exit(1)

    infile = open(sys.argv[1], "r")
    outfile = open(sys.argv[2], "w")

    for line in infile:
        outfile.write(line)

    infile.close()
    outfile.close()