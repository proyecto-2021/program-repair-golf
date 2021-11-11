// this Example is used to test post response if challenge and test are loaded correctly
using NUnit.Framework;

[TestFixture]
public class Example5Test {
    [Test]
    public void test1() {
        string result = Example5.example5();
        Assert.AreEqual("Test fail", result);  
    }
}
