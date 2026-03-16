using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataStructures {
    public class ComplexNumber {
        private double a, b;
        public ComplexNumber(double i, double j) {
            a = i;
            b = j;
        }
        public static ComplexNumber operator +(ComplexNumber a, ComplexNumber b) {
            ComplexNumber result = new ComplexNumber(a.a + b.a, a.b + b.b);
            return result;
        }
        public override String ToString() {
            if (b < 0) {
                return String.Format("({0}{1}i)", a, b);
            } else {
                return String.Format("({0}+{1}i)", a, b);
            }
        }
        public override int GetHashCode() {
            return a.GetHashCode() << 8 | b.GetHashCode();
        }
        public override bool Equals(Object obj) {
            ComplexNumber other = (ComplexNumber)obj;
            bool result = a == other.a && b == other.b;
            return result;
        }
        public double Real {
            get {
                return a;
            }
            set {
                a = value;
            }
        }
        public double Imaginary {
            get {
                return b;
            }
            set {
                b = value;
            }
        }
        public double OtherData {
            get;
            set;
        }
    }
}
