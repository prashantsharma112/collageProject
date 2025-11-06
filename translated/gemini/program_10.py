def main():
    text = input("Enter a string: ")
    target_char = input("Enter the character to count: ")[0]

    count = 0
    for i in range(len(text)):
        if text[i] == target_char:
            count += 1

    print("The character '" + target_char + "' appears " + str(count) + " times.")

if __name__ == "__main__":
    main()