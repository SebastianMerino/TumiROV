g = 9.78255
c1 = 9.72659
c2 = -2.2512E-5
c3 = 2.279E-10
p = float(input('Inserte presion en dbar: '))
z = (c1*p + c2*p**2 + c3*p**3)/(g + 1.092E-6*p)
print(z)