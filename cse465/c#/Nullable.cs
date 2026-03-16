using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

class NullableTest {
    public static string ClassifyAge(int? age) {
        string result;
        if (age.HasValue) {
            result = age.Value >= 18 ? "Adult" : "Minor";
        } else {
            result = "no value";
        }
        return result;
    }
    public static string ClassifyAge2(int? age) {
        string result;
        if (age is int intValue) {
            result = intValue >= 18 ? "Adult" : "Minor";
        } else {
            result = "no value";
        }
        return result;
    }
    public static void OtherThings() {
        int? w = 28;
        int x = w ?? -1;
        Console.WriteLine($"x is {x}");  // output: b is 28

        int? y = null;
        int z = y ?? -1;
        Console.WriteLine($"d is {z}");  // output: d is -1

        Console.WriteLine("Operator lifting");
        int? a = 10;
        int? b = null;
        int? sum = a + b;
        Console.WriteLine($"{a} >= null is {a >= b}");   // False
        Console.WriteLine($"{a} < null is {a < b}");     // False
        Console.WriteLine($"{a} == null is {a == b}");   // False

        String sumStr = sum.HasValue ? sum.Value.ToString() : "null";

        Console.WriteLine($"{a} + null is {sumStr}");   // Null

        int? c = null;
        int? d = null;
        Console.WriteLine($"null >= null is {c >= d}");     // False
        Console.WriteLine($"null == null is {c == d}");     // True
    }
    static void Main(string[] args) {
        int? age1 = null;
        int? age2 = 12;
        int age3 = 28;

        Console.WriteLine(ClassifyAge(age1));
        Console.WriteLine(ClassifyAge(age2));
        Console.WriteLine(ClassifyAge(age3));

        OtherThings();
    }
}
