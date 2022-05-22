import requests
from bs4 import BeautifulSoup
import json

level = ["Assente", "Bassa", "Media", "Alta"]

def get_forecast(city):
    url = r"https://www.3bmeteo.com/meteo/" + city + "/pollini"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find_all("div", class_="table-previsioni")[1]
    return table

def get_parsed_forecast(city):
    parsedForecast = list()
    table = get_forecast(city)
    # Extract full list
    forecastList = table.find_all("div", class_="row-table")
    # Analize each line
    for line in forecastList:
        el = line.find_all("div", class_="row-table")
        #print(el)
        if len(el) > 1:
            x = dict()
            x["name"] = el[0].get_text().strip()
            my_list = el[1].find_all("div", class_="altriDati")
            x["list"] = [s.get_text().strip() for s in my_list]
            parsedForecast.append(x)
        else:
            continue

    return parsedForecast

if __name__ == '__main__':
    allergies = ["graminacee", "olivo"]
    city = r"milano"
    data = get_parsed_forecast(city)

    #Check allergy
    for allergy in allergies:
        for info in data:
            if info["name"] == allergy:
                if info["list"][0] == level[3] or info["list"][1] == level[3]:
                    print("Attenzione alle : "+ allergy + " 🤧")
                else:
                    print("Nessun problema per: " + allergy)


    #print(data)
    with open('data.json', 'w') as f:
        json.dump(data, f)
