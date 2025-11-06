import java.util.Scanner;

public class SimpleInterest {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter Principal amount: ");
        double P = scanner.nextDouble();
        System.out.print("Enter Rate of interest: ");
        double R = scanner.nextDouble();
        System.out.print("Enter Time (in years): ");
        double T = scanner.nextDouble();

        double interest = (P * R * T) / 100;
        System.out.println("Simple Interest is: " + interest);
        scanner.close();
    }
}