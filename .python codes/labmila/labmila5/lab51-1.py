a = int(input("a "))
b = int(input("b "))
c = int(input("c "))
delta = b*b -4*a*c
bhas1 = (-b + delta**(1/2))/(2*a)
bhas2 = (-b - delta**(1/2))/(2*a)
if delta > 0:
    print(f"x1 se equivale a {bhas1} e x2 se equivale a {bhas2}")
else:
    print("Error")
