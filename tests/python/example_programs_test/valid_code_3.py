
def medianas(a,b,c):
    res = 2
    if ((a>=b and a<=c) or (a>=c and a<=b)):
        res = a
    if ((b>=a and b<=c) or (b>=c and b<=a)):
        res = b
    else:
        res = c
    return res

