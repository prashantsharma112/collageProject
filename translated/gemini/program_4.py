def main():
    P = float(input("Enter Principal amount: "))
    R = float(input("Enter Rate of interest: "))
    T = float(input("Enter Time (in years): "))

    interest = (P * R * T) / 100
    print("Simple Interest is: " + str(interest))

if __name__ == "__main__":
    main()