import sys

N = int(input("Enter an integer to see its multiplication table: "))

print("--- Table of " + N + " ---")
for i in range(1, 11):
    print(N + " x " + i + " = " + (N * i))