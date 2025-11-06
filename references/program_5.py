text = input("Enter a word or phrase: ")

if text.lower() == text[::-1].lower():
    print(f"'{text}' is a Palindrome.")
else:
    print(f"'{text}' is NOT a Palindrome.")
