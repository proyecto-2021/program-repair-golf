import static org.junit.Assert.*;
import org.junit.Test;

public class MedianTest {

    @Test
    public void test1() {
        int a = 1;
        int b = 2;
	int c = 3;
	int result = Median.median(a, b, c);
	assertEquals(2, result);	
    }

    @Test
    public void test2() {
        int a = 2;
        int b = 1;
        int c = 3;
        int result = Median.median(a, b, c);
        assertEquals(2, result);
    }

    @Test
    public void test3() {
        int a = 3;
        int b = 1;
        int c = 2;
        int result = Median.median(a, b, c);
        assertEquals(2, result);
    }

}


