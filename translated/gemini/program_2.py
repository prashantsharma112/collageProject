def main():
    number = int(input("Enter an integer: "))

    if number % 2 == 0:
        print(str(number) + " is an EVEN number.")
    else:
        print(str(number) + " is an ODD number.")

if __name__ == "__main__":
    main()