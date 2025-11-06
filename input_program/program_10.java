import java.util.Scanner;

public class CharacterCounter {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a string: ");
        String text = scanner.nextLine();
        System.out.print("Enter the character to count: ");
        // Read the first character of the next input line
        char targetChar = scanner.nextLine().charAt(0);

        int count = 0;
        // Iterate through the string's characters
        for (int i = 0; i < text.length(); i++) {
            if (text.charAt(i) == targetChar) {
                count++;
            }
        }

        System.out.println("The character '" + targetChar + "' appears " + count + " times.");
        scanner.close();
    }
}