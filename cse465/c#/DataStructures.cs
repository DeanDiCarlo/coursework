using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataStructures {

    public class DataStructures {
        public static void DisplayStuff<T>(IEnumerable<T> items) {
            foreach (T item in items) {
                Console.Write(item + " ");
            }
            Console.WriteLine();
        }
        public static void TestBasicList() {
            List<int> list1 = new List<int>();
            for (int i = 0; i < 10; i++) {
                int item1 = (int)Math.Pow(2, i);
                int item2 = 2 * i;
                list1.Add(item1);
                list1.Add(item2);
            }
            DisplayStuff(list1);
        }
        public static void TestBasicSets() {
            //HashSet<int> set1 = new HashSet<int>();
            SortedSet<int> set1 = new SortedSet<int>();
            for (int i = 0; i < 10; i++) {
                int item1 = (int)Math.Pow(2, i);
                int item2 = 2 * i;
                set1.Add(item1);
                set1.Add(item2);
            }
            DisplayStuff(set1);
        }
        public static void TestBasicDictionary() {
            Dictionary<string, int> ages = new Dictionary<string, int>();
            ages.Add("fred", 21);
            ages["sarah"] = 13;
            ages["sammy"] = 5;

            foreach (string name in ages.Keys) {
                Console.WriteLine("Name: " + name + " is " + ages[name] + " years");
            }
        }
        public static void TestBasicStack() {
            Stack<string> stk = new Stack<string>();
            stk.Push("hello");
            stk.Push("world");
            string a = stk.Peek();
            string b = stk.Pop();
            string c = stk.Pop();
            Console.WriteLine("Stack items: {0} {1} {2}", a, b, c);
        }
        public static void TestCustomHashSet() {
            HashSet<ComplexNumber> set = new HashSet<ComplexNumber>();
            ComplexNumber i1 = new ComplexNumber(3, 4);
            ComplexNumber i2 = new ComplexNumber(-3, 4);
            ComplexNumber i3 = new ComplexNumber(-3, -4);

            i1.Real = 10;
            i1.Imaginary = 11;
            i1.OtherData = 12;

            set.Add(i2);
            set.Add(i1);
            set.Add(i2);
            set.Add(i3);
            set.Add(i1);
            Console.WriteLine(i2.GetHashCode());
            DisplayStuff(set);
        }
        static void Main(string[] args) {
            TestBasicList();
            TestBasicSets();
            TestBasicDictionary();
            TestBasicStack();
            TestCustomHashSet();
        }
    }
}
