text = input("Enter a string: ")
target_char = input("Enter the character to count: ")[0]

count = 0
for char in text:
    if char == target_char:
        count += 1

print(f"The character '{target_char}' appears {count} times.")
