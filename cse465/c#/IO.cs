using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

public class IO {
    public static OUT_T[] Convert<IN_T, OUT_T>(IN_T[] items, Func<IN_T, OUT_T> F) {
        int len = items.Length;
        OUT_T[] result = new OUT_T[len];
        for (int i = 0; i < len; i++) {
            result[i] = F(items[i]);
        }
        return result;
    }
    static void Main(string[] args) {
        using (StreamWriter output = new StreamWriter("sorted.txt"))
        using (StreamReader input = new StreamReader("items.csv")) {
            while (!input.EndOfStream) {
                string? line = input.ReadLine();
                string[]? toks = line?.Split(',');
                if (toks == null) {
                    continue;
                }
                int[] values = Convert(toks, Int32.Parse);
                Array.Sort(values);
                foreach (int value in values) {
                    output.Write(value + " ");
                }
                output.WriteLine();
            }
        }
    }
}
