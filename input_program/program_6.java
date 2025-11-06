import java.util.Scanner;

public class MultiplicationTable {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter an integer to see its multiplication table: ");
        int N = scanner.nextInt();

        System.out.println("--- Table of " + N + " ---");
        for (int i = 1; i <= 10; i++) {
            System.out.println(N + " x " + i + " = " + (N * i));
        }
        scanner.close();
    }
}