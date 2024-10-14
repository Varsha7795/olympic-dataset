# Importing Libraries
import matplotlib
import numpy as np                                          # Implemennts milti-dimensional array and matrices
import pandas as pd                                         # For data manipulation and analysis

import matplotlib.pyplot as plt                             # Plotting library for Python programming language and it's numerical mathematics extension NumPy
import seaborn as sns                                       # Provides a high level interface for drawing attractive and informative statistical graphics
from pandas.testing import assert_frame_equal

#from pandas._testing import at

sns.set()

from subprocess import check_output
olympic = pd.read_csv("https://raw.githubusercontent.com/insaid2018/Term-1/master/Data/Projects/summer%20olympics.csv")
olympic.shape
olympic.head()
olympic.info()

olympic.describe(include='all')
# Fetching Mode over Country column
olympic.Country.mode()
# Replacing missing Country column values with Mode
olympic.Country.fillna('USA', inplace=True)

olympic.columns = map(str.lower, olympic.columns)
# map() function returns a list of results after applying the given function to each item of a given iterable.
olympic.dtypes



# Dropping duplicates
olympic.drop_duplicates(inplace=True)
def missing_data(data):
    total = data.isnull().sum().sort_values(ascending = False)
    percent = (data.isnull().sum()/data.isnull().count()*100).sort_values(ascending = False)
    return pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data(olympic)

#Most Medals in Summer Olympics
data = olympic.groupby(['discipline','year'])['medal'].value_counts()
sns.set(color_codes=True)
sns.set_palette(sns.color_palette("muted"))
sns.countplot(y='year', hue='medal', data=olympic).set_title('Count plot for medals in summer olympics')

# Discipline with maximum medals
olympic.groupby(['discipline','medal'])['medal'].value_counts().sort_values(ascending=False)


#1 How many events do we have thus far, in Olympics(1)
print("There are {} unique sports thus far, in Olympics". format(olympic["sport"].nunique()))

#Not all of the above sports were part of Olympics starting 1896.
#2 Let us find out which year the sport was inducted into Olympics(2)
olympic.groupby("sport")["year"].min().sort_values().reset_index()
df_sports = olympic[olympic["year"]<1950].groupby("sport")["year"].min().sort_values(ascending=False).reset_index()
plt.figure(figsize=(15,20))
plt.xlim(1700,1950)
sns.barplot(x = "year", y = "sport", hue="year", data=df_sports)
plt.show()

#3. What is the number of Sports held per year in Summer Olypics, since 1896?(3)
#Let us summarize number of "Sports" held per year, starting 1896
df_sports = olympic.groupby("year")["sport"].nunique().sort_values(ascending=False).reset_index()
fig = plt.figure(figsize=(30,10))
fig.add_subplot(111)
sns.barplot(x = "year", y = "sport", data=df_sports, palette="summer", saturation=.65 )
plt.title("number of Sports held per year in Summer Olypics")
plt.show()

#4 Top 5 countries to win most Gold medals across all seasons collectively(11)
olympic[(olympic['medal'] == 'Gold')]['country'].value_counts().reset_index(name='medal').head(5)
totalGoldMedals = olympic[(olympic['medal'] == 'Gold')]['country'].value_counts().reset_index(name='medal').head(5)
g = sns.catplot(x="index", y="medal", data=totalGoldMedals,
                height=6, kind="bar", palette="muted")
g.despine(left=True)
g.set_xlabels("Top 5 countries")
g.set_ylabels("Number of Medals")
plt.title('Medals per Country')
plt.show()

#Adding id to the dataset, for analysis
olympic['id'] = range(0, len(olympic))
olympic.head(5)

#5 Overall Gender Distribution for Summer Olympics(5)
plt.figure(figsize=(13,6))
olympic.groupby("gender")["id"].nunique().plot.pie(autopct = "%1.0f%%",
                                               wedgeprops = {"linewidth":2,"edgecolor":"w"},
                                              explode = [0,.01],shadow = True ,
                                               colors = ["royalblue","lawngreen"])
plt.ylabel("")
circ = plt.Circle((0,0),.7,color = "white")
plt.gca().add_artist(circ)
plt.title("SUMMER OLYMPICS -overall gender distribution")
plt.show()

#6 How many Cities are there since 1896?(6)
print("There are {} cities in whicn Olympics was conducted since 1896".format (olympic["city"].value_counts().nunique()))

#How many cities in which Olympics was conducted more than once?
olympic.groupby(["city"])["year"].nunique().sort_values(ascending=False)

#Which country won the most Gold medals, in each of the Olympics?
df_sports  = olympic[olympic["medal"]=="Gold"].groupby(["year","country"], as_index=False)["id"].count().rename(
    columns={"id":"total"})
df_sports.iloc[df_sports.groupby(["year"])["total"].idxmax()]


#7 How many medals were won by women in Summer Olympics(8)?
womenInOlympics = olympic[(olympic['gender'] == 'Women')&(olympic['medal'] == 'Gold')]
womenInOlympics.groupby(['year'])['medal'].value_counts().sort_values(ascending=False)
#Women - medals per edition of the Games
#womenInOlympics = olympic[(olympic['Gender'] == 'Women')&(olympic['Medal'] == 'Gold')]
sns.set(style="darkgrid")
plt.figure(figsize=(20, 10))
sns.countplot(x='year', data=womenInOlympics)
plt.title('Women medals per edition of the Games')
plt.show()

#8 Top 10 Women Athletes - Gold Medals(9)
womenMedalWinners=womenInOlympics.groupby(['athlete'])['medal'].value_counts().sort_values(ascending=False)
womenMedalWinners.head(10)
totalWomenGoldMedalAthlete = olympic[(olympic['medal'] == 'Gold') & (olympic['gender'] == 'Women')]['athlete'].value_counts().reset_index(name='athlete').head(10)
g = sns.catplot(y="index", x="athlete", data=totalWomenGoldMedalAthlete,
                height=6, kind="bar", palette="muted")
g.despine(left=True)
g.set_xlabels("Number of Medals")
g.set_ylabels("Top 10 Women Athlete")
plt.title('Medals per Women Athlete')
plt.show()

# 9 How the number of athletes participation varied along time ?(13.3)
plt.figure(figsize=(19,8))
ax = sns.barplot(x='year', y='country', hue='gender', data=olympic.groupby(['year', 'gender'], as_index=False).count())
ax.set_title('Number of athlete participated through the olympics history and how athletes participation varied along time .')
ax.set_ylabel('Count')
plt.show()


#10 Athletes participation by gender over years for Olympics(21)
sum_gc = olympic.groupby(["year","gender"])["id"].nunique().reset_index()

fig = plt.figure(figsize=(13,16))
ax = sns.pointplot(x = sum_gc["year"] , y = sum_gc["id"],
                   markers="h" , hue = sum_gc["gender"],palette = ["r","b"])
plt.grid(True)
plt.xticks(rotation = 60)
ax.set_facecolor("lightgrey")
plt.ylabel("count")
plt.title("Athletes by gender over years for Summer Olympics",color="b")
plt.legend(loc = "best" ,prop={"size":15})
plt.show()

#11 . What is the YoY growth of Athlete participation in each Summer Olympic game?(17)
summer_games_athletes = olympic.pivot_table(olympic, index=['year'], aggfunc=lambda x: len(x.unique())).reset_index()[['year','id']]
summer_games_athletes['id1'] = summer_games_athletes['id'].shift(1)
summer_games_athletes['growth'] = ((summer_games_athletes['id']-summer_games_athletes['id1']))/summer_games_athletes['id1']
summer_games_athletes.dropna(inplace=True)

fig, ax = plt.subplots(figsize=(22,6))
a = sns.barplot(x='year', y='growth', data=summer_games_athletes, ax=ax, color="palegreen")
a.set_xticklabels(labels=summer_games_athletes['year'],rotation=90)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2, p.get_height(), '{:,.1%}'.format(p.get_height()),
            fontsize=12, color='black', ha='center', va='bottom')

ax.set_xlabel('Olympic Summer Game', size=14, color="green")
ax.set_ylabel('Growth of number of Athletes', size=14, color="green")
ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
ax.set_title('YoY growth of Athlete participation in each Summer Olympic game', size=18, color="green")

plt.show()

#12 . USA Medals in Sports across Years(20.1)
t3_summer = olympic[(olympic['country'].isin(['USA'])) & (olympic['medal']!='No Medal')]
t3_summer = pd.pivot_table(t3_summer, index=['sport'], columns=['year'], values=['id'],  aggfunc=len, fill_value=0)
t3_summer = t3_summer.reindex(t3_summer['id'].sort_values(by=2012, ascending=False).index)

f, ax = plt.subplots(figsize=(20, 20))
sns.heatmap(t3_summer, annot=True, linewidths=0.05, ax=ax, cmap="RdYlGn")
ax.set_xlabel('Summer Game Year', size=14, color="green")
ax.set_ylabel('Sports', size=14, color="green")
ax.set_title('[Heatmap] USA Medals in Sports across Years', size=18, color="green")
plt.show()