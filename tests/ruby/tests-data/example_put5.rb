def median2(a,b,c)
  res = 0
  if ((a>=b and a<=c) or (a>=c and a<=b))
    res = a
  end
  if ((b>=a and b<=c) or (b>=c and b<=a))
    res = b
  else
    res = c
  end
  return res
end
