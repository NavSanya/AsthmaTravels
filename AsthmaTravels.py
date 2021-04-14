from queue import Queue
from datetime import datetime
import random

places = {1:"San Diego",
    2:"Palm Springs",
    3:"Los Angeles",
    4:"Santa Barbara",
    5:"Bakersfield",
    6:"San Luis Obispo",
    7:"Fresno",
    8:"Monterey",
    9:"San Jose",
    10:"Sacramento",
    11:"Oakland",
    12:"San Fransisco",
    13:"Napa",
    14:"Eureka",
    15:"Redding"}

names = {1:"Sam",
    2:"Alex",
    3:"Steve",
    4:"David",
    5:"John",
    6:"Bill",
    7:"Jose",
    8:"Sarah",
    9:"Mary",
    10:"Julia",
    11:"Victoria",
    12:"Bella",
    13:"Angela",
    14:"Olivia",
    15:"Sophia"}

sens = {1:"Minor",
    2:"Mild",
    3:"Moderate",
    4:"Severe"}

class Patient:
    def __init__(self,dos,senAQI,senPol,name):
        self.name = name
        self.degreeOfSensitivity=dos
        self.AQIsensitive=senAQI
        self.PollenSensitive=senPol

    def printAllValues(self):
        print("degree of senstitivity"+degreeOfSenstivity)
        print("Sensitive to AQI"+ AQIsensitive)
        print("Sensitive to Pollen Count"+PollenSensitive)
    
class Graph:
    def __init__(self):
        random.seed()
        self.G={"San Diego":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Palm Springs":133,"Los Angeles":120},
           "Palm Springs":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Los Angeles":107, "San Diego":133},
           "Los Angeles":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Santa Barbara":96, "Bakersfield":112, "San Diego":120},
           "Santa Barbara":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"San Luis Obispo":95, "Los Angeles":96},
           "Bakersfield":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Fresno":109, "Los Angeles":112},
           "San Luis Obispo":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Monterey":141, "San Jose":185, "Santa Barbara":95},
           "Fresno":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Sacramento":169,"Bakersfield":109},
           "Monterey":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"San Jose":73, "San Luis Obispo":141},
           "San Jose":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Oakland":41, "San Fransisco":48, "Monterey":73, "San Luis Obispo":185},
           "Sacramento":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Napa":62, "Redding":160, "Fresno":169},
           "Oakland":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Napa":42, "San Jose":41},
           "San Fransisco":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Napa":52, "San Jose":48},
           "Napa":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Eureka":252, "Sacramento":62, "Oakland":42, "San Fransisco":52},
           "Eureka":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Redding":147, "Napa":252},
           "Redding":{"AQI":random.randrange(0, 350),"Pollen":random.randrange(0, 100) / 10,"Eureka":147, "Sacramento":160}}

#runs program with random inputs for locations and patient info
def test():
    #Setup some random values
    random.seed()
    person = Patient(random.randrange(1,4), False, True, names[random.randrange(1,15)])
    g = Graph()
    start = places[random.randrange(1, 15)]
    end = places[random.randrange(1, 15)]
    while end == start:
        end = places[random.randrange(1, 15)]
    path = search(person, g.G, start, end)

    #Give feedback about what's been generated and what happened
    print(person.name + " wants to drive from " + start + " to " + end + ". They have a " + sens[person.degreeOfSensitivity] + " sensitivity to allergens.")
    if person.AQIsensitive and person.PollenSensitive:
        print(person.name + " is particularly sensitive to pollen and AQI.")
    elif person.AQIsensitive:
        print(person.name + " is particularly sensitive to AQI.")
    elif person.PollenSensitive:
        print(person.name + " is particularly sensitive to pollen.")
    print("The path they should take to minimize allergen exposure is:")
    print(path)

    #Loop through the cities in the path and give detailed information about air quality
    for city in path:
        safety = airQuality(person, g.G[city]["AQI"], g.G[city]["Pollen"])
        if safety == 0:
            print("The air quality in " + city + " is just fine today.")
        elif safety == -1:
            print("The pollen count in " + city + " is notably high today at a level of " + str(g.G[city]["Pollen"]) + ".")
        elif safety == -2:
            print("The AQI in " + city + " is notably high today at a level of " + str(g.G[city]["AQI"]) + ".")
        elif safety == -3:
            print("The AQI and pollen counts in " + city + " are notably high today at levels of " + str(g.G[city]["AQI"]) + " and " + str(g.G[city]["Pollen"]) + " respectively.")

def search(person, cities, source, dest):
    #Need to keep track of cities visited in later loops
    visited = {"San Diego":False,
       "Palm Springs":False,
       "Los Angeles":False,
       "Santa Barbara":False,
       "Bakersfield":False,
       "San Luis Obispo":False,
       "Fresno":False,
       "Monterey":False,
       "San Jose":False,
       "Sacramento":False,
       "Oakland":False,
       "San Fransisco":False,
       "Napa":False,
       "Eureka":False,
       "Redding":False}

    #Need to keep track of the cost of taking particular paths
    cost = {"San Diego":0,
       "Palm Springs":0,
       "Los Angeles":0,
       "Santa Barbara":0,
       "Bakersfield":0,
       "San Luis Obispo":0,
       "Fresno":0,
       "Monterey":0,
       "San Jose":0,
       "Sacramento":0,
       "Oakland":0,
       "San Fransisco":0,
       "Napa":0,
       "Eureka":0,
       "Redding":0}

    #Initialize a queue to keep track of the cities that need to be processed and costs calculated for
    q = Queue(maxsize = 0)
    q.put(source)
    while not q.empty():
        curCity = q.get()
        for key, value in cities[curCity].items():
            #The degree of sensitivity to allergens is factored into the weights for the cost of moving through particular cities
            if key == "AQI":
                if airQuality(person, value, cities[curCity][key]) == 0:
                    cost[curCity] += value / 10
                else:
                    cost[curCity] += person.degreeOfSensitivity*value / 10
            elif key == "Pollen":
                if airQuality(person, cities[curCity][key], value) == 0:
                    cost[curCity] += value
                else:
                    cost[curCity] += person.degreeOfSensitivity*value
            else:
                if not visited[key] and key != source:
                    cost[key] += cost[curCity] + 2*value
                    q.put(key)
                    visited[key] = True
    #Here we traverse the city nodes once all the movement costs have been calculated
    return traverse(cities, source, dest, cost)

def traverse(cities, source, dest, cost):
    visited = {"San Diego":False,
       "Palm Springs":False,
       "Los Angeles":False,
       "Santa Barbara":False,
       "Bakersfield":False,
       "San Luis Obispo":False,
       "Fresno":False,
       "Monterey":False,
       "San Jose":False,
       "Sacramento":False,
       "Oakland":False,
       "San Fransisco":False,
       "Napa":False,
       "Eureka":False,
       "Redding":False}
    path = []
    path.append(source)
    #Loop while there are cities in the path to process from
    while path:
        minimum = 100000
        minkey = ""
        curCity = path[-1]
        #Once we find the destination we want to exit the loop and return, we will have our path
        if curCity == dest:
            break
        elif cost[curCity] < cost[dest]: #We need to make sure the cost is not higher than the destination if we're taking an alternate path
            for key, value in cities[curCity].items():
                if key != "AQI" and key != "Pollen" and not visited[key]:
                    if key != source and cost[key] < minimum:
                        minimum = cost[key]
                        minkey = key
        #if we reach this condition and haven't found a possible city to move to, we pop the current city off the stack, otherwise we queue up the next city
        if minkey == "":
            path.pop()
        else:
            path.append(minkey)
            visited[minkey] = True
        
    return path

#This function simply checks if the given AQI and pollen counts are below the given thresholds depending on sensitivity
def safetyCheck(sensitiveAQI, sensitivePollen, thresholdAQILow, thresholdAQIHigh, thresholdPollenLow, thresholdPollenHigh, AQI, pollen):
    if sensitiveAQI and sensitivePollen:
        if AQI > thresholdAQILow and pollen > thresholdPollenLow:
            return -3
        elif AQI > thresholdAQILow:
            return -2
        elif pollen > thresholdPollenLow:
            return -1
        else:
            return 0
    elif sensitiveAQI:
        if AQI > thresholdAQILow and pollen > thresholdPollenHigh:
            return -3
        elif AQI > thresholdAQILow:
            return -2
        elif pollen > thresholdPollenHigh:
            return -1
        else:
            return 0
    elif sensitivePollen:
        if AQI > thresholdAQIHigh and pollen > thresholdPollenLow:
            return -3
        elif AQI > thresholdAQIHigh:
            return -2
        elif pollen > thresholdPollenLow:
            return -1
        else:
            return 0
    else:
        if AQI > thresholdAQIHigh and pollen > thresholdPollenHigh:
            return -3
        elif AQI > thresholdAQIHigh:
            return -2
        elif pollen > thresholdPollenHigh:
            return -1
        else:
            return 0

def airQuality(person, AQI, pollen):
    #If the pollen or AQI counts are above these levels, the air isn't safe regardless of sensitivity
    danger = safetyCheck(person.AQIsensitive, person.PollenSensitive, 300, 300, 9.7, 9.7, AQI, pollen)
    if danger < 0:
        return danger
    elif person.degreeOfSensitivity == 1:
        return safetyCheck(person.AQIsensitive, person.PollenSensitive, 200, 300, 7.2, 9.7, AQI, pollen)
    elif person.degreeOfSensitivity == 2:
        return safetyCheck(person.AQIsensitive, person.PollenSensitive, 150, 200, 4.8, 7.2, AQI, pollen)
    elif person.degreeOfSensitivity == 3:
        return safetyCheck(person.AQIsensitive, person.PollenSensitive, 100, 150, 2.4, 4.8, AQI, pollen)
    elif person.degreeOfSensitivity == 4:
        return safetyCheck(person.AQIsensitive, person.PollenSensitive, 50, 100, 0, 2.4, AQI, pollen)

class AsthmaTrip():
    """ Initializes values with user input and finds best path """
    def __init__ (self):
        self.person = self.getPatient()
        self.g = Graph()
        self.startLoc = places[random.randrange(1, 15)]
        self.endLoc = places[random.randrange(1, 15)]
        self.path = self.getPath()
        self.showResults()
        
    def showResults(self):
         #Give feedback about what's been generated and what happened
        print('\n\nHere are the results for', self.person.name, '!!\n\n' ) 
        print(self.person.name + " wants to drive from " + self.startLoc + " to " + self.endLoc + ".\n They have a " + sens[self.person.degreeOfSensitivity] + " sensitivity to allergens.")
        if self.person.AQIsensitive and self.person.PollenSensitive:
            print(self.person.name + " is particularly sensitive to pollen and AQI.")
        elif self.person.AQIsensitive:
            print(self.person.name + " is particularly sensitive to AQI.")
        elif self.person.PollenSensitive:
            print(self.person.name + " is particularly sensitive to pollen.")
        print("\n\nThe path they should take to minimize allergen exposure is:")
        print(self.path)
        print('\n\nTRIP DETAILS')

        #Loop through the cities in the path and give detailed information about air quality
        for city in self.path:
            safety = airQuality(self.person, self.g.G[city]["AQI"], self.g.G[city]["Pollen"])
            if safety == 0:
                print("The air quality in " + city + " is just fine today.")
            elif safety == -1:
                print("The pollen count in " + city + " is notably high today at a level of " + str(self.g.G[city]["Pollen"]) + ".")
            elif safety == -2:
                print("The AQI in " + city + " is notably high today at a level of " + str(self.g.G[city]["AQI"]) + ".")
            elif safety == -3:
                print("The AQI and pollen counts in " + city + " are notably high today at levels of " + str(self.g.G[city]["AQI"]) + " and " + str(self.g.G[city]["Pollen"]) + " respectively.")


    def getPath(self):
        """ Calls search to find the optimal route """
        return search(self.person, self.g.G, self.startLoc, self.endLoc)
        
    #def getLocations(self):

    def getPatient(self):
        """ Returns tha patients information
        """
        #get name
        name = input('\nEnter name of person: ')
        
        #get asthma condition
        print('How severe is the asthma condition of', name, '? ')
        for i in sens:
            print('(', i, ') ', sens[i])
        degreeOfSensitivity = int(input())
        
        #get aqi sensitivity 
        AQI = input('Are they sensitive to bad air quality? (Y/N) ')
        if (AQI == 'Y' or AQI == 'y'):
            AQIsensitive = True
        else:
            AQIsensitive = False

        #get pollen sensitivity
        Pollen = input('Are they sensitive to high pollen counts? (Y/N) ')
        if (AQI == 'Y' or AQI == 'y'):
            PollenSensitive = True
        else:
            PollenSensitive = False

        return Patient(degreeOfSensitivity, AQIsensitive, PollenSensitive, name)

def main():
    print('')
    print('')
    print('')
    print('------------------------------')
    print('------------------------------')
    print('------------------------------')
    print('!!!!!!!!Asthma Travels!!!!!!!!')
    print('------------------------------')
    print('---------------------CSci 154-')
    print('------------------------------')
    print('------------------------------')
    print('')
    print('')
    print('I need to get some information from you')
    print('before we can get you on your way...')
    myTrip = AsthmaTrip()
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')


main()