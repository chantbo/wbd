import Navigation.prod.Fix as Fix

myFix = Fix.Fix()

x = myFix.__init__("log.txt")

x = myFix.setSightingFile("sightingFile.xml")
print x

