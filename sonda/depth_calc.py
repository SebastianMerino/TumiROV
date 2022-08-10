def calc_profundidad(p,lat):
	"""
	Calcula la profundidad a la que está sumergido el ROV en función
	de la presión en dbar y la latitud (positiva). Con la fórmula de
	"Depth-pressure relationships in the oceans and seas" por
	Claude C. Leroy y Francois Parthiot
	"""
	from math import pi, sin
	c1,c2,c3,c4 = 9.7266, -2.2512E-5, 2.28E-10, -1.8E-15
	lat = 12.5
	g = 9.7803 * (1+ 5.3E-3*sin(lat*pi/180))
	z = (c1*p + c2*p**2 + c3*p**3 + c4*p**4)/(g + 1.1E-6*p)
	corr = p/(p+100) + 5.7E-4*p
	return z+corr

while True:
	p = int(input('Ingresar presion: '))
	lat = int(input('Ingresar latitud: <'))
	z = calc_profundidad(p,lat)
	print('Profundidad: ', z, 'm')