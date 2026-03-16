using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Delegates {
    class Delegates {
        public delegate int IntFunc(int x);
        public delegate String StringFunc(String s);

        public static int echo(int x) {
            return x;
        }
        public static int sqr(int x) {
            return x * x;
        }
        public static int sum(int N, IntFunc f) {
            int sum = 0;
            for (int i = 0; i <= N; i++) {
                sum += f(i);
            }
            return sum;
        }
        static void DelegateExample() {
            Console.WriteLine("Start DelegateExample");
            const int N = 5;
            Console.WriteLine(N * N);
            Console.WriteLine(sqr(N));

            Console.WriteLine(sum(100, echo));
            Console.WriteLine(sum(100, sqr));

            Console.WriteLine();
        }


        delegate void VoidFunc(int a);
        public static void f1(int a) { Console.WriteLine(a); }
        public static void f2(int a) { Console.WriteLine(2 * a); }
        public static void f3(int a) { Console.WriteLine(3 * a); }
        static void MulticastDelegateExample() {
            VoidFunc func = f1;
            func += f2;
            func += f3;
            func(4);
        }
        public static void Main(string[] args) {
            DelegateExample();
            MulticastDelegateExample();
        }
    }
}
