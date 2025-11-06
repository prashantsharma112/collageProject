def main():
    N = int(input("Enter an integer to see its multiplication table: "))

    print("--- Table of " + str(N) + " ---")
    for i in range(1, 11):
        print(str(N) + " x " + str(i) + " = " + str(N * i))

if __name__ == "__main__":
    main()