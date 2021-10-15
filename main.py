import requests
import re
import json
from bs4 import BeautifulSoup

url = 'https://telegov.njportal.com/njmvc/AppointmentWizard/17'
response = requests.get(url).text

soup = BeautifulSoup(response, "html.parser")
scripts = soup.find_all('script')
locationPattern = re.compile('var locationData = (.*?);')
timePattern = re.compile("var timeData = (.*?);")
timePattern2 = "var timeData"


for script in scripts:
    if not script.string: continue

    if(locationPattern.match(str(script.string.strip()))):
        locationData = locationPattern.match(script.string.strip())
        locationData = json.loads(locationData.groups()[0])

        timeData = script.string.strip().split(timePattern2)
        timeData = timePattern2 + timeData[1]
        timeData = timeData.split("var locationModel")[0].strip()
        if timeData[-1] != ";": timeData = timeData + ";"
        timeData = timePattern.search(timeData)
        timeData = json.loads(timeData.groups()[0])
        break;


    #elif timeData and locationData: break


for location in locationData:
    if "Paterson" in location["Name"]:
        paterson = location
        break

patersonID = paterson["LocAppointments"][0]["LocationId"]

for time in timeData:

    if time["LocationId"] == patersonID:
        if time["FirstOpenSlot"][0] == "N":
            print("Appointment is not available")
            break
        else:
            print("Appointment is available")
            break
