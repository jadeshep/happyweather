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
    print(dic)
    return dic

def get_website_data(url):
    # d = {}
    L = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
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

def database(data1):
    cur, conn = setUpDatabase('weather_data.db')
    cur.execute('CREATE TABLE IF NOT EXISTS Weather (city TEXT, state TEXT temp INTEGER)')
    for i in data1:
        cur.execute('INSERT INTO Weather (city, state, temp) VALUES (?,?,?)', (i[0][0], i[0][1], i[3][1]))
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
    unittest.main(verbosity=2)
    cur, conn = setUpDatabase('weather_data.db')
    #database(data1)
    print("------------")

if __name__ == "__main__":
    main()