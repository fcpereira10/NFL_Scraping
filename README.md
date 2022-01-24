# NFL Passing Stats Scraping and Top 10 champions candidates calculation
Processing of Information Course - ISPGAYA

## [1st Project](https://github.com/fcpereira10/NFL_Scraping/blob/d332ebacc8c3f7825972c70f81b348cbaee23dc0/main.py)
1. Scraping NFL Offense Passing Teams Stats from NFL.com (https://www.nfl.com/stats/team-stats/offense/passing/2021/reg/all) by years chosen by user
2. Save in SQLite database

## 2nd Project
1. [Creating Graphs of the Stats by Team](https://github.com/fcpereira10/NFL_Scraping/blob/d332ebacc8c3f7825972c70f81b348cbaee23dc0/graph.py)
Example graph of Packers Stats from 2007 to 2010:

![alt text](https://github.com/fcpereira10/NFL_Scraping/blob/master/Packers.png)

2. [Calculate the TOP10 based on stats](https://github.com/fcpereira10/NFL_Scraping/blob/d332ebacc8c3f7825972c70f81b348cbaee23dc0/champion.py)

After analyzing the graphs the optimal formula to calculate the top is:
> (Completed pass percentage * touchdowns) - (failed pass percentage * interceptions)
