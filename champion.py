import datetime
import operator
import sqlite3

#database Connection
conn = sqlite3.connect('nfl_db')
c = conn.cursor()

now = datetime.datetime.now()

# input from user
year = int(input('Enter the Year:'))

# check user input
while year < 1970 or year > now.year-1:
    year = int(
        # alterar
        input('The Year must be higher then 1969 and lower than ' + str(now.year-1) + '! Enter the Starting Year:'))

#query the database with the chosen year
query = c.execute(
    """SELECT T.name,Y.year, S.touchdowns, S.interceptions, S.yards, S.attempts, S.completions,Y.champions FROM Stats S JOIN Year Y, Team T WHERE Y.id = S.id_year AND T.id = S.id_team AND Y.year = '%s' ORDER BY T.name""" % (year))

#Arrays initalization
teams = []
touchdowns = []
completionsPercentage = []
interceptions = []

#get data from every team
for row in query:
    champion = row[7]
    if row[0] not in teams:
        teams.append((row[0]))
    touchdowns.append(int(row[2]))
    interceptions.append(int(row[3]))
    completionsPercentage.append(int(row[6])/int(row[5]))

#initialize Score dictionary
teamsScores = {}
i=0
for team in teams:
    # Completed pass percentage * touchdowns - failed pass percentage * interceptions
    scoreTeamYear = (completionsPercentage[i] * touchdowns[i]) - ((1 - completionsPercentage[i]) * interceptions[i])
    i = i+1
    #save score rounded by team
    teamsScores[team] = round(scoreTeamYear,2)

#sort the scores by Top10
sortedScores = sorted(teamsScores.items(), key=lambda x: x[1],reverse=True)[:10]
i=0

#Show Superbowl Champion for the year chosen
print(year,'Super Bowl Champions:',champion)
for key, value in sortedScores:
    i=i+1
    #print the top10
    print(i,'- '+key, ' : ', value)




