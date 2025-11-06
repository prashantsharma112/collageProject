def main():
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))
    c = int(input("Enter third number: "))

    max_num = a
    if b > max_num:
        max_num = b
    if c > max_num:
        max_num = c

    print("The largest number is:", max_num)

if __name__ == "__main__":
    main()