#original LOC 400
#new LOC 130
from decimal import Decimal
class Angle():
    
    def __init__(self):
        #instance of angle
        self.angle = 0.0
              
    def setDegrees(self, degrees = 0.0):
        
        try:
            #calculate for degrees
            self.angle = (float(degrees) % 360.0)
            degree = int(self.angle)
            #calculate for minutes
            minutes = round((self.angle - degree)*60, 1)
            #compute angle with degree and minute
            self.angle = degree + minutes/60.0
            return self.angle
        except:
            raise ValueError("Angle.setDegrees: Degree Value is incorrect")
           
    def setDegreesAndMinutes(self, degAndMin = None):
        #original LOC 100
        #new LOC 35
        try:
            DAM = degAndMin.split("d")
            if float(DAM[1])<0.0:
                raise ValueError("Angle.setDegreesAndMinutes: d separator is missing")
            
            if (DAM == None):
                raise ValueError("Angle.setDegreesAndMinutes: No data")
        
            #assign variables for split
            splitDegree = int(DAM[0])
            splitMinute = float(DAM[1])/60
        
            #check to see if there is more than one decimal place
            decimal = abs(Decimal(DAM[1]).as_tuple().exponent)
            if (decimal > 1):
                raise ValueError("Angle.setDegreesAndMinutes: Minute must have only one decimal place")
        
            #check degree portion and compute
            if (-360 < splitDegree < 0):
                self.angle = 360 -(abs(splitDegree)+splitMinute)
            else:
                self.angle = (splitDegree%360)+splitMinute
            return self.angle
        except:
            raise ValueError("Angle.setDegreesAndMinutes: Value is incorrect")
    
    def add(self, angleAdd=None):
        #original LOC 60
        #new LOC 20
        #check to see if something is there
        if (angleAdd == None):
            raise ValueError("Angle.add: Missing Parameters")
        #check to see if it is not an instance of angle (raise error)
        #elif (not isinstance(angleAdd, Angle)):
            #raise ValueError("Angle.add: Not Angle Instance")
        #check to see if it is instance of angle and perform calculations
        elif (isinstance(angleAdd, Angle)):
            self.angle = (self.angle+angleAdd.angle)%360
            return self.angle
        else:
            raise ValueError("Angle.add: Missing Parameters")
        
        
    def subtract(self, angleSubtract = None):
        #original LOC 60
        #new LOC 20
        #check to see if something is there
        if (angleSubtract == None):
            raise ValueError("Angle.subtract: Missing Parameter")
        #check to see if it is not an instance of angle (raise error)
        #elif (not isinstance(angleSubtract, Angle)):
            #raise ValueError("Angle.add: Not Angle Instance")
        #check to see if it is instance of angle and perform calculations
        elif (isinstance(angleSubtract, Angle)):
            self.angle = (self.angle-angleSubtract.angle)%360
            return self.angle
        else:
            raise ValueError("Angle.subtract: Missing Parameter")

        
    def compare(self, angleCompare = None):
        #original LOC 50
        #new LOC 25
        a = 1
        b = -1
        c = 0
        #check to see if something is there
        if (angleCompare == None):
            raise ValueError("Angle.compare: Missing Parameter")
        #check to see if not instance of angle (raise error)
        #elif (not isinstance(angleCompare, Angle)):
            #raise ValueError("Angle.add: Not Angle Instance")
        elif (isinstance(angleCompare, Angle)):
            if (self.angle > angleCompare.angle):
                return a
            elif (self.angle < angleCompare.angle):
                return b
            else:
                return c
        else:
            raise ValueError("Angle.compare: Angle is incorrect")
        
      
    def getString(self):
        #original LOC 40
        #new LOC 10
        
        stringDegree = str(int(self.angle)//1)
        stringMinute = str(round( ( ( self.angle%1)*60.0),1))   
        newString = stringDegree+"d"+stringMinute
        print newString
        return newString
    
    def getDegrees(self):
        #original LOC 35
        #new LOC 5
        
        #compute angle
        self.angle = self.angle%360
        return self.angle
    
    