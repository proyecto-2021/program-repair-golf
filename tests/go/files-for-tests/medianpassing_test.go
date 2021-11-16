package defaultpackage


import "testing"


func TestAdd1(t *testing.T){
    var a, b, c int = 1, 2, 3
    var result int = Median(a, b, c)
    if result != 2 {
        t.Errorf("got %d, wanted %d", result, 2)
    }
}