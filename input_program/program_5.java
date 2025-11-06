import java.util.Scanner;

public class PalindromeChecker {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a word or phrase: ");
        String original = scanner.nextLine();

        // Reverse the string
        String reversed = new StringBuilder(original).reverse().toString();

        if (original.equalsIgnoreCase(reversed)) {
            System.out.println("'" + original + "' is a Palindrome.");
        } else {
            System.out.println("'" + original + "' is NOT a Palindrome.");
        }
        scanner.close();
    }
}