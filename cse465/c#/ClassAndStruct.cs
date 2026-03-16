using System;
using System.Text;


public class RectangleClass {
    public double lx, ly, rx, ry;
    public RectangleClass(double LX, double LY, double RX, double RY) {
        lx = LX;
        ly = LY;
        rx = RX;
        ry = RY;
    }
    public override string ToString() { return String.Format("RC ({0},{1},{2},{3})", lx, ly, rx, ry); }
}
public struct RectangleStruct {
    public double lx, ly, rx, ry;
    public RectangleStruct(double LX, double LY, double RX, double RY) {
        lx = LX;
        ly = LY;
        rx = RX;
        ry = RY;
    }
    public override string ToString() { return String.Format("RS ({0},{1},{2},{3})", lx, ly, rx, ry); }
}
public class Tester {
    static void Main(string[] args) {
        RectangleClass rcOrig = new RectangleClass(-10, -10, 10, 10);
        RectangleClass rcCopy = rcOrig;

        Console.WriteLine();
        Console.WriteLine("Class demo");
        Console.WriteLine("Before: Original - {0} Copy - {1}", rcOrig, rcCopy);
        rcOrig.lx = rcOrig.ly = 0;
        rcOrig.rx = rcOrig.ry = 2;
        Console.WriteLine("After: Original - {0} Copy - {1}", rcOrig, rcCopy);

        RectangleStruct rsOrig = new RectangleStruct(-10, -10, 10, 10);
        RectangleStruct rsCopy = rsOrig;

        Console.WriteLine();
        Console.WriteLine("Struct demo");
        Console.WriteLine("Before: Original - {0} Copy - {1}", rsOrig, rsCopy);
        rsOrig.lx = rsOrig.ly = 0;
        rsOrig.rx = rsOrig.ry = 2;
        Console.WriteLine("After: Original - {0} Copy - {1}", rsOrig, rsCopy);
    }
}