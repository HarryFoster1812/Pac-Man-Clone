# The previous code was storing strings

def printState():
    print("Red Light is " + str(redLight))
    print("Yellow Light is " + str(yellowLight))
    print("Green Light is " + str(greenLight))
    print("The type of the data is " + str(type(redLight)))

redLight = 1
yellowLight = 0
greenLight = 0
printState()
