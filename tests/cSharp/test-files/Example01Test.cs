using NUnit.Framework;

[TestFixture]
public class Example01Tests {

    [Test]
    public void test1() {
        int a = 1;
        int b = 2;
        int result = Example01.max(a, b);
        Assert.AreEqual(2, result);	
    }

    [Test]
    public void test2() {
        int a = 2;
        int b = 1;
        int result = Example01.max(a, b);
        Assert.AreEqual(2, result);
    }

    [Test]
    public void test3() {
        int a = 2;
        int b = 2;
        int result = Example01.max(a, b);
        Assert.AreEqual(2, result);
    }

}
