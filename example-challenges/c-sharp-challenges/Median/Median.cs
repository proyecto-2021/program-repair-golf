using System;



public class Median {

    public static int median(int a, int b, int c) {
        int res;
        if ((a>=b && a<=c) || (a>=c && a<=b))
            res = a;
        if ((b>=a && b<=c) || (b>=c && b<=a))
            res = b;
        else
            res = c; 
        return res;
    }

    public static void Main(string[] args)
    {
        Console.WriteLine (median(1, 2, 3));
    }

}

