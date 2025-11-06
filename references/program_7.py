a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
c = int(input("Enter third number: "))

max_value = a
if b > max_value:
    max_value = b
if c > max_value:
    max_value = c

print("The largest number is:", max_value)
