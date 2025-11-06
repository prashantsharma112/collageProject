import math

def main():
    radius = float(input("Enter the radius of the circle: "))
    area = math.pi * radius * radius
    print("The area of the circle is: " + str(area))

if __name__ == "__main__":
    main()