using System;

namespace cs {
    public class Params {
        public static void f(int a, out int b, ref int c) {
            int x = 1;
            a = 1;      // value param
                        // x = b;	// illegal, b must be set first
            b = 2;
            c = 0;
            x = c;
        }
        public static void Main() {
            int a = 1, y, z = 3;
            f(a, out y, ref z);
			Console.WriteLine(a);
			Console.WriteLine(y);
			Console.WriteLine(z);
        }
    }
}
