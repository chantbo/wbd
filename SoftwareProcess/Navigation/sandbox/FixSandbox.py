import os
import datetime
import Angle
import xml.dom.minidom as T
import xml.etree.ElementTree as ET
from datetime import datetime
from math import sqrt, tan, degrees, radians
import math



class Fix():

   
    #Parameter is optional and unvalidated
    def __init__(self, logFile = None):
        self.error = 0
        #If no parameter given and/or if it doesn't exist
        if logFile == None:
            #Set logFile attribute
            self.logFile = "log.txt"
            #create the log.txt file
            logFile = open("log.txt", 'w')
            filePath = os.path.abspath(self.logFile)  
            #Write the state change
            logFile.write(self.currentDateTime() + "Log file:\t" + filePath + "\n")
            #Close the file to prevent memory leak
            logFile.close()
        elif not os.path.exists(logFile):
            #Set logFile attribute
            self.logFile = "log.txt"
            #create the log.txt file
            logFile = open("log.txt", 'w')
            filePath = os.path.abspath(self.logFile)  
            #Write the state change
            logFile.write(self.currentDateTime() + "Log file:\t" + filePath + "\n")
            #Close the file to prevent memory leak
            logFile.close()
        #if the parameter is given and the file exists        
        elif os.path.exists(logFile):
            #Set logFile attribute
            self.logFile = logFile
            #Open the file in 'append' mode 
            logFile = open(logFile, 'a')  
            #Write the state change
            filePath = os.path.abspath(self.logFile)
            logFile.write(self.currentDateTime() + "Log file:\t" + filePath + "\n") 
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
            raise ValueError("Fix.setSightingFile: Invalid file extension")
        #If the extension is .xml then:
        elif os.path.exists(sightingFile): #check to see that the file exists
            
            #assign the sighting file path as an attribute for future use
            #self.sightingFile = sightingFile
            #File exists, has valid extension, and meets param specifications
            #As a result return False for old file and write to log.txt
            #Try and Catch on value error
            try:
                logFile = open(self.logFile, 'a')
                self.sightingFile = os.path.abspath(sightingFile)
                logFile.write(self.currentDateTime() + "Sighting file:" + "\t" + self.sightingFile + '\n')
                logFile.close()
            except:
                raise ValueError("Fix.setSightingFile: File cannot be opened.") 
            #--------------------#
            
            return self.sightingFile    
        else:
            #File doesn't exist, return True and write to log.txt
            logFile = open(self.logFile, 'a')
            self.sightingFile = os.path.abspath(sightingFile)
            logFile.write(self.currentDateTime() + "Sighting file:" + "\t" + self.sightingFile + '\n')
            #logFile.close()
    #No parameters
    def setAriesFile(self, ariesFile):
        #If the extension of sightingFile is NOT .txt....
        if not ariesFile.endswith('.txt'):
            #...raise a ValueError
            raise ValueError("Fix.setAriesFile: Invalid file extension")
        #If the extension is .xml then:
        elif os.path.exists(ariesFile): #check to see that the file exists
            self.ariesFile = os.path.abspath(ariesFile)
            try:
                logFile = open(self.logFile, 'a')
                logFile.write(self.currentDateTime() + "Aries file:" + "\t" + self.ariesFile + "\n")
                logFile.close()
            except:
                raise ValueError("Fix.setAriesFile: File cannot be opened.") 
           
            return self.ariesFile
        
    def setStarFile(self, starFile):
        #If the extension of sightingFile is NOT .txt....
        if not starFile.endswith('.txt'):
            #...raise a ValueError
            raise ValueError("Fix.setStarFile: Invalid file extension")
        #If the extension is .xml then:
        elif os.path.exists(starFile): #check to see that the file exists
            self.starFile = os.path.abspath(starFile)
            try:
                logFile = open(self.logFile, 'a')
                logFile.write(self.currentDateTime() + "Star file:" + "\t" + self.starFile + "\n")
                logFile.close()
            except:
                raise ValueError("Fix.setStarFile: File cannot be opened.") 
           
            return self.starFile
    
       
    def getSightings(self):
        approximateLatitude = "0d0.0"            
        approximateLongitude = "0d0.0"
        List = []
        LatLong = (approximateLatitude,approximateLongitude)
        ############
        sightingsFile = T.parse (self.sightingFile).documentElement.getElementsByTagName("sighting")
        #Which will check the root of the file(which should be 'fix' tag
        root = ET.parse(self.sightingFile).getroot()
        Tag=root.tag
        self.errorString = ""
        try:
            if(Tag=='fix'):
                # sightingsNum used to know about which sighting we are in
                sighting=1
                for i in sightingsFile:
                    Dictionary = {}
                    # Which searching body tag where sighting=sighting
                    try:
                        body = i.getElementsByTagName('body')[0]
                        stringBody = body.childNodes[0].data
                        self.body = stringBody
                    except:
                        self.error += 1
                        self.errorString += "body tag is missing"+str(sighting) + "\n"
                        continue
                    # Which searching date tag where sighting=sightingsNum
                    try:
                        date = i.getElementsByTagName('date')[0]
                        stringDate=date.childNodes[0].data
                        self.date=stringDate
                    except:
                        self.error += 1
                        self.errorString += "date tag is missing"+str(sighting) + "\n"
                        continue
                    # Which searching time tag where sighting=sightingsNum
                    try:
                        time = i.getElementsByTagName('time')[0]
                        stringTime = time.childNodes[0].data
                        self.time = stringTime
                    except:
                        self.error += 1
                        # raise ValueError("time tag is missing in sighting-"+str(sightingsNum))
                        self.errorString += "time tag is missing"+str(sighting) + "\n"
                        continue
                    # Which searching observation tag where sighting=sightingsNum
                    try:
                        observation = i.getElementsByTagName('observation')[0]
                        x = observation.childNodes[0].data
                        DegreeMin = x
                        splitAnglestring = x.split("d")
                        degrees = int(splitAnglestring[0])
                        Minutes = float(splitAnglestring[1])
                        angle1 = Angle.Angle()
                        angle1.setDegreesAndMinutes(DegreeMin)
                        observedAltitude = angle1.degrees + (angle1.minutes / 60) % 360
                    except Exception as e:
                        print e
                        self.error += 1
                        self.errorString += "observation tag is missing"+str(sighting) + "\n"
                        continue

                    # Here we are checking the observedAltitude valid or not(in the range or not)
                    if(0 <= degrees < 90):
                        self.degrees=degrees
                    else:
                        self.error += 1
                        self.errorString += "invalid observation altitude"+str(sighting) + "\n"
                        continue
                    if(0 <= Minutes < 60):
                        self.Minutes=Minutes
                    else:
                        self.error += 1
                        self.errorString += "invalid observation altitude"+str(sighting) + "\n"
                        continue

                    if(degrees == 0):
                        if(Minutes<0.1):
                            self.error += 1
                            self.errorString += "invalid observation altitude"+str(sighting) + "\n"

                    
                    try:
                        height = i.getElementsByTagName('height')[0]
                        stringHeight=height.childNodes[0].data
                        self.height=stringHeight
                    except:
                        self.height=0.0
                        continue

                    # Which searching temperature tag where sighting=sightingsNum
                    try:
                        temperature = i.getElementsByTagName('temperature')[0]
                        stringTemp=temperature.childNodes[0].data
                        if(-20<=int(stringTemp)<=120):
                            self.temperature=stringTemp
                        else:
                            self.temperature=72
                    except:
                        self.temperature=72
                        continue

                    # Which searching pressure tag where sighting=sightingsNum
                    try:
                        pressure = i.getElementsByTagName('pressure')[0]
                        stringPressure=pressure.childNodes[0].data
                        if(100<=int(stringPressure)<1100):
                            self.pressure=stringPressure
                        else:
                            self.pressure=1010
                    except:
                        self.pressure=1010
                        continue
                    # Which searching horizon tag where sighting=sightingsNum
                    try:
                        horizon = i.getElementsByTagName('horizon')[0]
                        x=horizon.childNodes[0].data
                        self.horizon = x
                    except:
                        self.horizon = 'Natural'
                        continue
                    if(self.horizon == "Natural"):
                        dip = (-0.97 * math.sqrt(float(self.height ))) / 60
                    else:
                        dip = 0

                    # calculate refraction using pressure, temperature and oberservedAltitude.
                    try:
                        refraction = (-0.00452 * float(self.pressure)) / (273 + ((float((self.temperature))-32)*5)/9) / tan(radians(observedAltitude))

                        # calculate adjusted Altitude.
                        adjustedAltitude = observedAltitude + dip + refraction
                        angle1.setDegrees(adjustedAltitude)
                        adjustedAltitudestring=angle1.getString()
                        # split time where received from sighting file and set hours, minutes and seconds.
                        hours = self.time.split(":")[0]
                        minutes = self.time.split(":")[1]
                        sec = self.time.split(":")[2]
                        # convert minutes in seconds
                        s = (int(minutes) * 60) + int(sec)

                        # converted sighting file date into aries file and star file date format.
                        formatedDate = datetime.strptime(self.date, '%Y-%m-%d').strftime('%m/%d/%y')
                        # open stars file in read mode.
                        starData = open(self.starFile, "r")
                        # use this flag while some tags are missing in sighting file.
                        bodyFlag = False
                        # create new Angle instance.
                        angle = Angle.Angle()
                        # read line from star file.
                    except:
                        self.error += 1
                        continue
                    for line in starData:
                        # split line and take first element as name.
                        name = line.split("\t")[0]
                        # split line and take first element as date.
                        tempDt = line.split("\t")[1]
                        # searching in stars file.
                        if name == self.body and tempDt == formatedDate:
                            # if name and date match than set variable by slit line and take third element.
                            self.SHAstar = angle.setDegreesAndMinutes(line.split("\t")[2])
                            # split line and take forth element and set latitude.
                            self.latitude = (line.split("\t")[3]).strip()
                            bodyFlag = True
                    # close stars file.
                    starData.close()
                    # if name and date not found in stars file than return.
                    if(not bodyFlag):
                        self.error += 1
                        continue
                    # open aries file in read mode.
                    ariesData = open(self.ariesFile, "r")
                    # create a new instance of angle.
                    self.firstAngle = Angle.Angle()
                    self.secondAngle = Angle.Angle()
                    # read line form aries file.
                    for line in ariesData:
                        # split line and use first element as date
                        tempD = line.split("\t")[0]
                        # split line and use second element as hours
                        tempH = line.split("\t")[1]
                        # split line and use third element as observation.
                        obj = line.split("\t")[2]
                        # convert hour to integer.
                        hours = int(hours)
                        tempH = int(tempH)
                        # match sighting file data and hours to aries file data.
                        if tempD == formatedDate and tempH == hours:
                            # set return value of setDegreesAndMinutes method to variable.
                            self.GHAaries1 = self.firstAngle.setDegreesAndMinutes(obj)
                            # read next line and split line, use third element as next observation.
                            nextObservation = next(ariesData).split("\t")[2]
                            # set return value of setDegreesAndMinutes method to variable.
                            self.GHAaries2 = self.secondAngle.setDegreesAndMinutes(nextObservation)
                    # close aries file.
                    ariesData.close()
                    # calculate GHAaries.
                    self.GHAaries = self.GHAaries1 + (self.GHAaries2 - self.GHAaries1) * float(s)/3600
                    # calculate GHAobservation.
                    self.GHAobservation = self.GHAaries + self.SHAstar

                    # pass GHAobservation as degrees to setDegrees method.
                    angle.setDegrees(self.GHAobservation)
                    # set return value of getString method to GHAobservation.
                    self.GHAobservation = angle.getString()

                    # populate data in dictionary
                    Dictionary["body"] = self.body
                    Dictionary["date"] = self.date
                    Dictionary["time"] = self.time
                    Dictionary["adjustedAltitude"] = adjustedAltitudestring
                    Dictionary["latitude"] = self.latitude
                    Dictionary["longitude"] = self.GHAobservation
                    Dictionary["datetime"] = datetime.strptime(self.date + " " + self.time, "%Y-%m-%d %H:%M:%S")
                    # add dictionary in list
                    List.append(Dictionary)
            # sort data by body and datetime
                List.sort(key=lambda k: k['body'])
                List.sort(key=lambda k: k['datetime'])

                for dictionaries in List:
                    print dictionaries
                    # write log entry to log file.
                    logFile = open(self.logFile, 'a')
                    logFile.write((self.currentDateTime() + dictionaries["body"] + "\t" + dictionaries["date"] + "\t" + dictionaries["time"] + "\t" + dictionaries["adjustedAltitude"] + "\t" + dictionaries["latitude"] + "\t" + dictionaries["longitude"] + "\n"))
                    logFile.close()
                sighting=sighting+1
                if(sighting==1):
                    raise ValueError("No sightings found")
                logFile = open(self.logFile, 'a')
                logFile.write(self.currentDateTime() + " Sighting errors:" + "\t" + str(self.error) + "\n")
                logFile.close()
            else:
                raise ValueError("Invalid file")
            # return approximateLatitude and approximateLongitude
            return LatLong

        except:
            print self.errorString
            # write to logfile.
            logFile = open(self.logFile, 'a')
            logFile.write(self.currentDateTime() + " Sighting errors:" + "\t" + str(self.error) + "\n")
            logFile.close()