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
    return dic

def get_website_data(url):
    # d = {}
    L = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml") #lxml
    x = soup.find_all(class_ = "cardhub-edu-table center-aligned sortable")
    for i in x:
        name = i.find_all("tr")
        for j in name:
            n = j.text
            L.append(n)
    print(L)
    return L

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def set_up_tables(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (city_id INTEGER PRIMARY KEY, city TEXT, state TEXT, temp INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Scores (city_id INTEGER PRIMARY KEY, city TEXT, HousingScore INTEGER, CostOfLivingScore INTEGER)")
    conn.commit()

def fill_weather_table(cur, conn):
    # cur, conn = setUpDatabase('weather_data.db')
    # conn = sqlite3.connect("weather_data.db")
    # cur = conn.cursor()
    #cur.execute("DROP TABLE IF EXISTS Weather")
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
    for tup in city_state_list:
        list_of_dics.append(get_data(tup[0], tup[1]))

    cur.execute('SELECT city FROM Weather')
    city_list = cur.fetchall()

    x = 1
    count = len(city_list)

    for x in range(8):
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
    #cur.execute("DROP TABLE IF EXISTS Scores")
    #cur.execute("CREATE TABLE IF NOT EXISTS Scores (city_id INTEGER PRIMARY KEY, city TEXT, HousingScore INTEGER, CostOfLivingScore INTEGER)")
    cities = ["anchorage", "asheville", "atlanta", "austin", "birmingham", "boise", "buffalo", "charleston", 
            "chattanooga", "chicago", "cincinnati", "cleveland", "colorado-springs", "columbus", "dallas", "denver",
            "detroit", "honolulu", "houston", "indianapolis", "jacksonville", "kansas-city", "knoxville", "las-vegas",
            "memphis", "miami", "milwaukee", "nashville", "new-orleans", "oklahoma-city",
            "omaha", "orlando", "philadelphia", "phoenix", "pittsburgh", "providence", "raleigh", "richmond",
            "rochester", "salt-lake-city", "san-antonio", "san-diego", "seattle", "st-louis"]

    list_of_dics = []
    for city in cities:
        list_of_dics.append(get_data_2(city))

    cur.execute('SELECT city FROM Scores')
    city_list = cur.fetchall()

    x = 1
    count = len(city_list)

    for x in range(8):
        x = count
        city_id = count + 1
        city = list_of_dics[count]['summary'].split(",")[0][3:]
        housing = list_of_dics[count]['categories'][0]['score_out_of_10']
        living = list_of_dics[count]['categories'][1]['score_out_of_10']

        x += 1
        cur.execute("INSERT OR IGNORE INTO Scores (city_id, city, HousingScore, CostOfLivingScore) VALUES (?,?,?,?)", (city_id, city, housing, living))
        count += 1

    conn.commit()

class TestWeatherAPI(unittest.TestCase):
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

    # print("-----Unittest-------")
    
    # cur, conn = setUpDatabase('weather_data.db')
    conn = sqlite3.connect("weather_data.db")
    cur = conn.cursor()
    set_up_tables(cur, conn)
    

    #fill_weather_table(cur, conn)
    fill_scores_table(cur, conn)

    print("------------")

    unittest.main(verbosity=2) #put this last

if __name__ == "__main__":
    main()