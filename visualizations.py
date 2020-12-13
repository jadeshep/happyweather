import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import re
import json
import matplotlib.pyplot as plt
import plotly.express as plt
import plotly.graph_objects as go
import plotly.express as px


def main():
    """Takes no inputs and returns nothing. Selects data from the database in order to create visualizations.) """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+"/weather_data.db")
    cur = conn.cursor()

    #Population vs Housing Scores of US Cities
    cur.execute('SELECT Scores.city, Scores.HousingScore, Scores.CostOfLivingScore, Population.population FROM Scores INNER JOIN Population ON Scores.city = Population.city')
    results = cur.fetchall()
    pop_list = []
    hscores_list = []
    cscores_list = []
    city_list = []
    for res in results:
        pop_list.append(int(res[3].replace(",","")))
        hscores_list.append(res[1])
        cscores_list.append(res[2])
        city_list.append(res[0])
    
    fig = go.Figure(go.Scatter(
        x=pop_list,
        y=hscores_list,
        marker=dict(color="blue", size=12),
        mode="markers",
        text = city_list, 
        marker_color = "blue"
    ))

    fig.update_traces(mode='markers', marker_line_width=2, marker_size=15)
    fig.update_layout(title='Population vs Housing Scores of U.S Cities', 
                        xaxis_title="Population", 
                        yaxis_title="Housing Scores")
    fig.show()

    #Population vs Cost of Living Scores of US Cities
    fig1 = go.Figure(data = go.Scatter(
        x=pop_list,
        y=cscores_list,
        marker=dict(color="red", size=12),
        mode="markers",
        text = city_list, marker_color = "red"
    ))
    fig1.update_traces(mode='markers', marker_line_width=2, marker_size=15)
    fig1.update_layout(title='Population vs Cost of Living Scores of U.S Cities', 
                        xaxis_title="Population", 
                        yaxis_title="Cost of Living Scores")
    fig1.show()


    #Correlation Between Housing Score and Cost of Living Score in Cities
    cur.execute('SELECT city, HousingScore, CostOfLivingScore FROM Scores')
    results1 = cur.fetchall()
    hscores1_list = []
    cscores1_list = []
    city1_list = []

    for res in results1:
        hscores1_list.append(res[1])
        cscores1_list.append(res[2])
        city1_list.append(res[0])

    fig2 = go.Figure(data = go.Scatter(
        x=hscores1_list,
        y=cscores1_list,
        marker=dict(color="pink", size=12),
        mode="markers",
        text = city1_list, marker_color = "pink"
    ))
    fig2.update_traces(mode='markers', marker_line_width=2, marker_size=15)
    fig2.update_layout(title='Correlation Between Housing Score and Cost of Living Score in Cities', 
                        xaxis_title="Housing Scores", 
                        yaxis_title="Cost of Living Scores")
    fig2.show()

    #Cost of Living in Different Cities
    cur.execute("SELECT Weather.city, Weather.temp, Scores.CostOfLivingScore FROM Weather INNER JOIN Scores ON Weather.city = Scores.city")
    barresults = cur.fetchall()
    cities = []
    costs = []

    for res in barresults:
        cities.append(res[0])
        costs.append(res[2])
    
    barfig = go.Figure([go.Bar(y = costs, x = cities)])
    barfig.update_traces(marker_color = "green", marker_line_color = "purple", marker_line_width = 2, opacity = .7)
    barfig.update_layout(title_text = "Cities Costs of Living", xaxis_title = "Cities", yaxis_title = "Cost of Living Score")
    barfig.show()

    
if __name__ == "__main__":
    main()
