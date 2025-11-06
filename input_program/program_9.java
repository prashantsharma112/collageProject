import java.util.Scanner;

public class FactorialCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a non-negative integer: ");
        int N = scanner.nextInt();

        long factorial = 1; // Use long for potentially large factorials
        for (int i = 1; i <= N; i++) {
            factorial *= i;
        }

        System.out.println("The factorial of " + N + " is: " + factorial);
        scanner.close();
    }
}