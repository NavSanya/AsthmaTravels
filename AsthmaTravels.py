import config
import random
import requests
from queue import Queue
from datetime import datetime
from geopy.geocoders import Nominatim
from copy import deepcopy

open_weather_key = config.apiKey

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
    12:"San Francisco",
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

class Node:
    pass
    #AQI, Pollen, etc

class Edge:
    pass
    #Distance
    #AQI average
    #Pollen average
    #(Node A, Node B)
    
class Graph2:
    pass
    #self.nodes[0..n] = Node()
    #self.edges[0..n] = Edge()
    #collection of nodes and edges

class Graph:
    def __init__(self):
        random.seed()
        self.G={"San Diego":{"AQI": self.aqiData("San Diego")[0],"Pollen":self.aqiData("San Diego")[1],"Palm Springs":133,"Los Angeles":120},
           "Palm Springs":{"AQI":self.aqiData("Palm Springs")[0],"Pollen":self.aqiData("Palm Springs")[1],"Los Angeles":107, "San Diego":133},
           "Los Angeles":{"AQI":self.aqiData("Los Angeles")[0],"Pollen":self.aqiData("Los Angeles")[1],"Santa Barbara":96, "Bakersfield":112, "San Diego":120},
           "Santa Barbara":{"AQI":self.aqiData("Santa Barbara")[0],"Pollen":self.aqiData("Santa Barbara")[1],"San Luis Obispo":95, "Los Angeles":96},
           "Bakersfield":{"AQI":self.aqiData("Bakersfield")[0],"Pollen":self.aqiData("Bakersfield")[1],"Fresno":109, "Los Angeles":112},
           "San Luis Obispo":{"AQI":self.aqiData("San Luis Obispo")[0],"Pollen":self.aqiData("San Luis Obispo")[1],"Monterey":141, "San Jose":185, "Santa Barbara":95},
           "Fresno":{"AQI":self.aqiData("Fresno")[0],"Pollen":self.aqiData("Fresno")[1],"Sacramento":169,"Bakersfield":109},
           "Monterey":{"AQI":self.aqiData("Monterey")[0],"Pollen":self.aqiData("Monterey")[1],"San Jose":73, "San Luis Obispo":141},
           "San Jose":{"AQI":self.aqiData("San Jose")[0],"Pollen":self.aqiData("San Jose")[1],"Oakland":41, "San Francisco":48, "Monterey":73, "San Luis Obispo":185},
           "Sacramento":{"AQI":self.aqiData("Sacramento")[0],"Pollen":self.aqiData("Sacramento")[1],"Napa":62, "Redding":160, "Fresno":169},
           "Oakland":{"AQI":self.aqiData("Oakland")[0],"Pollen":self.aqiData("Oakland")[1],"Napa":42, "San Jose":41},
           "San Francisco":{"AQI":self.aqiData("San Francisco")[0],"Pollen":self.aqiData("San Francisco")[1],"Napa":52, "San Jose":48},
           "Napa":{"AQI":self.aqiData("Napa")[0],"Pollen":self.aqiData("Napa")[1],"Eureka":252, "Sacramento":62, "Oakland":42, "San Francisco":52},
           "Eureka":{"AQI":self.aqiData("Eureka")[0],"Pollen":self.aqiData("Eureka")[1],"Redding":147, "Napa":252},
           "Redding":{"AQI":self.aqiData("Redding")[0],"Pollen":self.aqiData("Redding")[1],"Eureka":147, "Sacramento":160}}
    
    def aqiData(self, city):
        # Implementing API to get geolocation
        loc = city
        geolocation = Nominatim(user_agent="asthmaTravels")  # Making an instance of Nominatim class
        locInfo = geolocation.geocode(loc)
        locLat = locInfo.latitude
        locLong = locInfo.longitude

        ow_link = 'http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(locLat)+'&lon='+str(locLong)+'&appid='+open_weather_key

        api_link = requests.get(ow_link)
        api_data = api_link.json()
        airQual = api_data['list'][0]['main']['aqi']
        partMatt = api_data['list'][0]['components']['pm2_5']
        return airQual, partMatt

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
       "San Francisco":False,
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
       "San Francisco":0,
       "Napa":0,
       "Eureka":0,
       "Redding":0}

    c = deepcopy(cities)
    for key1, value1 in cost.items():
        for key2, value2 in cities[key1].items():
            if key2 != "AQI" and key2 != "Pollen":
                if airQuality(person, cities[key1]["AQI"], cities[key1]["Pollen"]) != 0:
                    del c[key1][key2]
                    
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
    '''
    Function header: traverse(cities, source, dest, cost)
    Parameters: the graph, start location(int), end location(int) and the cost of all edges of the graph
    Returns the shortest path from source to destination according to the cost
    '''
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
       "San Francisco":False,
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
traverse.__doc__

#This function simply checks if the given AQI and pollen counts are below the given thresholds depending on sensitivity
def safetyCheck(sensitiveAQI, sensitivePollen, thresholdAQILow, thresholdAQIHigh, thresholdPollenLow, thresholdPollenHigh, AQI, pollen):
    '''
    Function header: safetyCheck(sensitiveAQI, sensitivePollen, thresholdAQILow, thresholdAQIHigh, thresholdPollenLow, thresholdPollenHigh, AQI, pollen)
    Parameters:  sensitiveAQI(true/false), sensitivePollen(true/false), thresholdAQILow(int), thresholdAQIHigh(int), thresholdPollenLow(int), thresholdPollenHigh(int)
    This function simply checks if the given AQI and pollen counts are below the given thresholds depending on sensitivity
    '''
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
safetyCheck.__doc__

def airQuality(person, AQI, pollen):
    #If the pollen or AQI counts are above these levels, the air isn't safe regardless of sensitivity
    danger = safetyCheck(person.AQIsensitive, person.PollenSensitive, 301, 301, 250.5, 250.5, AQI, pollen)
    if danger < 0:
        return danger
    elif person.degreeOfSensitivity == 1:
        return safetyCheck(person.AQIsensitive, person.PollenSensitive, 201, 300, 150.5, 250.4, AQI, pollen)
    elif person.degreeOfSensitivity == 2:
        return safetyCheck(person.AQIsensitive, person.PollenSensitive, 151, 200, 55.5, 150.4, AQI, pollen)
    elif person.degreeOfSensitivity == 3:
        return safetyCheck(person.AQIsensitive, person.PollenSensitive, 101, 150, 35.5, 55.4, AQI, pollen)
    elif person.degreeOfSensitivity == 4:
        return safetyCheck(person.AQIsensitive, person.PollenSensitive, 51, 100, 12.1, 35.4, AQI, pollen)

class AsthmaTrip():
    """ Initializes values with user input and finds best path """
    def __init__ (self):
        self.person = self.getPatient()
        self.g = Graph()
        self.startLoc, self.endLoc = self.getLocations()
        self.path = self.getPath()
        self.showResults()
        
    def showResults(self):
        """ Give feedback about what's been generated and what happened """
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
                print("The Particle Matter 2.5 in " + city + " is notably high today at a level of " + str(self.g.G[city]["Pollen"]) + ".")
            elif safety == -2:
                print("The AQI in " + city + " is notably high today at a level of " + str(self.g.G[city]["AQI"]) + ".")
            elif safety == -3:
                print("The AQI and pollen counts in " + city + " are notably high today at levels of " + str(self.g.G[city]["AQI"]) + " and " + str(self.g.G[city]["Pollen"]) + " respectively.")


    def getPath(self):
        """ Calls search to find the optimal route """
        return search(self.person, self.g.G, self.startLoc, self.endLoc)
        
    def getLocations(self):
        """ Get user input for start and end locations """
    
        for i in places:
            print('(', i, ') ', places[i])
        
        start = int(input('Choose departure city:  '))
        end = int(input('Choose destination city:  '))

        return places[start], places[end]

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
        PM = input('Are they sensitive to higher levels of Particulate Matter (PM2.5)? (Y/N) ')
        if (PM == 'Y' or PM == 'y'):
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