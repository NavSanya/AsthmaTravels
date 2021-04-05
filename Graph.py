class Graph:
    G={"San Diego":{"Palm Springs":133,"Los Angeles":120},
       "Palm Springs":{"Los Angeles":107, "San Diego":133},
       "Los Angeles":{"Santa Barbara":96, "Bakersfield":112, "San Diego":120},
       "Santa Barbara":{"San Luis Obispo":95, "Los Angeles":96},
       "Bakersfield":{"Fresno":109, "Los Angeles":112},
       "San Luis Obispo":{"Monterey":141, "San Jose":185, "Santa Barbara":95},
       "Fresno":{"Sacramento":169,"Bakersfield":109},
       "Monterey":{"San Jose":73, "San Luis Obispo":141},
       "San Jose":{"Oakland":41, "San Fransisco":48, "Monterey":73, "San Luis Obisco":185},
       "Sacramento":{"Napa":62, "Redding":160, "Fresno":169},
       "Oakland":{"Napa":42, "San Jose":41},
       "San Fransisco":{"Napa":52, "San Jose":48},
       "Napa":{"Eureka":252, "Sacramento":62, "Oakland":42, "San Fransisco":52},
       "Eureka":{"Redding":147, "Napa":252},
       "Redding":{"Eureka":147, "Sacramento":160}}
    AQI = []
    PollenCount=[]

    #for x in f
    #    AQI.append(x)
    #for x1 in f1
    #    PollenCount.append(x1)
    for i in AQI:
        def get_all_values(nested_dictionary):

            for key, value in nested_dictionary.items():
                if type(value) is dict:
                    get_all_values(value)
                elif:
                    distance = value
                    sensitivityAQI = input("Input Y if you are sensitive to AQI otherwise input anything else")
                    sensitivityPollen  = input("Input Y if you are sensitive to Pollen otherwise input anything else")
                    cost = (2*distance) + AQI[i] + PollenCount[i]
                    if (sensitivityAQI=='Y')
                        cost+=AQI[i]
                    if (sensitivityPollen=='Y')
                        cost+=PollenCount[i]
                    value = cost
        
