import datetime
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import sqlite3

conn = sqlite3.connect('nfl_db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Team (name)')
c.execute('CREATE TABLE IF NOT EXISTS Year (year)')
c.execute(
    'CREATE TABLE IF NOT EXISTS Stats (attempts, completions, yards, touchdowns, interceptions, id_team INTEGER REFERENCES Team(id), id_year INTEGER REFERENCES Year(id))')
conn.commit()
check = False

now = datetime.datetime.now()
start = int(input('Enter the Starting Year:'))
if start < 1970 or start > now.year:
    start = int(input('The Year must be higher then 1969! Enter the Starting Year:'))

end = int(input('Enter the Ending Year:'))
if end > now.year:
    end = int(input('The maximum year is '+ now.year +'! Enter the Ending Year:'))

years = []
y = start
i = 0
while y <= end:

    url = 'https://www.nfl.com/stats/team-stats/offense/passing/' + str(y) + '/reg/all'
    print(str(y) + ' NFL Season successfully Scraped')
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    table = soup.find('table', {
        'd3-o-table d3-o-table--detailed d3-o-team-stats--detailed d3-o-table--sortable {sortlist: [[0,0]], sortinitialorder: \'asc\'}'})

    # STATS TABLE
    attempts = []
    completions = []
    yards = []
    touchdowns = []
    interceptions = []
    yearsId = []
    teamsId = []

    # TEAMS TABLE
    teams = []

    years.append(str(y))

    dfy = pd.DataFrame({'year': years}, columns=['year'])
    dfy.to_sql('Year', conn, if_exists='replace', index=True, index_label='id')
    c.execute("SELECT id FROM Year WHERE year=" + str(y))
    dfy = pd.DataFrame(c.fetchall(), columns=['id'])

    for row in table.find_all('tr')[1:]:
        data = row.find_all('td')
        team = data[0].text.strip().split("\n", 1)[0]
        if not team in teams:
            teams.append(team)
        attempts.append(data[1].text.strip())
        completions.append(data[2].text.strip())
        yards.append(data[5].text.strip())
        touchdowns.append(data[6].text.strip())
        interceptions.append(data[7].text.strip())
        yearsId.append(int(float(dfy["id"][0])))
        dft = pd.DataFrame({'name': teams}, columns=['name'])
        dft.to_sql('Team', conn, if_exists='replace', index=True, index_label='id')
        c.execute("SELECT id FROM Team WHERE name=\'" + team+"\'")
        dft = pd.DataFrame(c.fetchall(), columns=['id'])
        teamsId.append(int(float(dft["id"][0])))


    # Dataframe Team to SQL


    # Dataframe Year to SQL


    # Dataframe Stats to SQL
    dfs = pd.DataFrame.from_dict({'attempts': attempts, 'completions': completions, 'yards': yards,
                                  'touchdowns': touchdowns, 'interceptions': interceptions, 'id_team': teamsId, 'id_year': yearsId}, orient='index')
    dfs = dfs.transpose()
    #dfs.insert(5, 'id_team', id_team)
    #dfs.insert(6, 'id_year', id_year)

    if not check:
        dfs.to_sql('Stats', conn, if_exists='replace', index=False)
        check = True
    else:
        dfs.to_sql('Stats', conn, if_exists='append', index=False)
    i += 1
    y += 1


