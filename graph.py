import matplotlib.pyplot as plt
import datetime
import pandas as pd
import sqlite3

now = datetime.datetime.now()

# Database Connection
conn = sqlite3.connect('nfl_db')
c = conn.cursor()

# User input
year = int(input('Enter the Year:'))

# Check if input is within data range
while year < 1973 or year > now.year-1:
    year = int(
        # alterar
        input('The Year must be higher then 1973 and lower than ' + str(now.year-1) + '! Enter the Starting Year:'))
start = year-3

# Query to get data between chosen date and 3 years earlier
query = c.execute(
    """SELECT T.name,Y.year, S.touchdowns, S.interceptions, S.yards, S.attempts, S.completions FROM Stats S JOIN Year Y, Team T WHERE Y.id = S.id_year AND T.id = S.id_team AND year BETWEEN '%s' AND '%s' ORDER BY T.name""" % (start,year))

# Arrays initialization
teams = []
years = []
touchdowns = []
completionsPercentage = []
interceptions = []
yards = []
interval = 4
j=0

# Get Data from every row in query and save it in the arrays
for row in query:
    if row[0] not in teams:
        teams.append((row[0]))
    if (int(row[1])) not in years:
        years.append(int(row[1]))
    touchdowns.append(int(row[2]))
    interceptions.append(int(row[3]))
    yards.append(int(row[4]))
    completionsPercentage.append(int(row[6])/int(row[5]))

# Save data by data
for team in teams:
    touchdowns_team = []
    interceptions_team = []
    yards_team = []
    completionsPercentage_team = []
    for i in range(j, j+4):
        touchdowns_team.append(touchdowns[i])
        interceptions_team.append(interceptions[i])
        yards_team.append(yards[i])
        completionsPercentage_team.append(completionsPercentage[i])
    j = j+4

    # Create Dataframe with arrays data
    df = pd.DataFrame({'x': years, 'touchdowns': touchdowns_team, 'interceptions': interceptions_team, 'yards': yards_team, 'Completion Percentage': completionsPercentage_team})


    # Graph Styles
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')

    num = 0

    # Clear Graphs
    plt.clf()

    #   Create the 4 graphs
    for column in df.drop('x', axis=1):
        num += 1

        # plt.tight_layout(pad=0.01, h_pad=0.05, w_pad=0.5, rect=None)
        plt.rc('xtick', labelsize=7)
        plt.rc('ytick', labelsize=7)
        # Find the right spot on the plot
        plt.subplot(2, 2, num)

        plt.locator_params(axis='x', nbins=4)

        # Plot the lineplot
        plt.plot(df['x'], df[column], marker='', color='red', linewidth=1, alpha=0.9, label=column)

        # Same limits for every chart
        plt.xlim(years[0], years[3])
        plt.ylim(0, max(df[column]))

        # Add title
        plt.title(column, loc='left', fontsize=8, fontweight=0, color='red')

        # general title
        plt.suptitle("\n"+team, fontsize=13, fontweight=5, color='red',
                     style='normal', y=1.02)

    # save the graph
    plt.savefig(team+'.png')

