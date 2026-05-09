import java.util.regex.Matcher;
import java.util.regex.Pattern;

/*
 * Fill this code in.
 * All of your code must reside in this file.
 * Use regular expressions to solve these problems.
 * Do not change the names of the class or methods.
 * You can add methods static methods to this class.
 */

public class RegexS26 {
	/*
	 * 3 digits, dash, 3 digits, dash, and 4 digits.
	 * No intervening spaces.
	 */
	public static boolean isLongPhoneNumber(String str) {
		return Pattern.matches("\\d{3}-\\d{3}-\\d{4}", str);
	}
	/*
	 * Same as above, but the 3 digit blocks do not start with a 0 or 1,
	 */
	public static boolean isLongPhoneNumber2(String str) {
		return Pattern.matches("[2-9]\\d{2}-[2-9]\\d{2}-\\d{4}", str);
	}
	/*
	 * A simple definition of a real_literal:
	 * Decimal_Digit+ "." Decimal_Digit+ Exponent_Part? Real_Type_Suffix?
	 * where, Exponent_Part is (E or e) Sign? Decimal_Digit+
	 * where, Real_Type_Suffix is (F, f, D, d, M, or m).
	 * where, Decimal_Digit is 0, 1, 2, ... 9
	 * where, Sign is + or -
	 */
	public static boolean isRealLiteralPart1(String str) {
		return Pattern.matches("\\d+\\.\\d+([Ee][+-]?\\d+)?[FfDdMm]?", str);
	}
	public static void main(String [] args) {
		// You are encouraged to do more testing than what you see below.
		
		System.out.println(isLongPhoneNumber("513-529-1809"));		// true
		System.out.println(isLongPhoneNumber(" 513-529-1809 "));	// false
		System.out.println(isLongPhoneNumber("513 529 1809"));		// false
		System.out.println(isLongPhoneNumber("013-529-1809"));		// true

		System.out.println(isLongPhoneNumber2("513-529-1809"));		// true
		System.out.println(isLongPhoneNumber2("513-029-1809"));		// false
		System.out.println(isLongPhoneNumber2("013-529-1809"));		// false
		System.out.println(isLongPhoneNumber2("013-029-1809"));		// false
		
		System.out.println(isRealLiteralPart1("12.0"));				// true		
		System.out.println(isRealLiteralPart1("0.0E-12"));			// true		
		System.out.println(isRealLiteralPart1(".-12"));				// false
	}
}
