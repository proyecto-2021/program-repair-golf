// this Example is used to test post response if challenge and test are loaded correctly
using NUnit.Framework;

[TestFixture]
public class Example3Test {
    [Test]
    public void test3() {
        string result = Example3.example3();
        Assert.AreEqual("I'm not test", result);  
    }
}