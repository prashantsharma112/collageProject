N = int(input("Enter an integer to see its multiplication table: "))

print(f"--- Table of {N} ---")
for i in range(1, 11):
    print(f"{N} x {i} = {N * i}")
