import Navigation.prod.Angle as Ang

myAngle = Ang.Angle()

#myAngle.__init__()

#x = myAngle.setDegrees(-10)
#print x.degrees

x = myAngle.setDegreesAndMinutes("100d85")    
print x.degrees
print x.minutes

#Ang.Angle().add("700d61")

#x = myAngle.add("700d61")
#print x.degrees
#print x.minutes

#x = myAngle.add("700d61","45d10.1")
#print x.degrees
#print x.minutes

#myAngle.subtract("700d100")

#x = myAngle.subtract("700d100")
#print x.degrees
#print x.minutes

#myAngle.compare("700d45")

#x = myAngle.compare("700d100","-700d100")
#print x.degrees
#print x.minutes

#myAngle.getString()

#myAngle.getDegrees()


