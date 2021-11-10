// This Example is used to test post response when test code has sintax errors
using NUnit.Framework;

[TestFixture]
public class Example3Test {
    [Test]
    public void test1() {
        string result = Example3.example3()
        Assert.AreEqual("I'm a test", result);	
    }
}
