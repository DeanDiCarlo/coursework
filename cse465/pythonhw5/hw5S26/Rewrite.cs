using System;

namespace Rewrite {
	public class Sample {
		// Rewrite the following code so that compound
		// assignment statements and the increment
		// operators are not used.
		public static int CompoundAssignment(int N) {
			int M = 3 * N;
			N = N * 3;
			M = M + 1;
			N = N + M;
			return N;
		}
		public static int Sum(int N) {
			return (N * N + N) / 2;
		}
		// Rewrite the following code so that assignment 
		// is not used as an expression.
		public static int AssignmentAsExpression(int N) {
			int total = 0;
			int i = 1;
			int x = Sum(i);
			i = i + 1;
			while (x < 10000) {
				total = total + x;
				x = Sum(i);
				i = i + 1;
			}
			return total;
		}
		// Add parenthesis until the expression is fully 
		// parenthesized. That is, all performed operations
		// appear within a () pair. Here are some examples:
		//	3 + 2 * 3  --> (3 + (2*3))
		//	3 + 2 * 3 + 4  --> ((3 + (2*3)) + 4)
		//	(3 + 2) * 3 + 4  --> (((3 + 2) * 3) + 4)
		// The resulting expression must be equivalent to the
		// the original. Do not rearrange the terms, not delete
		// them. For every operator, there must be one pair of 
		// of parenthesis.
		public static int OperatorPrecedence1(int A, int B) {
			return ((A + ((B * 100) / A)) + A);
		}
		public static int OperatorPrecedence2(int A, int B) {
			return ((A << 2) >> B);
		}
		public static int OperatorPrecedence3(int A, int B) {
			return (A | (B ^ (A & 0xFF)));
		}
		public static int OperatorPrecedence4(int A, int B) {
			return (B += (3 * A));
		}
		public static bool OperatorPrecedence5(bool A, bool B, bool C, bool D) {
			return ((((! A) == B) && C) || D);
		}
		public static void Main(string [] args) {
			Console.WriteLine(CompoundAssignment(10));
			Console.WriteLine(AssignmentAsExpression(10));
			Console.WriteLine(OperatorPrecedence1(5, 4));
			Console.WriteLine(OperatorPrecedence2(5, 4));
			Console.WriteLine(OperatorPrecedence3(5, 4));
			Console.WriteLine(OperatorPrecedence4(5, 4));
			Console.WriteLine(OperatorPrecedence5(false, false, false, false));
		}
	}
}
