// This Example is used to test post response when no test fails
using NUnit.Framework;

[TestFixture]
public class Example4Test {
    [Test]
    public void test1() {
        string result = Example4.example4();
        Assert.AreEqual("I'm a test", result);	
    }
}