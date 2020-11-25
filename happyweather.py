import unittest
import sqlite3
import requests
import json
import os

#Testing git pull - do you see this comment?
# test 2 - hi jade

API_KEY = "91c93e9c-1957-45b7-bdf5-c7b51881a029"
def get_data(city, state):
    try:
        base_url = "http://api.airvisual.com/v2/city?city={}&state={}&country=USA&key={}"
        request_url = base_url.format(city, state, API_KEY)
        r = requests.get(request_url)
        lst = json.loads(r.text)
    except:
        print("error when reading from url")
        lst = []
    print(lst)
    return lst



def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



class TestDiscussion11(unittest.TestCase):
    def test_check_data(self):
        data1 = get_data("Los Angeles", "California")
        data2 = get_data("Madison", "Wisconsin")
        #self.assertEqual(type(data1), type([]))
        #self.assertEqual(data1[0]['page'], 1)
        #self.assertEqual(data1[1][0]['countryiso3code'], "BRA")

def main():
    # CO2 emission in the US in 2014 (tons per capita)
    # print("-----Population-----")
    # country = "JPN" !
    # year = "2014"
    # value1 = population_year(country, year)
    # print("The population in {} in {} is {}".format(country, year, value1))

    # print("-----Unittest-------")
    unittest.main(verbosity=2)
    cur, conn = setUpDatabase('animal_hospital.db')
    print("------------")

if __name__ == "__main__":
    main()
