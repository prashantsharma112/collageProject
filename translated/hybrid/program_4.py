import math

principal = float(input("Enter Principal amount: "))
rate = float(input("Enter Rate of interest: "))
years = float(input("Enter Time (in years): "))

interest = principal * (rate / 100) * years
print("Simple Interest is: " + str(interest))