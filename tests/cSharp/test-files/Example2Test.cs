// this Example is used to test post response if source code has sintax errors
using NUnit.Framework;

[TestFixture]
public class Example2Test {
    [Test]
    public void test1() {
        string result = Example2.example2();
        Assert.AreEqual("I'm a test", result);	
    }
}
