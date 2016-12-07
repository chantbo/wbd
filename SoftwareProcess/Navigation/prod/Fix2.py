from datetime import datetime, timedelta
from xml.dom import minidom
import math
from decimal import *
import Angle
from math import tan, sqrt, pi, sin
import os

class Fix():
    def __init__(self, logFile = "logFile.txt"):
        try:
            self.logFile = logFile
            self.sightingFile = None
            self.strOfSightingFile = None
            self.starDict = None
            self.ariesDict = None
            self.fileAries = None
            self.fileStar = None
            f = open(self.logFile, "a")
            f.write(self.currentDateTime() + "Log file:\t" + os.path.abspath(self.logFile) + "\n")
        except:
            raise ValueError("Fix.__init__: The file is incorrect")    
        
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
           
    def setSightingFile(self, sightingFile = None):
        #check for instance as string
        if(isinstance(sightingFile, basestring)):
            if(sightingFile == None):
                raise ValueError("Fix.setSightingFile: The file is incorrect")                    
            #check in sightingfile to find period
            periodCheck = sightingFile.find(".")
            if(periodCheck != -1):
                enteredFileType = sightingFile[periodCheck + 1: len(sightingFile)]
                if(enteredFileType != "xml"):
                    raise ValueError("Fix.setSightingFile: The file is incorrect")                    
            else:
                raise ValueError("Fix.setSightingFile: The file is incorrect")                    
            
            try:
                #append to logFile
                self.sightingFile = sightingFile
                f = open(self.logFile, "a")
                f.write(self.currentDateTime() + "Sighting file:\t" + os.path.abspath(self.sightingFile) + "\n")
                
                #read through sightingFile and obtain values
                s = open(sightingFile, "r")
                self.unedittedString = s.read()
                self.strOfSightingFile = self.unedittedString.translate(None, "\t")
                s.close()
                return os.path.abspath(self.sightingFile)
            except:    
                raise ValueError("Fix.setSightingFile: The file is incorrect")                    
        else:
            raise ValueError("Fix.setSightingFile: The file is incorrect")                    
             
    def setAriesFile(self, ariesFile = None):
        #check for none ariesFile
        if(ariesFile == None):
            raise ValueError("Fix.setAriesFile: The file is incorrect")
        #check for type ariesFile                    
        if(isinstance(ariesFile, basestring)):
            periodCheck = ariesFile.find(".")
            #check for period
            if(periodCheck != -1):
                enteredFileType = ariesFile[periodCheck + 1: len(ariesFile)]
                if(enteredFileType != "txt"):
                    raise ValueError("Fix.setAriesFile: The file is incorrect")                    
            else:
                raise ValueError("Fix.setAriesFile: Incorrect file")                    
            
            try:
                #append to logfile
                self.fileAries = ariesFile
                f = open(self.logFile, "a")
                f.write(self.currentDateTime() + "Aries file:\t" + os.path.abspath(self.fileAries) + "\n")
                
                #read through ariesFile and obtain values
                dictionaryForAries = {}
                with open(ariesFile) as af:
                    for line in af:
                        entry = line.split("\t", 1)
                        date = entry[0]
                        values = entry[1].split()
                        if date in dictionaryForAries:
                            dictionaryForAries[date].append(values)
                        else:
                            dictionaryForAries[date] = [values]
                        
                self.ariesDict = dictionaryForAries
                return os.path.abspath(self.fileAries)
            except:    
                raise ValueError("Fix.setAriesFile: Incorrect file")                    
        else:
            raise ValueError("Fix.setAriesFile: Incorrect file")
    
    def setStarFile(self, starFile = None):
        #check for none parameter
        if(starFile == None):
            raise ValueError("Fix.setStarFile: Incorrect file")
        #check for type starFile                    
        if(isinstance(starFile, basestring)):
            checkForPeriod = starFile.find(".")
            #check for period
            if(checkForPeriod != -1):
                enteredFileType = starFile[checkForPeriod + 1: len(starFile)]
                if(enteredFileType != "txt"):
                    raise ValueError("Fix.setStarFile: Incorrect file")                    
            else:
                raise ValueError("Fix.setStarFile: Incorrect file")                    
            
            try:
                #append to logfile
                self.fileStar = starFile
                f = open(self.logFile, "a")
                f.write(self.currentDateTime() + "Star file:\t" + os.path.abspath(self.fileStar) + "\n")
                
                #read through starFile and obtain values
                dictionaryForStar = {}
                with open(starFile) as sf:
                    for line in sf:
                        entry = line.split("\t", 1)
                        star = entry[0]
                        values = entry[1].split()
                        if star in dictionaryForStar:
                            dictionaryForStar[star].append(values)
                        else:
                            dictionaryForStar[star] = [values]
                        
                self.starDict = dictionaryForStar
                return os.path.abspath(self.fileStar)
            except:    
                raise ValueError("Fix.setStarFile: Incorrect file")        
        else:
            raise ValueError("Fix.setStarFile: Incorrect file")
    
            
    def getAngleInfo(self):
        # retrieve the values needed for requirements and compute for GHA
        dateOfSighting = self.date
        dateConverted = self.dateNeededForGHA
        dateConverted = datetime.strptime(dateConverted,"%Y-%m-%d").strftime("%m/%d/%y")
        dateConverted = datetime.strptime(dateConverted,"%m/%d/%y")
        ariesDate = datetime.strptime(dateOfSighting, "%Y-%m-%d").strftime("%m/%d/%y")
        sightingBody = self.body
        timeArray = self.time.split(":") 
        hourNeeded = int(timeArray[0])
        s = int(timeArray[1]) * 60 + int(timeArray[2])
        starDictionary = self.starDict
        ariesDictionary = self.ariesDict
        starIndex = 0
        geoPosLatAngle = Angle.Angle()
        geoPosLonAngle = Angle.Angle()
        starSarHourAngle = Angle.Angle()
        ariesGHA2Angle = Angle.Angle()
        ariesGHA1Angle = Angle.Angle()
        ariesGHA = Angle.Angle()
        
        for star in starDictionary[sightingBody]:
            checkDate = datetime.strptime(star[0], "%m/%d/%y")
            if (checkDate == dateConverted):
                observedStar = starDictionary[sightingBody][starIndex]
                break
            elif (checkDate > dateConverted):
                observedStar = starDictionary[sightingBody][starIndex - 1]
                break
        

        
        geographicPositionLatitude = observedStar[2]
        geoPosLatAngle.setDegreesAndMinutes(geographicPositionLatitude)
        starSHA = observedStar[1]
        returnedSHA = observedStar[2]
        returnedSHAANlge = Angle.Angle()
        returnedSHAANlge.setDegreesAndMinutes(returnedSHA)
        starSarHourAngle.setDegreesAndMinutes(starSHA)
        
        dateList = ariesDictionary[ariesDate]
        aries1GHA = dateList[hourNeeded][1]
        
        if (hourNeeded == 23):
            ariesDate = datetime.strptime(ariesDate, "%m/%d/%y")
            ariesDate += timedelta(days=1)
            ariesDate = datetime.strftime(ariesDate, "%m/%d/%y")
            dateList = ariesDictionary[ariesDate]
            aries2GHA = dateList[0][1]
        else:
            aries2GHA = dateList[hourNeeded + 1][1]

        ariesGHA1Angle.setDegreesAndMinutes(aries1GHA)
        ariesGHA2Angle.setDegreesAndMinutes(aries2GHA)
        part1 = float(ariesGHA1Angle.angle)
        part2 = float(ariesGHA2Angle.angle)

        computeFormula = abs(part2 - part1)
        computeFormula = float(computeFormula) * s/3600
        ariesGHA.setDegrees(computeFormula)
        ariesGHA.add(ariesGHA1Angle)
        
        ariesGHA.add(starSarHourAngle)
        
        
        
        geoPosLonAngle.setDegrees((ariesGHA.angle) % 360)
        self.latitude = returnedSHAANlge.getDegrees()
        self.longitude = geoPosLonAngle.getDegrees()
        return (returnedSHA, geoPosLonAngle)
        
            
    def getSightings(self, assumedLatitude = "0d0.0", assumedLongitude = "0d0.0"):
        if(self.strOfSightingFile == None):
            raise ValueError("Fix.getSightings: Sighting file not set")
        if(self.ariesDict == None):
            raise ValueError("Fix.getSightings: Aries file not set")
        if(self.starDict == None):
            raise ValueError("Fix.getSightings: Star file not set")
        if(not(isinstance(assumedLatitude, basestring))):
            raise ValueError("Fix.getSightings: Latitude is not string")
        if(not(isinstance(assumedLongitude, basestring))):
            raise ValueError("Fix.getSightings: Longitude is not string")
        try:
            checkStrLat = assumedLatitude.split("d")
            if (float(checkStrLat[1]) < 0.0):
                raise ValueError("Fix.getSightings: Incorrect Parameter")
    
            decimalCheck = abs(Decimal(checkStrLat[1]).as_tuple().exponent)
            if (decimalCheck > 1):
                raise ValueError("Fix.getSightings: Incorrect Parameter")
            
            checkStrLon = assumedLongitude.split("d")
            if (float(checkStrLon[1]) < 0.0):
                raise ValueError("Fix.getSightings: Incorrect Parameter")
    
            decimalCheck = abs(Decimal(checkStrLon[1]).as_tuple().exponent)
            if (decimalCheck > 1):
                raise ValueError("Fix.getSightings: Incorrect Parameter")
        except:
            raise ValueError("Fix.getSightings: Incorrect Parameter")
        
        checkForLatN = assumedLatitude.find("N")
        checkForLatS = assumedLatitude.find("S")
        if (checkForLatN == -1):
            if (checkForLatS == -1):
                assumedLatitude = "0d0.0"
            else:
                assumedLatitude = "-" + assumedLatitude[1:]
        else:
            assumedLatitude = assumedLatitude[1:]
            
        #establish variables
        self.errorCount = 0
        self.totalErrorCount = 0
        self.sumCosAzimuth = 0
        self.sumSinAzimuth = 0
        self.sumDistance = 0
        self.multCosVar = 0
        self.multSinVar = 0
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        sightingList = xmlDocument.getElementsByTagName('sighting')
        amount = len(sightingList)
        usedAngle = Angle.Angle()
        f = open(self.logFile, "a")
        for i in range(0, amount):
            self.dateNeededForGHA = None
            #pull from XMLParsedData class for information
            XMLParsedData.getBody(i)
            XMLParsedData.getDate(i)
            XMLParsedData.getHeight(i)
            XMLParsedData.getHorizon(i)
            XMLParsedData.getObservation(i)
            XMLParsedData.getPressure(i)
            XMLParsedData.getTemp(i)
            XMLParsedData.getTime(i)
            observedAltitude = usedAngle.setDegreesAndMinutes(self.observation)
            if(self.errorCount == 0):
                #calculate for natural
                if(self.horizon.lower() == "natural"):
                    self.dip = float((-0.97 * sqrt(float(self.numericHeight))) / 60.0)
                else:
                    self.dip = 0.0
                self.refraction = (-0.00452 * self.intPressure) / (273 + (.5556 * (self.intTemperature - 32))) / tan(observedAltitude * pi/180)
                self.adjustedAltitude = round(observedAltitude + self.dip + self.refraction, 3)
                usedAngle.angle = self.adjustedAltitude
                (lat, lon) = self.getAngleInfo()

                assumedLonAngle = Angle.Angle()
                assumedLatAngle = Angle.Angle()
                assumedLatAngle.setDegreesAndMinutes(assumedLatitude)
                assumedLonAngle.setDegreesAndMinutes(assumedLongitude)
                
                LHA = self.longitude - assumedLonAngle.getDegrees()
                
                correctedAltitude = math.asin((math.sin(self.latitude) * math.sin(assumedLatAngle.getDegrees()))) + (math.cos(self.latitude) * math.cos(assumedLatAngle.getDegrees()) * math.cos(LHA))
                distanceAdjustment = round(usedAngle.getDegrees() - correctedAltitude, 1)
                azimuthAdjustment = math.acos(math.sin(self.latitude) - math.sin(assumedLatAngle.getDegrees()) * (math.cos(assumedLatAngle.getDegrees()) * math.cos(distanceAdjustment)))
                self.sumDistance += distanceAdjustment
                self.sumCosAzimuth += math.cos(azimuthAdjustment)
                self.sumSinAzimuth += math.sin(azimuthAdjustment)
                self.multCosVar += self.sumDistance * self.sumCosAzimuth 
                self.multSinVar += self.sumDistance * self.sumSinAzimuth
                
                f.write(self.currentDateTime() + self.body + "\t" + self.date + "\t" + self.time + "\t" + usedAngle.getString() + "\t" + str(lat) + "\t" + str(lon.getString()) + "\t" + str(assumedLatitude) + "\t" + str(assumedLongitude) + "\t" + str(azimuthAdjustment) + "\t" + str(round(distanceAdjustment), 1) +"\n")

            else:
                self.totalErrorCount += 1
                self.errorCount = 0
            
        f.write(self.currentDateTime() + "Sighting errors:\t" + str(self.totalErrorCount) + "\n")
        
        latDegrees = assumedLatAngle.getDegrees()    
        degreesLatitude = latDegrees + (self.multCosVar / 60)
        assumedLatAngle.setDegrees(degreesLatitude)
        approximateLatitude = assumedLatAngle.getString()
        
        lonDegrees = assumedLonAngle.getDegrees()    
        degreesLongitude = lonDegrees + (self.multSinVar / 60)
        assumedLonAngle.setDegrees(degreesLongitude)
        approximateLongitude = assumedLonAngle.getString()
        
        f.write(self.currentDateTime() + "Approximate latitude:\t" + approximateLatitude + "\t" + "Approximate Longitude:\t" + approximateLongitude)
        f.close()
        return (approximateLatitude, approximateLongitude)
        
    
class XMLParsedData():
    #get info from body
    def getBody(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        bodyList = xmlDocument.getElementsByTagName('body')
        if(len(bodyList) == 0):
            self.errorCount += 1
            
        try:
            self.body = bodyList[count].firstChild.nodeValue
            return self.body
        except:
            self.errorCount += 1
    
    #get info from Date
    def getDate(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        dateList = xmlDocument.getElementsByTagName('date')
        self.date = dateList[count].firstChild.nodeValue
        try:
            self.dateNeededForGHA = self.date
            datetime.strptime(self.date, "%Y-%m-%d")
            return self.date
        except:
            self.errorCount += 1
            
    #get info from Time       
    def getTime(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        timeList = xmlDocument.getElementsByTagName('time')
        self.time = timeList[count].firstChild.nodeValue
        try:
            datetime.strptime(self.time, "%H:%M:%S")
            return self.time
        except:
            self.errorCount += 1
        
    #get info from Observation    
    def getObservation(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        observationList = xmlDocument.getElementsByTagName('observation')
        self.observation = observationList[count].firstChild.nodeValue
        strDelimiter = self.observation.find("d")
        if(strDelimiter == -1):
            self.errorCount += 1
        else:
            return self.observation
    
    #get info from Height    
    def getHeight(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        heightList = xmlDocument.getElementsByTagName('height')
        if(len(heightList) == 0):
            self.numericHeight = 0.0
            return self.numericHeight
        
        self.height = heightList[count].firstChild.nodeValue        
        try:
            self.numericHeight = float(self.height)
            if(self.numericHeight <= 0):
                self.errorCount += 1
            else:    
                return self.numericHeight
        except:
            self.errorCount += 1
    
    #get info from Temp        
    def getTemp(self, count):
            xmlDocument = minidom.parseString(self.strOfSightingFile)
            tempList = xmlDocument.getElementsByTagName('temperature')
            if(len(tempList) == 0):
                self.intTemperature = 72
                return self.intTemperature
            
            self.temp = tempList[count].firstChild.nodeValue
            self.intTemperature = int(self.temp)
            if(self.intTemperature <= -20):
                self.errorCount += 1
            elif(self.intTemperature >= 120):
                self.errorCount += 1
            else:
                return self.intTemperature
    
    #get info from Pressure       
    def getPressure(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        pressureList = xmlDocument.getElementsByTagName('pressure')
        if(len(pressureList) == 0):
            self.intPressure = 1010
            return self.intPressure
            
        self.pressure = pressureList[count].firstChild.nodeValue
        checkForPeriod = self.pressure.find(".")
        if(checkForPeriod != -1):
            self.errorCount += 1
        else:
            self.intPressure = int(self.pressure)
            return self.intPressure
    
    #get info from Horizon   
    def getHorizon(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        horizonList = xmlDocument.getElementsByTagName('horizon')
        if(len(horizonList) == 0):
            self.horizon = "natural"
            return self.horizon
        
        self.horizon = horizonList[count].firstChild.nodeValue
        if(self.horizon.lower() == "natural"):
            return self.horizon
        elif(self.horizon.lower() == "artificial"):
            return self.horizon
        else:
            self.errorCount += 1