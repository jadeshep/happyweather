import unittest
import sqlite3
import requests
import json
import os
from bs4 import BeautifulSoup
import time
import re

API_KEY = "b833a42c-9fec-403b-9a8c-b954f59a03b0"
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
    return dic

def get_city_website_data(url):

    L1 = []
    L2 = []
    pattern = r't">([A-Za-z\s\.\-]*)<\/d'
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser') #lxml
    x = soup.find('table', {'class':'goodOlTxt content'})
    links = x.find_all('tr')
    for i in links:
        y = i.find('td', {'class':'numbers'})
        L1.append(str(y))
    for item in L1:
        name = re.findall(pattern, item)
        for n in name:
            L2.append(n)
    L2.insert(0, 'New York')
    return L2

def get_pop_website_data(url):
    L1 = []
    L2 = []
    pattern = r'r">([\S]*)<\/d'
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser') #lxml
    x = soup.find('table', {'class':'goodOlTxt content'})
    links = x.find_all('tr')
    for i in links:
        y = i.find_all('td', {'class':'numbers'})
        L1.append(str(y))
    for item in L1:
        nums = re.findall(pattern, item)
        for num in nums:
            L2.append(num)
    L2[0] = '8,622,698'
    return(L2)


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def set_up_tables(cur, conn):
    # cur.execute("DROP TABLE IF EXISTS Weather")
    # cur.execute("DROP TABLE IF EXISTS Scores")
    # cur.execute("DROP TABLE IF EXISTS Population")
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (city_id INTEGER PRIMARY KEY, city TEXT, state TEXT, temp INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Scores (city_id INTEGER PRIMARY KEY, city TEXT, HousingScore INTEGER, CostOfLivingScore INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Population (city_id INTEGER PRIMARY KEY, city TEXT, population INTEGER)")
    conn.commit()

def fill_weather_table(cur, conn):
    # cur, conn = setUpDatabase('weather_data.db')
    # conn = sqlite3.connect("weather_data.db")
    # cur = conn.cursor()

    #cur.execute("CREATE TABLE IF NOT EXISTS Weather (city_id INTEGER PRIMARY KEY, city TEXT, state TEXT, temp INTEGER)")
    city_state_list = [("anchorage", "Alaska"), ("asheville", "North Carolina"), ("atlanta", "Georgia"), ("austin", "Texas"), 
        ("birmingham", "Alabama"), ("boise", "Idaho"), ("buffalo", "New York"), ("charleston", "South Carolina"),
        ("chattanooga", "Tennessee"), ("chicago", "Illinois"), ("cincinnati", "Ohio"), ("cleveland", "Ohio"),
        ("colorado springs", "Colorado"), ("columbus", "Ohio"), ("dallas", "Texas"), ("denver", "Colorado"),
        ("detroit", "Michigan"), ("honolulu", "Hawaii"), ("houston", "Texas"), ("indianapolis", "Indiana"), 
        ("jacksonville", "Florida"), ("kansas city", "Kansas"), ("knoxville", "Tennessee"), ("las vegas", "Nevada"),
        ("memphis", "Tennessee"), ("miami", "Florida"), ("milwaukee", "Wisconsin"), ("nashville", "Tennessee"),
        ("new orleans", "Louisiana"), ("oklahoma-city", "Oklahoma"),("omaha", "Nebraska"), ("orlando", "Florida"),
        ("philadelphia", "Pennsylvania"), ("phoenix", "Arizona"), ("pittsburgh", "Pennsylvania"), 
        ("providence", "Rhode Island"), ("raleigh", "North Carolina"), ("richmond", "Virginia"),
        ("rochester", "Minnesota"), ("salt-lake-city", "Utah"), ("san-antonio", "Texas"), ("san diego", "California"),
        ("seattle", "Washington"), ("st louis", "Missouri")]
    
    list_of_dics = []
    num = 0
    for tup in city_state_list:
        list_of_dics.append(get_data(tup[0], tup[1]))
        num += 1
        if num == 10 or num ==15 or num == 20 or num == 25 or num == 30 or num == 35 or num == 40 or num == 50:
            time.sleep(75)

    cur.execute('SELECT city FROM Weather')
    city_list = cur.fetchall()

    x = 1
    count = len(city_list)

    for x in range(25):
        x = count
        city_id = count + 1
        city = list_of_dics[count]['data']['city']
        state = list_of_dics[count]['data']['state']
        temp = list_of_dics[count]['data']['current']['weather']['tp']

        x += 1
        cur.execute("INSERT OR IGNORE INTO Weather (city_id, city, state, temp) VALUES (?,?,?,?)", (city_id, city, state, temp))
        count += 1

    conn.commit()

def fill_scores_table(cur, conn):
    #cur.execute("CREATE TABLE IF NOT EXISTS Scores (city_id INTEGER PRIMARY KEY, city TEXT, HousingScore INTEGER, CostOfLivingScore INTEGER)")
    cities = ["anchorage", "asheville", "atlanta", "austin", "birmingham", "boise", "buffalo", "charleston", 
            "chattanooga", "chicago", "cincinnati", "cleveland", "colorado-springs", "columbus", "dallas", "denver",
            "detroit", "honolulu", "houston", "indianapolis", "jacksonville", "kansas-city", "knoxville", "las-vegas",
            "memphis", "miami", "milwaukee", "nashville", "new-orleans", "oklahoma-city",
            "omaha", "orlando", "philadelphia", "phoenix", "pittsburgh", "portland-me", "portland-or", "providence", "raleigh", "richmond",
            "rochester", "salt-lake-city", "san-antonio", "san-diego", "seattle", "st-louis", "amsterdam", "athens",
            "bangkok", "barcelona", "beijing", "berlin", "brisbane", "brussels", "budapest", "cairo", "cambridge",
            "casablanca", "cologne", "copenhagen", "delhi", "dubai", "dublin", "edinburgh", "edmonton", "florence",
            "geneva", "gibraltar", "glasgow", "guadalajara", "guatemala-city", "hamburg", "havana", "helsinki",
            "hong-kong", "istanbul", "jakarta", "kiev", "krakow", "kyoto", "lagos", "leeds", "leipzig", "lima", "lisbon",
            "liverpool", "london", "luxembourg", "lyon", "madrid", "malaga", "manchester", "manila", "marseille", "melbourne",
            "mexico-city", "milan", "montreal", "moscow", "mumbai", "nairobi", "naples", "nice", "ottawa", "seoul",
             "shanghai", "singapore", "sydney"]

    list_of_dics = []
    for city in cities:
        list_of_dics.append(get_data_2(city))

    cur.execute('SELECT city FROM Scores')
    city_list = cur.fetchall()

    x = 1
    count = len(city_list)

    for x in range(10):
        x = count
        city_id = count + 1
        city = list_of_dics[count]['summary'].split(",")[0][3:]
        housing = list_of_dics[count]['categories'][0]['score_out_of_10']
        living = list_of_dics[count]['categories'][1]['score_out_of_10']

        x += 1
        cur.execute("INSERT OR IGNORE INTO Scores (city_id, city, HousingScore, CostOfLivingScore) VALUES (?,?,?,?)", (city_id, city, housing, living))
        count += 1

    conn.commit()

def fill_pop_table(cur, conn):

    url = "https://www.baruch.cuny.edu/nycdata/world_cities/largest_cities-usa.htm"
    L1 = get_city_website_data(url)
    L2 = get_pop_website_data(url)

    cur.execute('SELECT city FROM Population')
    pop_list = cur.fetchall()

    x = 1
    count = len(pop_list)

    for x in range(25):
        x = count
        city_id = count + 1
        city = L1[count]
        pop = L2[count]

        x += 1
        cur.execute("INSERT OR IGNORE INTO Population (city_id, city, population) VALUES (?,?,?)", (city_id, city, pop))
        count += 1
    
    conn.commit()

def join_tables(cur, conn):
    cur.execute('SELECT Scores.city, Scores.HousingScore, Scores.CostOfLivingScore, Population.population FROM Scores INNER JOIN Population ON Scores.city = Population.city')
    results = cur.fetchall()
    conn.commit()
    print(results)

class TestWeatherAPI(unittest.TestCase):
    def test_check_data(self):
        data1 = get_data("Los Angeles", "California")
        data2 = get_data("Madison", "Wisconsin")
        #self.assertEqual(type(data1), type([]))
        #self.assertEqual(data1[0]['page'], 1)
        #self.assertEqual(data1[1][0]['countryiso3code'], "BRA")

class TestWebsiteData(unittest.TestCase):
    def test_website_data(self):
        pass

def main():

    # print("-----Unittest-------")
    
    # cur, conn = setUpDatabase('weather_data.db')
    conn = sqlite3.connect("/Users/jadeshepherd/Desktop/SI 206/happyweather/weather_data.db")
    cur = conn.cursor()
    set_up_tables(cur, conn)
    
    #fill_weather_table(cur, conn)
    #fill_scores_table(cur, conn)
    #fill_pop_table(cur, conn)
    join_tables(cur, conn)

    print("------------")
    #unittest.main(verbosity=2) #put this last

if __name__ == "__main__":
    main()