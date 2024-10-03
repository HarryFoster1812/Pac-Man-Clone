num1 = int(input("Enter a number: "))
num2 = int(input("Enter a second number: "))
print(f"The sum is {num1 + num2}\nThe product is {num1*num2}\nThe ratio is 1:{num2/num1}\nThe modulus is {num1 % num2}\nThe exponentiation is {num1**num2}")

#######################################################

celsius = float(input("Enter the temperature in celsius"))
far = celsius*(9/5) + 32
print(f"The result is {far}")

#######################################################

import math
radius = float(input("Enter the radius: "))
area = math.pi*(radius**2)
circumfrence = 2*math.pi*radius
print(f"Area is {area}, circumference is {circumfrence}")


#######################################################

radius = float(input("Enter the radius of the sphere"))
SurfaceArea = 4*math.pi*(radius**2)
Volume = (4/3)*math.pi*(radius**3)
print(f"The volume is {Volume}, The surface area is {SurfaceArea}")

#######################################################

height = float(input("Enter the height"))
radius = float(input("Enter the radius"))
SurfaceArea = 2*math.pi*height*radius + 2*math.pi*(radius**2)
print("The surface area is" + str(SurfaceArea))

#######################################################

firstName = input("Enter your first-name: ")
Surname = input("Enter your surname: ")
print(f"The initials will be {firstName[0] + Surname[0]}")

#######################################################

age = int(input("Enter your age: "))
if (age<18):
	print(False)
else:
	print(True)
