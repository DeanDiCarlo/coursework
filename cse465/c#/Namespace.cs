using System;
using System.Text;
using NS1;


namespace NS1 {
    public class C1 {
        private int x;
        public C1(int value) {
            x = value;
        }
        public override string ToString() {
            return x.ToString();
        }
    }
    public class C2 {
        private int x;
        public C2(int value) {
            x = value;
        }
        public override string ToString() {
            return x.ToString();
        }
    }
}
namespace NS2 {
    public class C1 {
        private int x;
        public C1(int value) {
            x = value;
        }
        public override string ToString() {
            return x.ToString();
        }
    }
}

namespace OtherNS {
    public class Tester {
        static void Main(string[] args) {
            NS1.C1 a = new NS1.C1(1);
            NS2.C1 b = new NS2.C1(2);
            C2 c = new C2(3);           // allowed because of "using NS1;"

            Console.WriteLine(a);
            Console.WriteLine(b);
            Console.WriteLine(c);
        }
    }
}
