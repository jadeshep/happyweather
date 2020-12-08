import unittest
import sqlite3
import requests
import json
import os
from bs4 import BeautifulSoup

#Testing git pull - do you see this comment?

# test 2 - hi jade
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

def get_website_data(url):

    L = []
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser') #lxml
    #x = soup.find_all(class_ = "wikitable sortable jquery-tablesorter")
    x = soup.find('table', {'class':'wikitable sortable'})
    links = x.find_all('a')
    for i in links:
        if i.get('title') == None:
            continue
        else:
            L.append(i.get('title'))
        # name = i.find_all("title")
        # for j in name:
        #     n = j.text
        #     L.append(n)
    print(L)
    return L

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def set_up_tables(cur, conn):
    # cur.execute("DROP TABLE IF EXISTS Weather")
    # cur.execute("DROP TABLE IF EXISTS Scores")
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (city_id INTEGER PRIMARY KEY, city TEXT, state TEXT, temp INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Scores (city_id INTEGER PRIMARY KEY, city TEXT, HousingScore INTEGER, CostOfLivingScore INTEGER)")
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
    for tup in city_state_list:
        list_of_dics.append(get_data(tup[0], tup[1]))

    cur.execute('SELECT city FROM Weather')
    city_list = cur.fetchall()

    x = 1
    count = len(city_list)

    for x in range(10):
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

class TestWeatherAPI(unittest.TestCase):
    def test_check_data(self):
        data1 = get_data("Los Angeles", "California")
        data2 = get_data("Madison", "Wisconsin")
        #self.assertEqual(type(data1), type([]))
        #self.assertEqual(data1[0]['page'], 1)
        #self.assertEqual(data1[1][0]['countryiso3code'], "BRA")

class TestWebsiteData(unittest.TestCase):
    def test_website_data(self):
        data = get_website_data("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population")
        print(data)

def main():

    # print("-----Unittest-------")
    
    # cur, conn = setUpDatabase('weather_data.db')
    conn = sqlite3.connect("weather_data.db")
    cur = conn.cursor()
    set_up_tables(cur, conn)
    
    #fill_weather_table(cur, conn)
    #fill_scores_table(cur, conn)

    print(get_website_data("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"))

    print("------------")

    unittest.main(verbosity=2) #put this last

if __name__ == "__main__":
    main()