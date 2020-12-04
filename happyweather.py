import unittest
import sqlite3
import requests
import json
import os
from bs4 import BeautifulSoup

#Testing git pull - do you see this comment?

# test 2 - hi jade
API_KEY = "91c93e9c-1957-45b7-bdf5-c7b51881a029"
def get_data(city, state):
    try:
        base_url = "http://api.airvisual.com/v2/city?city={}&state={}&country=USA&key={}"
        request_url = base_url.format(city, state, API_KEY)
        r = requests.get(request_url)
        dic = json.loads(r.text)
    except:
        print("error when reading from url")
        dic = []
    #print(dic)
    return dic

def get_data_2(city):
    base_url = 'https://api.teleport.org/api/urban_areas/slug:{}/scores/'
    request_url = base_url.format(city)
    r = requests.get(request_url)
    dic = json.loads(r.text)
    # print(dic)
    # print(dic['summary'].split(",")[0][3:])
    # print(dic['categories'][0]['score_out_of_10']) #housing
    # print(dic['categories'][1]['score_out_of_10']) #costofliving
    return dic

def get_website_data(url):
    # d = {}
    L = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser") #lxml
    x = soup.find_all(class_ = "cardhub-edu-table center-aligned sortable")
    for i in x:
        name = i.find_all("tr")
        for j in name[:25]:
            n = j.text
            L.append(n)
    print(L)
    return L

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def database(data, cur, conn):
    # cur, conn = setUpDatabase('weather_data.db')
    # conn = sqlite3.connect("weather_data.db")
    # cur = conn.cursor()
    #cur.execute("DROP TABLE IF EXISTS Weather")
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (city TEXT PRIMARY KEY UNIQUE, state TEXT, temp INTEGER)")
    cur.execute("INSERT INTO Weather (city, state, temp) VALUES (?,?,?)", (data['data']['city'], data['data']['state'], data['data']['current']['weather']['tp']))
    conn.commit()

def database2(data, cur, conn):
    #cur.execute("DROP TABLE IF EXISTS Scores")
    cur.execute("CREATE TABLE IF NOT EXISTS Scores (city TEXT PRIMARY KEY UNIQUE, HousingScore INTEGER, CostOfLivingScore INTEGER)")
    cur.execute("INSERT INTO Scores (city, HousingScore, CostOfLivingScore) VALUES (?,?,?)", (data['summary'].split(",")[0][3:], data['categories'][0]['score_out_of_10'], data['categories'][1]['score_out_of_10']))
    conn.commit()

class TestDiscussion11(unittest.TestCase):
    def test_check_data(self):
        data1 = get_data("Los Angeles", "California")
        data2 = get_data("Madison", "Wisconsin")
        #self.assertEqual(type(data1), type([]))
        #self.assertEqual(data1[0]['page'], 1)
        #self.assertEqual(data1[1][0]['countryiso3code'], "BRA")

class TestWebsiteData(unittest.TestCase):
    def test_website_data(self):
        data = get_website_data("https://wallethub.com/edu/happiest-places-to-live/32619")

def main():
    # CO2 emission in the US in 2014 (tons per capita)
    # print("-----Population-----")
    # country = "JPN" !
    # year = "2014"
    # value1 = population_year(country, year)
    # print("The population in {} in {} is {}".format(country, year, value1))

    # print("-----Unittest-------")
    
    # cur, conn = setUpDatabase('weather_data.db')
    conn = sqlite3.connect("weather_data.db")
    cur = conn.cursor()
    L2 = ["anchorage", "asheville", "atlanta", "austin", "birmingham", "boise", "boston", "buffalo", "charleston", 
            "chattanooga", "chicago", "cincinnati", "cleveland", "colorado-springs", "columbus", "dallas", "denver",
            "detroit", "honolulu", "houston", "indianapolis", "jacksonville", "kansas-city", "knoxville", "las-vegas",
            "los-angeles", "memphis", "miami", "milwaukee", "nashville", "new-orleans", "new-york", "oklahoma-city",
            "omaha", "orlando", "philadelphia", "phoenix", "pittsburgh", "providence", "raleigh", "richmond",
            "rochester", "salt-lake-city", "san-antonio", "san-diego", "seattle", "st-louis"]
    database(get_data("Los Angeles", "California"), cur, conn)
    for city in L2:
        database2(get_data_2(city), cur, conn)
    print("------------")

    unittest.main(verbosity=2) #put this last

if __name__ == "__main__":
    main()