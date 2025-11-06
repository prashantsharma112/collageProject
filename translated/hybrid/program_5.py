import sys

def main():
    original = input("Enter a word or phrase: ")
    reversed = original[::-1]
    if original == reversed:
        print("'" + original + "' is a Palindrome.")
    else:
        print("'" + original + "' is NOT a Palindrome.")

if __name__ == '__main__':
    main()