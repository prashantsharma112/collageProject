def main():
    celsius = float(input("Enter temperature in Celsius: "))

    fahrenheit = (celsius * 9 / 5) + 32
    print(str(celsius) + "°C is equal to " + str(fahrenheit) + "°F")

if __name__ == "__main__":
    main()