using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace Arrays {
    public class MatrixTester {
        public const int R1 = 1000, C1 = 1000;
        public const int R2 = C1, C2 = 600;
        public const int R3 = R1, C3 = C2;
        public const int SEED = 34;

        public static int[][] CreateMatrix(int R, int C) {
            Random rand = new Random(SEED);
            int[][] result = new int[R][];
            for (int i = 0; i < R; i++) {
                result[i] = new int[C];
                for (int j = 0; j < C; j++) {
                    result[i][j] = rand.Next() % 10;
                }
            }
            return result;
        }
        public static int[,] CreateRectangularMatrix(int R, int C) {
            Random rand = new Random(SEED);
            int[,] result = new int[R, C];
            for (int i = 0; i < R; i++) {
                for (int j = 0; j < C; j++) {
                    result[i, j] = rand.Next() % 10;
                }
            }
            return result;
        }
        public static void MatrixMult(int[][] mat1, int[][] mat2, int[][] mat3) {
            int R1 = mat1.Length;
            int C1 = mat1[0].Length;
            int R2 = mat2.Length;
            int C2 = mat2[0].Length;
            int R3 = mat3.Length;
            int C3 = mat3[0].Length;
            Debug.Assert(C1 == R2 && R3 == R1 && C3 == C2);
            for (int r = 0; r < R3; r++) {
                for (int c = 0; c < C3; c++) {
                    mat3[r][c] = 0;
                    for (int i = 0; i < C1; i++) {
                        mat3[r][c] += mat1[r][i] * mat2[i][c];
                    }
                }
            }
        }
        public static void RectMatrixMult(int[,] mat1, int[,] mat2, int[,] mat3) {
            int R1 = mat1.GetLength(0);
            int C1 = mat1.GetLength(1);
            int R2 = mat2.GetLength(0);
            int C2 = mat2.GetLength(1);
            int R3 = mat3.GetLength(0);
            int C3 = mat3.GetLength(1);
            Debug.Assert(C1 == R2 && R3 == R1 && C3 == C2);
            for (int r = 0; r < R3; r++) {
                for (int c = 0; c < C3; c++) {
                    mat3[r, c] = 0;
                    for (int i = 0; i < C1; i++) {
                        mat3[r, c] += mat1[r, i] * mat2[i, c];
                    }
                }
            }
        }
        public static unsafe void RectMatrixMultWithPointers(int[,] mat1, int[,] mat2, int[,] mat3) {
            int R1 = mat1.GetLength(0);
            int C1 = mat1.GetLength(1);
            int R2 = mat2.GetLength(0);
            int C2 = mat2.GetLength(1);
            int R3 = mat3.GetLength(0);
            int C3 = mat3.GetLength(1);
            Debug.Assert(C1 == R2 && R3 == R1 && C3 == C2);
            int row, col, i;
            fixed (int* M1 = &mat1[0, 0], M2 = &mat2[0, 0]) {
                for (row = 0; row < R3; row++) {
                    for (col = 0; col < C3; col++) {
                        int sum = 0;
                        int* a = M1 + C1 * row;
                        int* b = M2 + col;
                        for (i = 0; i < C1; i++, a++, b += C2) {
                            sum += (*a) * (*b);
                        }
                        mat3[row, col] = sum;
                    }
                }
            }
        }
        public static void TestMatrixMult() {
            int[][] mat1 = CreateMatrix(R1, C1);
            int[][] mat2 = CreateMatrix(R2, C2);
            int[][] mat3 = CreateMatrix(R3, C3);
            int[,] rmat1 = CreateRectangularMatrix(R1, C1);
            int[,] rmat2 = CreateRectangularMatrix(R2, C2);
            int[,] rmat3 = CreateRectangularMatrix(R3, C3);
            int[,] r2mat1 = CreateRectangularMatrix(R1, C1);
            int[,] r2mat2 = CreateRectangularMatrix(R2, C2);
            int[,] r2mat3 = CreateRectangularMatrix(R3, C3);

            DateTime start = DateTime.Now;
            MatrixMult(mat1, mat2, mat3);
            DateTime end = DateTime.Now;
            TimeSpan delta = end.Subtract(start);
            Console.WriteLine(delta);

            start = DateTime.Now;
            RectMatrixMult(rmat1, rmat2, rmat3);
            end = DateTime.Now;
            delta = end.Subtract(start);
            Console.WriteLine(delta);

            start = DateTime.Now;
            RectMatrixMultWithPointers(r2mat1, r2mat2, r2mat3);
            end = DateTime.Now;
            delta = end.Subtract(start);
            Console.WriteLine(delta);
        }
        public static void Main(string[] args) {
            MatrixTester.TestMatrixMult();
        }
    }
}
