import datetime
import operator
import sqlite3

conn = sqlite3.connect('nfl_db')
c = conn.cursor()

now = datetime.datetime.now()

year = int(input('Enter the Year:'))
while year < 1970 or year > now.year-1:
    year = int(
        # alterar
        input('The Year must be higher then 1969 and lower than ' + str(now.year-1) + '! Enter the Starting Year:'))



query = c.execute(
    """SELECT T.name,Y.year, S.touchdowns, S.interceptions, S.yards, S.attempts, S.completions,Y.champions FROM Stats S JOIN Year Y, Team T WHERE Y.id = S.id_year AND T.id = S.id_team AND Y.year = '%s' ORDER BY T.name""" % (year))

teams = []
touchdowns = []
completionsPercentage = []
interceptions = []
for row in query:
    champion = row[7]
    if row[0] not in teams:
        teams.append((row[0]))
    touchdowns.append(int(row[2]))
    interceptions.append(int(row[3]))
    completionsPercentage.append(int(row[6])/int(row[5]))

teamsScores = {}
i=0
for team in teams:
    # Percentagem de Passes completos * touchdowns / percentagem de passes falhados * interceptions
    scoreTeamYear = (completionsPercentage[i] * touchdowns[i]) - ((1 - completionsPercentage[i]) * interceptions[i])
    i = i+1
    teamsScores[team] = round(scoreTeamYear,2)

sortedScores = sorted(teamsScores.items(), key=lambda x: x[1],reverse=True)[:10]
i=0
print(year,'Super Bowl Champions:',champion)
for key, value in sortedScores:
    i=i+1
    print(i,'- '+key, ' : ', value)




