# -*- coding: utf-8 -*-
"""
create dummy data

@author: M.N.Descamps
"""

import pandas as pd
import random
import mysql.connector

#separate file with DB credentials
from my_db_credentials import mydb

""" DATABASE SETTINGS """
INSERT = True

# #db connection information
# mydb = mysql.connector.connect(
#   host=" ",
#   user=" ",
#   passwd=" ",
#   database=" "
# )

#inserts the data tuple into the db
def insertData(location,profession,url,lat,lon):
    mycursor = mydb.cursor()
    sql = "INSERT INTO professionals (location, profession,url,lat,lon) VALUES (%s, %s,%s,%s,%s)"
    val = (location, profession,url,lat,lon)
    mycursor.execute(sql, val)
    mydb.commit()
    #print(mycursor.rowcount, "record inserted.")

#use this function according to your data, or in a loop
#insertData("Paris","Data Analyst","http://devpost.com",48.8667, 2.3333)


""" DATA GENERATION """
print(' **** ')
print(' collect and generate data ')
"""  Europe countries """
eu = pd.read_csv('Europe_countries.csv', sep=',' , na_values=['nan'], na_filter=True)
europe_countries = eu['name'].tolist()
print('europe country loaded')

""" read world city database  """
cities = pd.read_csv('worldcities.csv', sep=',' , na_values=['nan'], na_filter=True)

#filter to only european cities
eu_cities = cities[cities['country'].isin(europe_countries)]
eu_cities = eu_cities.fillna(0)
N_cities = len(eu_cities)
print('cities filtered')

#list of job titles and proportion to total population
jobtitle = ['Data Analyst','Cybersecurity Specialist','Software Developer Python','Software Developer Java']
proportion_jobtitle = [0.000005,0.000002,0.000004,0.000004]

N_jobs = len(jobtitle)
#create the number of talents for each city
talentCount = pd.DataFrame(columns = ['Location','Latitude','Longitude'] + jobtitle)

for i in range(N_cities):
    #print(eu_cities['city'].iloc[i])
    city_info = {'Location':eu_cities['city'].iloc[i], 'Latitude':eu_cities['lat'].iloc[i],'Longitude':eu_cities['lng'].iloc[i]}

    #get the number of talents for each job title
    talent_number = [0]*N_jobs
    for j in range(N_jobs):
        talent_number[j] = int(proportion_jobtitle[j] * eu_cities['population'].iloc[i]* (1 + random.uniform(-0.2,0.2)  ) )

    talent_info = dict(zip(jobtitle,talent_number))
    city_info.update(talent_info)
    talentCount = talentCount.append(city_info,ignore_index=True)

print('length talent %s' % len(talentCount))

talentCount.to_csv('output.csv', index=False)

F = open('db_copy.csv','w')
F.write('Location,Job Title,url,Latitude,Longitude\n')

if INSERT == True:
    print(' **** ')
    print('insert to DB')
    db_copy_csv = pd.DataFrame(columns=['Location', 'Job Title','url','Latitude','Longitude'])
    iter=0
    for i in range(N_cities):
        location = talentCount['Location'].iloc[i]
        latitude = str(talentCount['Latitude'].iloc[i])
        longitude = str(talentCount['Longitude'].iloc[i])
        #print(location)
        for j in range(N_jobs):
            iteration = talentCount[jobtitle[j]].iloc[i]

            for k in range(iteration):
                F.write('%s,%s,%s,%s,%s\n' %(location,
                                             jobtitle[j],
                                             "http://devpost.com",
                                             latitude,
                                             longitude))
                #insertData(location,jobtitle[j],"http://devpost.com",latitude,longitude)
    F.close()
