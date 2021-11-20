package defaultpackage



func Median(first, second, third int) (int) {
    var res int
    if (first>=second && first<=third) || (first>=third && first<=second) {
        res = first
    }
    if (second>=first && second<=third) || (second>=third && second<=first) {
        res = second
    } else {
        res = third 
    }
    return res
}



