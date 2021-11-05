package defaultpackage



func Median(a, b, c int) (int) {
    var res int
    if (a>=b && a<=c) || (a>=c && a<=b) {
        res = a
    }
    if (b>=a && b<=c) || (b>=c && b<=a) {
        res = b
    } else {
        res = c 
    }
    return res
}



