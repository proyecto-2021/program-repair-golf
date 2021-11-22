def factorial(n)
  return 1 if n == 0
  return 1 if n == 1
  return (n) * factorial(n-2)
end