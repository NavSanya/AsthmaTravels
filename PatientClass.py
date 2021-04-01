#Patient class 
#DegreeOfSensitivity can have 1 to 4 values,i.e. 1=Well, 2=Mild, 3=Moderate, 4=Severe
#AQIsenstivity can have 0 or 1, i.e. 0 = not sensitive and 1 = sensitive
#PollenSensitive can have 0 or 1, i.e. 0 = not sensitive and 1 = sensitive

class Patient:
    def __init__(self,dos,senAQI,senPol ):
        self.degreeOfSenstivity=dos
        self.AQIsensitive=senAQI
        self.PollenSensitive=senPol

    def printAllValues(self):
        print("degree of senstitivity"+degreeOfSenstivity)
        print("Sensitive to AQI"+ AQIsensitive)
        print("Sensitive to Pollen Count"+PollenSensitive)
  