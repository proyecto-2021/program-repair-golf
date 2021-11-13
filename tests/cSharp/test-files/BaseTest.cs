// this Example is used to test post response if challenge and test are loaded correctly
using NUnit.Framework;

[TestFixture]
public class Example1Test {
    [Test]
    public void test1() {
        string result = Example1.example1();
        Assert.AreEqual("I'm a test", result);  
    }
}
