import plotly.express as px
import plotly.io as pio
import pandas as pd

import datetime
import math

# Read the data. COVID-19 data is provided by the COVID tracking project.
url1 = "https://api.covidtracking.com/v1/states/daily.csv"
df1 = pd.read_csv(url1, parse_dates = True)
number_of_columns = 14391
print(df1.tail())

# Clean the dataset
df1 = df1[['date', 'state', 'positive', 'death', 'positiveIncrease', 'deathIncrease']]
df1['casesAdj'] = pd.Series()

# Fix the dates / convert them
for i in range (0, number_of_columns):
    s = str(df1['date'][i])
    s_2 = s[0:4] + "-" + s[4:6] + "-" + s[6:8]
    df1['date'][i] = s_2
df1 = df1[::-1]
print(df1.tail())
#df1['date'] = str(pd.to_datetime(df1['date'], format = '%Y%m%d', errors = 'ignore'))[:-2]

# Adjust for population (because states with bigger populations will end up dominating the graph)
state_dict = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
} # This is needed for converting the state names into abbreviations (dictionary is from gist.github.com/rogerallen/1583593)

url2 = "http://www2.census.gov/programs-surveys/popest/datasets/2010-2019/national/totals/nst-est2019-alldata.csv"
pop = pd.read_csv(url2)
pop = pop[['NAME', 'POPESTIMATE2019']]
pop['ShortName'] = pop.NAME.replace(state_dict)
print(pop.head())

for i in range(0, number_of_columns):
    n = df1['positive'][i]
    divider = 1
    
    for j in range (0, 51):
        if (df1['state'][i] == pop['ShortName'][j]):
            divider = pop['POPESTIMATE2019'][j]
            break
    
    n /= divider    
    df1['casesAdj'][i] = round(n, 5);

# Generate the graph
print(df1.tail())
graph = px.choropleth(df1, locations = 'state',
                           color = 'positive',
                           color_continuous_scale = "peach",
                           #range_color=(0, 15000),
                           scope = "usa",
                           animation_frame = 'date',
                           locationmode = 'USA-states',
                           labels = {'Confirmed':'COVID-19 Positive Tests'},
                           hover_data = ["positive", "casesAdj", "death"]
                    )
graph.update_layout(
                    title_text = "COVID Explorer: A visual exploration of COVID-19 cases in the USA"
                    )
graph.show()
