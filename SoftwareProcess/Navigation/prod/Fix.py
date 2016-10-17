import os
import datetime
import xml.etree.ElementTree as ET
from datetime import datetime
from math import sqrt
import math
import Navigation.prod.Angle as Angle

class Fix():

   
    #Parameter is optional and unvalidated
    def __init__(self, logFile = None):
        #If no parameter given and/or if it doesn't exist
        if logFile == None or not os.path.exists(logFile):
            #Set logFile attribute
            self.logFile = "log.txt"
            #create the log.txt file
            logFile = open("log.txt", 'w')  
            #Write the state change
            logFile.write(self.currentDateTime() + "Start of log\n")
            #Close the file to prevent memory leak
            logFile.close()
        #if the parameter is given and the file exists        
        elif os.path.exists(logFile):
            #Set logFile attribute
            self.logFile = logFile
            #Open the file in 'append' mode 
            logFile = open(logFile, 'a')  
            #Write the state change
            logFile.write(self.currentDateTime() + "Start of log\n") 
            #Close file to prevent memory leak 
            logFile.close()  

    #gets current Date, time, and utc offset for logging purposes
    def currentDateTime(self):
        #Get curent local time
        now = datetime.now()
        #Gets current UTC time
        utcNow = datetime.utcnow()
        #Formats current UTC time
        currentTime = utcNow.strftime("%Y-%m-%d %H:%M:%S")
        #Subtracts local time from utc time to get the offset
        utcOffset = str(utcNow - now)
        #By default, the above is going to go all the way to miliseconds
        utcOffset.split(":")
        #Cuts off everything after the minute value
        offset = utcOffset[0] + ":" + utcOffset[2] + utcOffset[3]
        #Combines current UTC time and offset for the timestamp
        logTime = "LOG:\t" + currentTime + "-" + str(offset) + "\t"
        #returns the timestamp
        return logTime
        
    #Parameter is mandatory and unvalidated
    #Method needs to raise exception when an existing file can not be created or appended
    def setSightingFile(self, sightingFile):
        #If the extension of sightingFile is NOT .xml....
        if not sightingFile.endswith('.xml'):
            #...raise a ValueError
                raise ValueError("Invalid file extension")
        #If the extension is .xml then:
        else:
            #check to see that the file exists
            if os.path.exists(sightingFile):
                #assign the sighting file path as an attribute for future use
                #self.sightingFile = sightingFile
                #File exists, has valid extension, and meets param specifications
                #As a result return False for old file and write to log.txt
                #Try and Catch on value error
                try:
                    logFile = open(self.logFile, 'a')
                    logFile.write(self.currentDateTime() + "Start of sighting file " + sightingFile + "\n")
                    logFile.close()
                except:
                    raise ValueError("File cannot be opened.") 
                #--------------------#
                with open (sightingFile, "r") as myfile:
                    xmlFile=myfile.readlines()
                    
                
                    self.sightingFile = ''.join(xmlFile)
                    #print self.sightingFile, "aa"
                    return self.sightingFile
                    
            else:
                #File doesn't exist, return True and write to log.txt
                logFile = open(self.logFile, 'a')
                logFile.write(self.currentDateTime() + sightingFile + " was provided but not found.\n") 
                logFile.close()
                
    def getAltitude(self):
        approximateLatitude = "0d0.0"
        approximateLongitude = "0d0.0"
        return (approximateLatitude,approximateLongitude)
    
    #No parameters
    def getSightings(self):
        #Use the xml.etree.ElementTree built-in library to parse the XML file
        #This module comes with Python - no need to download anything
        sightingFile = ET.fromstring(self.sightingFile)
        #Gets the highest level tag in the XML file
        #In this file, it is the <fix></fix> tag
        #print sightingFile
        #root = sightingFile.getroot()
        
        myList = []
        #For every child tag in <fix>...</fix> that matches the string "sighting"...
        for sighting in sightingFile.iter('sighting'):
            anotherList = []
            #For every child in each <sighting></sighting> tag...
            for child in sighting:
                anotherList.append(child.text)
            myList.append(anotherList)
        print myList
        
    
        for listing in myList:
            print listing[7], "listing"
            if listing[7] == 'Natural':
                dip = (-0.97 * sqrt(float(listing[4]))) / 60
                print dip, "abc"
            else:
                dip = 0
                print dip , "cde"
            press = listing[len(listing)-2]
            print press, "press"
            pressure = int(press) * -0.00452
            print pressure
            temp = listing[len(listing)-3]
            print temp, "temp"
            newTemp = (int(temp)) - 32
            print newTemp, "newTemp"
            temperature = newTemp * 5 / 9
            print temperature,"temperature"
            alt = listing[len(listing)-5]
            print alt, "alt"
            #newAltitude = alt.split("d")
            #degrees = int(newAltitude[0])
            #minutes = float(newAltitude[1])
            myAngle = Angle.Angle()
            alt1 = [(myAngle.setDegreesAndMinutes(alt))]
            print alt1, "alt1"
            
            alt2 = float(math.tan(alt1))
            print alt2, "alt2"
            
            refrac = (pressure) / (273 + temperature) / (math.tan(altitude))
            refraction = float(refrac)
            adjustedAltitude = altitude + dip + refraction
            print adjustedAltitude, "aabb"
            
        #if myList[1][len(myList[1])-1] == "Natural":
        #    print "YES"
        
        
        #logFile = open(self.logFile, 'a')
        #for item in myList:
        #    print item
        #    logFile.write("\n" + self.currentDateTime()) 
            #print item[2]
        #    for child in item:
        #        logFile.write(" " + child) 
        #logFile.write("\n" + self.currentDateTime() + "End of sighting file." + "\n")
        #logFile.close()'''

        

myLog = Fix('log.txt')
myLog.setSightingFile('sightingFile.xml')
myLog.getSightings()