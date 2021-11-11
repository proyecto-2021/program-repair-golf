// This Example is used to test post response when test code has sintax errors
using System;

public class Example3 {
    public static string example3() {
        return "I'm not a test";
    }
    public static void Main(string[] args) {
        Console.WriteLine (example3());
    }
}