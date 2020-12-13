import unittest
import sqlite3
import requests
import json
import os
from bs4 import BeautifulSoup
import time
import re
import statistics

API_KEY = "e81c3fb0-2998-4139-8d32-7886f836d266"
def get_data(city, state):
    try:
        base_url = "http://api.airvisual.com/v2/city?city={}&state={}&country=USA&key={}"
        request_url = base_url.format(city, state, API_KEY)
        r = requests.get(request_url)
        dic = r.json()
    except:
        None
        print("error when reading from url")
        dic = []
    print(dic)
    return dic

def get_data_2(city):
    base_url = 'https://api.teleport.org/api/urban_areas/slug:{}/scores/'
    request_url = base_url.format(city)
    r = requests.get(request_url)
    dic = json.loads(r.text)
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
    soup = BeautifulSoup(r, 'html.parser')
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
    #cur.execute("DROP TABLE IF EXISTS Weather")
    #cur.execute("DROP TABLE IF EXISTS Scores")
    #cur.execute("DROP TABLE IF EXISTS Population")
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (city_id INTEGER PRIMARY KEY, city TEXT, state TEXT, temp INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Scores (city_id INTEGER PRIMARY KEY, city TEXT, HousingScore INTEGER, CostOfLivingScore INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Population (city_id INTEGER PRIMARY KEY, city TEXT, population INTEGER)")
    conn.commit()

def fill_weather_table(cur, conn):

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
        ("seattle", "Washington"), ("charlotte", "North Carolina"), 
        ("portland", "Oregon"), ("sacramento", "California"), ("oakland", "California"), ("tulsa", "Oklahoma"), 
        ("lexington", "Kentucky"), ("henderson", "Nevada"), ("greensboro", "North Carolina"), ("newark", "New Jersey"), 
        ("toledo", "Ohio"), ("laredo", "Texas"), ("madison", "Wisconsin"), ("scottsdale", "Arizona"), ("reno", "Nevada"), 
        ("boston", "Massachusetts"), ("louisville", "Kentucky"), ("baltimore", "Maryland"), ("albequerque", "New Mexico"), 
        ("tucson", "Arizona"), ("fresno", "California"), ("mesa", "Arizona"), ("minneapolis", "Minnesota"), ("arlington", "Texas"),
        ("wichita", "Kansas"), ("bakersfield", "California"), ("aurora", "Colorado"), ("anaheim", "California"),
        ("riverside", "California"), ("plano", "Texas"), ("durham", "North Carolina"), ("lubbock", "Texas"), ("chandlar", "Arizona"),
        ("norfolk", "Virginia"), ("gilbert", "Arizona"), ("chesapeake", "Virginia"), ("irving", "Texas"), ("hialeah", "Florida"),
        ("garland", "Texas"), ("fremont", "California"), ("spokane", "Washington"), ("tacoma", "Washington"), ("modesto", "California"),
        ("oxnard", "California"), ("huntsville", "Alabama"), ("augusta", "Georgia"), ("amarillo", "Texas"), ("oceanside", "California"),
        ("springfield", "Missouri"), ("lakewood", "Colorado"), ("hollywood", "Florida"), ("sunnyvale", "California"),
        ("macon", "Georgia"), ("pasadena", "Texas"), ("naperville", "Illinois"), ("bellevue", "Washington"), ("savannah", "Georgia"),
        ("syracuse", "New York"), ("denton", "Texas"), ("thorton", "Colorado")]
    
    cur.execute('SELECT max(city_id) FROM Weather')
    city_id = cur.fetchone()[0]
    if city_id == None:
        city_id = 0
    current_list = city_state_list[city_id:city_id + 25]

    for city_tup in current_list:
    
        try:
            city_data = get_data(city_tup[0], city_tup[1])
            city = city_data['data']['city']
            state = city_data['data']['state']
            temp = city_data['data']['current']['weather']['tp']
            
            cur.execute("INSERT OR IGNORE INTO Weather (city_id, city, state, temp) VALUES (?,?,?,?)", (city_id, city, state, temp))
            city_id += 1
        except:
            print("error")
        time.sleep(10)

    conn.commit()

def fill_scores_table(cur, conn):

    cities = ["anchorage", "asheville", "atlanta", "austin", "birmingham", "boise", "buffalo", "charleston", 
            "chattanooga", "chicago", "cincinnati", "cleveland", "colorado-springs", "columbus", "dallas", "denver",
            "detroit", "honolulu", "houston", "indianapolis", "jacksonville", "kansas-city", "knoxville", "las-vegas",
            "memphis", "miami", "milwaukee", "nashville", "new-orleans", "oklahoma-city",
            "omaha", "orlando", "philadelphia", "phoenix", "pittsburgh", "portland-or", "providence", "raleigh", "richmond",
            "rochester", "salt-lake-city", "san-antonio", "san-diego", "seattle", "st-louis",
            "bangkok", "beijing", "brisbane", "budapest", "cairo", "cambridge",
            "casablanca", "cologne", "delhi", "dubai","edmonton", "florence",
            "geneva", "gibraltar", "guadalajara", "guatemala-city", "hamburg", "havana",
            "istanbul", "jakarta", "krakow", "kyoto", "lagos", "leeds", "leipzig", "lima",
            "liverpool", "luxembourg", "lyon", "madrid", "malaga", "manchester", "manila", "marseille", "melbourne",
            "mexico-city", "milan", "nairobi", "naples", "nice", "ottawa",
             "shanghai", "sydney", "valencia", "washington-dc", 
             "winnipeg", "tampa-bay-area", "seville", "ankara", "baku", "bern", "nantes",
             "minsk", "oslo","perth", "oulu", "porto", "phuket"]

    list_of_dics = []
    for city in cities:
        list_of_dics.append(get_data_2(city))

    cur.execute('SELECT city FROM Scores')
    city_list = cur.fetchall()

    x = 1
    count = len(city_list)

    for x in range(25):
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

def join_scores_and_pop(cur, conn):
    cur.execute('SELECT Scores.city, Scores.HousingScore, Scores.CostOfLivingScore, Population.population FROM Scores INNER JOIN Population ON Scores.city = Population.city')
    results = cur.fetchall()
    conn.commit()
    print(results)
    return results

def join_pop_and_weather(cur, conn):
    cur.execute("SELECT Population.city, Population.population, Weather.temp FROM Population INNER JOIN Weather ON Population.city = Weather.city")
    results = cur.fetchall()
    conn.commit()
    print(results)
    return results

def join_weather_and_scores(cur, conn):
    cur.execute("SELECT Weather.city, Weather.temp, Scores.CostOfLivingScore FROM Weather INNER JOIN Scores ON Weather.city = Scores.city")
    results = cur.fetchall()
    conn.commit()
    print(results)
    return results

def population_vs_housingscore_calc(cur, conn):
    pops = []
    housescores = []
    tups = join_scores_and_pop(cur, conn)
    for tup in tups:
        pop = int(tup[3].replace(",", ""))
        pops.append(pop)
        housing = tup[1]
        housescores.append(housing)
    #calculate mean of pops
    mean_pops = statistics.mean(pops)
    print(mean_pops)
    #calculating mean of housing scores
    mean_housing = statistics.mean(housescores)
    print(mean_housing)
    return(mean_pops, mean_housing)

def calc_weather_scores(cur, conn):
    new_cities = []
    tups = join_weather_and_scores(cur, conn)
    for tup in tups:
        cost_score = tup[2]
        if cost_score >= 5:
            new_cities.append(tup)
    temps = []
    for tup in new_cities:
        temp = tup[1]
        temps.append(temp)
    average_temp = statistics.mean(temps)
    return average_temp

def write_data_to_file(filename, cur, conn):
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    outFile = open(path + filename, "w")
    means = population_vs_housingscore_calc(cur, conn)
    outFile.write("Average Population of US cities: ")
    outFile.write(str(means[0]) + "\n")
    outFile.write("=======================================================================\n\n")

    outFile.write("Average Housing Score of US cities: ")
    outFile.write(str(means[1]) + "\n")
    outFile.write("=======================================================================\n\n")

    avg_temp = calc_weather_scores(cur, conn)
    outFile.write("Average Temperature of US Cities with a Cost of Living Score of 5 or Higher: ")
    outFile.write(str(avg_temp) + "\n")
    outFile.write("=======================================================================\n\n")

    outFile.close()

def main():
    conn = sqlite3.connect("/Users/jadeshepherd/Desktop/SI 206/happyweather/weather_data.db")
    cur = conn.cursor()
    set_up_tables(cur, conn)
    
    fill_weather_table(cur, conn)
    fill_scores_table(cur, conn)
    fill_pop_table(cur, conn)

    write_data_to_file("calculations.txt", cur, conn)

if __name__ == "__main__":
    main()