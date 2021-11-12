using System;


//Max code wit sintax error.
public class Example01 {

    public static int max(int a, int b){
        int res;
        if (a>=b)
            res = a;
        else
            res = a; 
        return res;
    }

    public static void Main(string[] args)
    {
        Console.WriteLine (max(1, 2));
    }

}
