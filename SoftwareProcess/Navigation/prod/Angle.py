
class Angle():
    
    def __init__(self):
        
        self.degrees = 0
        
        self.minutes = 0       
                             
    def setDegrees(self, degrees = 0):
        
        if isinstance(degrees,int):
            if (degrees>360):
                degrees = degrees%360
                self.degrees = degrees
                #print self.degrees, "1"
            
            if (degrees<0):
                degrees = abs(degrees + 360)
                self.degrees = degrees
                #print self.degrees, "1"
                
            else:
                self.degrees = degrees
            
        elif isinstance(degrees, float):
            
            if (degrees>360):
                degrees = degrees%360
                self.degrees = degrees
                #print self.degrees, "1"
            
            if (degrees<0):
                degrees = abs(degrees + 360)
                self.degrees = degrees
                #print self.degrees, "2"
        
            else:
                self.degrees = degrees        
            
        
        else:
            raise ValueError("Degree Value is neither an integer or float")
            #print self.degrees, "3"
        #print self.degrees
        return self
    def setDegreesAndMinutes(self, degAndMin = None):
        
        #print self.degrees
        #print self.minutes
        
        if degAndMin.find('d')<0:
            raise ValueError("d separator is missing")
        
        if (degAndMin == None):
            raise ValueError("No data")
        
        else: 
            DAM = degAndMin.split('d')
            try: 
                splitDegree = int (DAM[0])
                carryOver = splitDegree
    #    print splitDegree
            except:
                raise ValueError("Not an Integer")
            
            if (splitDegree>360):
                splitDegree = splitDegree%360
                #print splitDegree, "splitDegree"
                #print splitDegree
            self.degrees = splitDegree
            
            if (splitDegree < 0):
                if DAM[1]>0:
                    #carryOver = splitDegree
                    splitDegree = abs((splitDegree)+360)

                    # print splitDegree

                else:

                    splitDegree = abs(splitDegree + 360)

                    #print splitDegree, "negativesplit"
                #print splitDegree, "negativesplit"
            
            try:
                splitMinute = float(DAM[1])
            except:
                raise ValueError("Not a Float")
            
                    
            dSM = DAM[1].split('.')
            #print dSM
            if ((len(dSM)==1)):
                self.minutes = int(dSM[0])
            
            else:
                if ((len(dSM[1])==1)):
                    self.minutes = splitMinute
                else:
                    raise ValueError("Minute must have only one decimal place") 
        if (splitMinute > 60):
            #print splitDegree, "x"
            #print splitMinute, "y"
            newSplitDegree = int(splitDegree) + (int(splitMinute)/60)
            #splitDegree = int(splitDegree)
            newSplitMinute = int(splitMinute)-60
            self.degrees = newSplitDegree
            self.minutes = newSplitMinute
            #print self.degrees, "a"
            #print self.minutes, "b"
            
        else:
            self.minutes = float(splitMinute)
            self.degrees = splitDegree
            #print self.minutes, "selfminutes"
            #print self.degrees, "selfdegrees"
            
        if (splitMinute < 0):
            raise ValueError("Minutes must be positive")
        
        if (splitMinute >= 1 and carryOver < 0):
            self.minutes = 60 - splitMinute
            self.degrees = self.degrees- splitMinute
            self.degrees = int(self.degrees)
            print self.degrees,"aa"

        print self.degrees
        print self.minutes
        return (self.degrees + self.minutes)
    
    def add(self, angleAdd):
        originalDegree = self.degrees
        print originalDegree, "aa"
        originalMinute = self.minutes
        print originalMinute, "bb"
        
        self.setDegreesAndMinutes(angleAdd)
        degreeX = self.degrees
        minutesX = self.minutes
        print degreeX, "a"
        print minutesX, "b"
        
        newDegree = originalDegree + degreeX
        newMinute = originalMinute + minutesX
        
        if (newDegree>360):
                newDegree = newDegree%360
                self.degrees = newDegree
        else:
            self.degrees = newDegree
        
        if (newMinute > 60):
            #print splitDegree, "x"
            #print splitMinute, "y"
            newDeg = int(newDegree) + (int(newMinute)/60)
            #splitDegree = int(splitDegree)
            newMin = int(newMinute)-60
            self.degrees = newDeg
            self.minutes = newMin
            #print self.degrees
            #print self.minutes
        
        elif (newMinute < 0):
                raise ValueError("Minutes must be positive")    
        else:
            self.minutes = int(newMinute)
        
        print self.degrees
        print self.minutes
        return self
        
    def subtract(self, angleSubtract):
        originalDegree = self.degrees
        print self.degrees, "original"
        originalMinute = self.minutes
        print self.minutes , "orig"
        
        self.setDegreesAndMinutes(angleSubtract)
        degreeX = self.degrees
        print degreeX
        minutesX = self.minutes
        print minutesX
        
        newDegree = originalDegree - degreeX
        print newDegree
        newMinute = originalMinute - minutesX
        print newMinute
        
        if (newDegree>360):
            newDegrees = newDegree%360
            #print newDegrees
        
        elif (newDegree<0):
            newDegrees = abs(newDegree + 360)
            self.degrees = newDegrees
            #print self.degrees
        
        else:
            self.degrees = newDegree
            #print self.degrees
           
        if (newMinute > 60):
            newDeg = int(newDegree) + (int(newMinute)/60)
            #splitDegree = int(splitDegree)
            newMin = int(newMinute)-60
            self.degrees = newDeg
            self.minutes = newMin
            #print self.degrees
            #print self.minutes
        
        elif (newMinute<0): 
            #print "Minutes must be positive"
            self.degrees = originalDegree
            self.minutes = originalMinute
            print self.degrees
            print self.minutes
            raise ValueError ("Minutes must be positive")
            
        else:
            self.minutes = int(newMinute)
        
        print self.degrees
        print self.minutes
        return self
        
    def compare(self, angleCompare):
        originalDegree = self.degrees
        print originalDegree
        originalMinute = self.minutes
        print originalMinute
        
        a = -1
        b = 1
        c = 0
        
        self.setDegreesAndMinutes(angleCompare)
        degreeX = self.degrees
        print degreeX
        minutesX = self.minutes
        print minutesX
         
        if (degreeX < originalDegree):
            print a
            return a
        
        if (degreeX > originalDegree):
            print b 
            return b
        
        if(degreeX == originalDegree):
            
            if minutesX < originalMinute:
                print a 
                return a
            
            elif minutesX > originalMinute:
                print b 
                return b
            
            elif minutesX == originalMinute:
                print c
                return c        
     
    def getString(self):
        #self.degrees = 700
        degree = self.degrees
        #print degree
        
        if (degree>360):
            newDegrees = degree%360
            self.degrees = newDegrees
            #print self.degrees
        
        elif (degree<0):
            newDegrees = abs(degree + 360)
            self.degrees = newDegrees
            #print self.degrees
            #print self.degrees
        
        else:
            self.degrees = degree
            #print self.degrees
        
        self.minutes = 50
        minutes = self.minutes
        #print minutes
        
        if (minutes > 60):
            #print splitDegree, "x"
            #print splitMinute, "y"
            newDeg = int(self.degrees) + (int(minutes)/60)
            #splitDegree = int(splitDegree)
            newMin = int(minutes)-60
            self.degrees = newDeg
            self.minutes = newMin
            #print self.degrees
            #print self.minutes
        
        elif (minutes < 0):
                raise ValueError("Minutes must be positive")    
        else:
            self.minutes = int(minutes)
            
        self.newString = "%dd%.1f" % (self.degrees,self.minutes)
        print self.newString
        return self.newString
    
    def getDegrees(self):
        
        #self.degrees = 700
        degree = self.degrees
        #print degree
        
        if (degree>360):
            newDegrees = degree%360
            self.degrees = newDegrees
            #print self.degrees
        
        elif (degree<0):
            newDegrees = abs(degree + 360)
            self.degrees = newDegrees
            #print self.degrees
            #print self.degrees
        
        else:
            self.degrees = degree
            #print self.degrees
        
        #self.minutes = 40
        minutes = self.minutes
        #print minutes
        
        if (minutes > 60):
            #print splitDegree, "x"
            #print splitMinute, "y"
            newDeg = int(self.degrees) + (int(minutes)/60)
            #splitDegree = int(splitDegree)
            newMin = int(minutes)-60
            self.degrees = newDeg
            self.minutes = newMin
            #print self.degrees
            #print self.minutes
        
        elif (minutes < 0):
                raise ValueError("Minutes must be positive")    
        else:
            self.minutes = int(minutes)
        
        minutes = (float)("%.1f" % self.minutes)
        print minutes
        #print self.degrees 
        #print self.minutes
        
        selfminute = minutes/60
        print selfminute
        tenthMinute = round(selfminute, 1)
        print tenthMinute
        exampleVar = self.degrees + tenthMinute 
    
        self.newString =  ("%.1f" % exampleVar)
        print self.newString
        return self

    
    
    