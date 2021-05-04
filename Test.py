import requests
from datetime import datetime
from geopy.geocoders import Nominatim

city = input('Enter the city: ')   
geolocation = Nominatim(user_agent="asthmaTravels")  # Making an instance of Nominatim class
locInfo = geolocation.geocode(city)                  # Applying geocode method to get the location
lattitude = locInfo.latitude
longitude = locInfo.longitude
print('The Latitude is -> ', lattitude)
print('The Longitude is -> ', longitude)

# Should be hidden
open_weather_key = 'debe00cc9953a4e09636a2e3e393929a'
# # Air Quality Index. Possible values: 1, 2, 3, 4, 5. 
# # 1 = Good, 
# # 2 = Fair, 
# # 3 = Moderate, 
# # 4 = Poor, 
# # 5 = Very Poor.

ow_link = 'http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lattitude)+'&lon='+str(longitude)+'&appid='+open_weather_key

api_link = requests.get(ow_link)
api_data = api_link.json()
airQual = api_data['list'][0]['main']['aqi']
partMatt = api_data['list'][0]['components']['pm2_5']

print('Air Quality Index: ', airQual)
print('Particle Matter 2.5: ', partMatt)

print('\nAPI DATA')
print(api_data)