a = int(input("Digite o primeiro número"))
b = int(input("Digite o segundo número"))
c = int(input("Digite o terceiro número"))
exp1 = a + b != c
exp2 = (a>b)*a + (b>a)*b < 2*c
exp3 = a % 5 == 0 or b % 5 == 0 or c % 5 == 0 
exp4 = a != b and  a != c and b != c
print(a + b != c,
(a>b)*a + (b>a)*b < 2*c,
a % 5 == 0 or b % 5 == 0 or c % 5 == 0 ,
a != b and  a != c and b != c)