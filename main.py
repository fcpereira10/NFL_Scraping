import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# Connection to database
conn = sqlite3.connect('nfl_db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Team (name)')
c.execute('CREATE TABLE IF NOT EXISTS Year (year)')
c.execute(
    'CREATE TABLE IF NOT EXISTS Stats (id PRIMARY KEY, attempts, completions, yards, touchdowns, interceptions, '
    'id_team INTEGER REFERENCES Team(id), id_year INTEGER REFERENCES Year(id))')
conn.commit()

# User inputs
now = datetime.datetime.now()
start = int(input('Enter the Starting Year:'))
while start < 1970 or start > now.year:
        start = int(
            input('The Year must be higher then 1969 and lower than ' + str(now.year) + '! Enter the Starting Year:'))

end = int(input('Enter the Ending Year:'))
while end > now.year or end < 1970:
        end = int(input('Enter a year lower than ' + str(now.year) + ' and higher than 1970! Enter the Ending Year:'))

check = False  # check if table is already created
years = []  # append all years in array
y = start  # start year
i = 0  # used for getting id in every stat
statsId = []  # get all ids in array

# Loop until end year
while y <= end:

    # URL to scrape
    url = 'https://www.nfl.com/stats/team-stats/offense/passing/' + str(y) + '/reg/all'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', {
        'd3-o-table d3-o-table--detailed d3-o-team-stats--detailed d3-o-table--sortable '
        '{sortlist: [[0,0]], sortinitialorder: \'asc\'}'})

    # Stats data arrays
    attempts = []
    completions = []
    yards = []
    touchdowns = []
    interceptions = []
    yearsId = []
    teamsId = []

    # Teams names array
    teams = []

    # Year array
    years.append(str(y))

    # Dataframe Years to SQL
    dfy = pd.DataFrame({'year': years}, columns=['year'])
    dfy.to_sql('Year', conn, if_exists='replace', index=True, index_label='id')
    c.execute("SELECT id FROM Year WHERE year=" + str(y))
    dfy = pd.DataFrame(c.fetchall(), columns=['id'])

    # loop every row on the table except the header
    for row in table.find_all('tr')[1:]:
        data = row.find_all('td')
        team = data[0].text.strip().split("\n", 1)[0]
        if team not in teams:
            teams.append(team)
        attempts.append(data[1].text.strip())
        completions.append(data[2].text.strip())
        yards.append(data[5].text.strip())
        touchdowns.append(data[6].text.strip())
        interceptions.append(data[7].text.strip())
        yearsId.append(int(float(dfy["id"][0])))

        # add teams to pandas dataframe of teams
        dft = pd.DataFrame({'name': teams}, columns=['name'])
        # put dataframe into SQL database
        dft.to_sql('Team', conn, if_exists='replace', index=True, index_label='id')
        # add id to teams
        c.execute("SELECT id FROM Team WHERE name=\'" + team + "\'")
        dft = pd.DataFrame(c.fetchall(), columns=['id'])
        teamsId.append(int(float(dft["id"][0])))
        # add id to stats
        statsId.append(i)
        i += 1

    # Create Dataframe Stats
    dfs = pd.DataFrame.from_dict({'id': statsId, 'attempts': attempts, 'completions': completions, 'yards': yards,
                                  'touchdowns': touchdowns, 'interceptions': interceptions, 'id_team': teamsId,
                                  'id_year': yearsId}, orient='index')
    dfs = dfs.transpose()

    # Reset Ids
    statsId = []
    yearsId = []
    teamsId = []

    # Dataframe Stats to Database
    if not check:
        dfs.to_sql('Stats', conn, if_exists='replace', index=False)
        check = True
    else:
        dfs.to_sql('Stats', conn, if_exists='append', index=False)

    # Success Message
    print(str(y) + ' NFL Season successfully Scraped')
    y += 1
