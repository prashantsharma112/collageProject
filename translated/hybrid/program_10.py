import sys

def main():
    text = input("Enter a string: ")
    targetChar = input("Enter the character to count: ")

    count = 0
    for i in range(len(text)):
        if text[i] == targetChar:
            count += 1

    print("The character '" + targetChar + "' appears " + count + " times.")

if __name__ == '__main__':
    main()