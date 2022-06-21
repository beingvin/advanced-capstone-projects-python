
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# This might be helpful:
from collections import Counter

"""## Notebook Presentation"""

pd.options.display.float_format = '{:,.2f}'.format

"""## Load the Data"""

df_hh_income = pd.read_csv('Median_Household_Income_2015.csv', encoding="windows-1252")
df_pct_poverty = pd.read_csv('Pct_People_Below_Poverty_Level.csv', encoding="windows-1252")
df_pct_completed_hs = pd.read_csv('Pct_Over_25_Completed_High_School.csv', encoding="windows-1252")
df_share_race_city = pd.read_csv('Share_of_Race_By_City.csv', encoding="windows-1252")
df_fatalities = pd.read_csv('Deaths_by_Police_US.csv', encoding="windows-1252")

"""# Preliminary Data Exploration

* What is the shape of the DataFrames? 
* How many rows and columns do they have?
* What are the column names?
* Are there any NaN values or duplicates?
"""

display(df_hh_income.shape)
display(df_pct_poverty.shape)
display(df_pct_completed_hs.shape)
display(df_share_race_city.shape)
display(df_fatalities.shape)

display(df_hh_income.columns)
display(df_pct_poverty.columns)
display(df_pct_completed_hs.columns)
display(df_share_race_city.columns)
display(df_fatalities.columns)

display('df_hh_income')
display(df_hh_income.isna().sum())
display(df_hh_income.duplicated().sum())
display(print('\n'))

display(print('df_pct_poverty'))
display(df_pct_poverty.isna().sum())
display(df_pct_poverty.duplicated().sum())
display(print('\n'))

display(print('df_pct_completed_hs'))
display(df_pct_completed_hs.isna().sum())
display(df_pct_completed_hs.duplicated().sum())
display(print('\n'))

display(print('df_share_race_city'))
display(df_share_race_city.isna().sum())
display(df_share_race_city.duplicated().sum())
display(print('\n'))


display(print('df_fatalities'))
display(df_fatalities.isna().sum())
display(df_fatalities.duplicated().sum())

"""## Data Cleaning - Check for Missing Values and Duplicates

Consider how to deal with the NaN values. Perhaps substituting 0 is appropriate. 
"""

display(df_hh_income.dropna(how='all'))
display(df_hh_income.drop_duplicates(inplace=True))

display(df_pct_poverty.dropna(how='all'))
display(df_pct_poverty.drop_duplicates(inplace=True))

display(df_pct_completed_hs.dropna(how='all'))
display(df_pct_completed_hs.drop_duplicates(inplace=True))

display(df_share_race_city.dropna(how='all'))
display(df_share_race_city.drop_duplicates(inplace=True))


display(df_fatalities.dropna(how='all'))
display(df_fatalities.drop_duplicates(inplace=True))



"""# Chart the Poverty Rate in each US State

Create a bar chart that ranks the poverty rate from highest to lowest by US state. Which state has the highest poverty rate? Which state has the lowest poverty rate?  Bar Plot
"""

df_pct_poverty[df_pct_poverty['poverty_rate'] == '-'] = '0.0'
df_pct_poverty['poverty_rate'] = df_pct_poverty['poverty_rate'].astype(float)
filter=df_pct_poverty['poverty_rate']>0
grouped=df_pct_poverty.groupby(['Geographic Area'])['poverty_rate'].mean()

fig,ax=plt.subplots(figsize=(15,16))
grouped.sort_values().plot.barh(ax=ax)
plt.title("Poverty Rate in each US State")
plt.show()

"""# Chart the High School Graduation Rate by US State

Show the High School Graduation Rate in ascending order of US States. Which state has the lowest high school graduation rate? Which state has the highest?
"""

df_pct_completed_hs[df_pct_completed_hs['percent_completed_hs'] == '-'] = '0.0'
df_pct_completed_hs[df_pct_completed_hs['percent_completed_hs'] == '-']
df_pct_completed_hs['percent_completed_hs'] = df_pct_completed_hs['percent_completed_hs'].astype(float)
filter = df_pct_completed_hs['percent_completed_hs'] > 0
hs_grouped = df_pct_completed_hs.groupby(['Geographic Area'])['percent_completed_hs'].mean()

fig,ax=plt.subplots(figsize=(15,14))
hs_grouped.sort_values(ascending=False).plot.barh(ax=ax)
plt.title("High School Graduation Rate by US State")
plt.show()

"""# Visualise the Relationship between Poverty Rates and High School Graduation Rates

#### Create a line chart with two y-axes to show if the rations of poverty and high school graduation move together.  
"""



plt.rcParams["figure.figsize"] = [15, 8]
plt.rcParams["figure.autolayout"] = True

ax1 = plt.subplot()
l1, = ax1.plot(grouped.sort_values(), color='red')
ax2 = ax1.twinx()
l2, = ax2.plot(hs_grouped.sort_values(), color='orange')

plt.legend([l1, l2], ["Poverty Rate", "High School Graduation Rate"])
plt.xlabel('US State')
plt.ylabel('Rates')
plt.title("Relationship between Poverty Rates and High School Graduation Rates")
plt.show()

"""#### Now use a Seaborn .jointplot() with a Kernel Density Estimate (KDE) and/or scatter plot to visualise the same relationship"""

Poverty_Rates = sns.jointplot(x=grouped.index, y=grouped.values, height=12)

High_School_Graduation_Rates = sns.jointplot(x=hs_grouped.index, y=hs_grouped.values, height=12)

"""#### Seaborn's `.lmplot()` or `.regplot()` to show a linear regression between the poverty ratio and the high school graduation ratio. """

poverty_ratio = grouped
hs_graduation_ratio = hs_grouped

poverty_ratio_df = pd.DataFrame(poverty_ratio)
poverty_ratio_df =poverty_ratio_df.reset_index(level=[0,0])

hs_graduation_ratio_df = pd.DataFrame(hs_graduation_ratio)
hs_graduation_ratio_df = hs_graduation_ratio_df.reset_index(level=[0,0])
hs_graduation_ratio_df.iloc[0]

update =poverty_ratio_df.merge(hs_graduation_ratio_df, left_index=True, right_index=True)
ratio_df = update.drop(index=0, columns='Geographic Area_y')

ratio_df.rename(columns={'Geographic Area_x':'Geographic Area'}, inplace=True)

ratio_df

ax = sns.lmplot(x="poverty_rate", y="percent_completed_hs", data=ratio_df, hue="Geographic Area")

"""# Create a Bar Chart with Subsections Showing the Racial Makeup of Each US State

Visualise the share of the white, black, hispanic, asian and native american population in each US State using a bar chart with sub sections. 
"""

# convert '(X)' values to '0.0'

df_share_race_city[df_share_race_city['share_white']== "(X)"] = '0.0'
df_share_race_city[df_share_race_city['share_black']== "(X)"] = '0.0'
df_share_race_city[df_share_race_city['share_native_american']== "(X)"] = '0.0'
df_share_race_city[df_share_race_city['share_asian']== "(X)"] = '0.0'

# convert str to float
df_share_race_city.iloc[: , 2:7 ] = df_share_race_city.iloc[: , 2:7 ].astype(float)

df = df_share_race_city.groupby('Geographic area').mean()
Racial_Makeup_df = pd.DataFrame(df)
Racial_Makeup_df = Racial_Makeup_df.reset_index(0,0)
Racial_Makeup_df = Racial_Makeup_df.drop(0)

plt.bar(Racial_Makeup_df['Geographic area'], Racial_Makeup_df['share_white'], color='#f7f7f7')
plt.bar(Racial_Makeup_df['Geographic area'], Racial_Makeup_df['share_black'], color='black')
plt.bar(Racial_Makeup_df['Geographic area'], Racial_Makeup_df['share_native_american'], color='#b9eef0')
plt.bar(Racial_Makeup_df['Geographic area'], Racial_Makeup_df['share_asian'], color='brown')
plt.xticks(Racial_Makeup_df['Geographic area'])
plt.xlabel("US State")
plt.ylabel("Racial Makeup of Each US State")
plt.legend(["white", "black", "native_american", "asian"])
plt.show()

"""# Create Donut Chart by of People Killed by Race

Hint: Use `.value_counts()`
"""

People_Killed_By_Race =df_fatalities['race'].value_counts()

plt.pie(People_Killed_By_Race, labels=People_Killed_By_Race.index)
circle = plt.Circle( (0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(circle)
plt.show()

"""# Create a Chart Comparing the Total Number of Deaths of Men and Women

Use `df_fatalities` to illustrate how many more men are killed compared to women. 
"""

x = df_fatalities['gender'].value_counts()

plt.figure(figsize=(18,8))
plt.bar(x.index, x, color ='red')
plt.xticks(x.index)
plt.xlabel("Gender")
plt.ylabel("Number of Deaths")
plt.title("Total Number of Deaths of Men and Women")
plt.show()
plt.show()

"""# Create a Box Plot Showing the Age and Manner of Death

Break out the data by gender using `df_fatalities`. Is there a difference between men and women in the manner of death? 
"""

df_fatalities.head(1)

ax = sns.boxplot(x="gender", y="age", hue="manner_of_death",
                 data=df_fatalities)



"""# Were People Armed? 

In what percentage of police killings were people armed? Create chart that show what kind of weapon (if any) the deceased was carrying. How many of the people killed by police were armed with guns versus unarmed? 
"""

unarmed = df_fatalities[df_fatalities['armed'] == 'unarmed']
armed = df_fatalities[df_fatalities['armed'] != 'unarmed']

armed_percentage = (len(armed) / len(df_fatalities) ) * 100
unarmed_percentage = (len(unarmed) / len(df_fatalities) ) * 100

print(f"{round(armed_percentage, 2)}% percentage of police killings were people armed")
print(f"{round(unarmed_percentage, 2)}% percentage of police killings were people unarmed")

sns.set_theme(style="darkgrid")
plt.figure(figsize=(10,18))
ax = sns.countplot(y='armed', data=df_fatalities)

with_guns = armed[armed['armed']== 'gun']['armed'].count()
without_armed = unarmed['armed'].count()

print(f"{with_guns} of the people killed by police were armed with guns ")
print(f"{without_armed} of the people killed by police were unarmed")

"""# How Old Were the People Killed?

Work out what percentage of people killed were under 25 years old.
"""

under_25 = df_fatalities[df_fatalities['age'] < 25 ]
percentage_25_years_old  = (len(under_25) / len(df_fatalities)) * 100

print(f"{round(percentage_25_years_old, 2)}% percentage of people killed were under 25 years old")

"""Create a histogram and KDE plot that shows the distribution of ages of the people killed by police. """

sns.histplot(data=df_fatalities, x="age", kde=True)

"""Create a seperate KDE plot for each race. Is there a difference between the distributions? """

g = sns.FacetGrid(data=df_fatalities, hue="race", aspect=3, height=4)
g.map(sns.kdeplot, "age", shade=True)
g.add_legend(title="Race")


g.set_ylabels("Count")
plt.title("Age distribution, by race", fontsize=17)

"""# Race of People Killed

Create a chart that shows the total number of people killed by race. 
"""

df_fatalities.head(2)

sns.set_theme(style="darkgrid")
plt.figure(figsize=(10,5))
ax = sns.countplot(x='race', data=df_fatalities)

"""# Mental Illness and Police Killings

What percentage of people killed by police have been diagnosed with a mental illness?
"""

diagnosed_with_mi=  df_fatalities[df_fatalities['signs_of_mental_illness'] == True]
percentage_of_killings  = (len(diagnosed_with_mi) / len(df_fatalities)) * 100

print(f"{round(percentage_of_killings, 2)} of people killed by police have been diagnosed with a mental illness")

"""# In Which Cities Do the Most Police Killings Take Place?

Create a chart ranking the top 10 cities with the most police killings. Which cities are the most dangerous?  
"""

# method 1 
#Easy method 
 
cities =  df_fatalities.city.value_counts().head(10)
cities.index

plt.figure(figsize=(15,8))
sns.barplot(x=cities.index, y=cities.values)
plt.title("Most dangerous cities", fontsize=17)

# method 2 
# df_fatalities.groupby('city')['city'].count().sort_values(ascending=False).head(10)

# method 3
# df_city = df.filter(["city"], axis=1)
# df_city
# df_city["count"] = 1
# df_city

# grouped_city = df_city.groupby("city", as_index=False,sort=False).sum()
# grouped_city.sort_index(ascending=False)


# grouped_city = grouped_city.sort_values("count", ascending=False).head(10)
# grouped_city                                                      

# plt.figure(figsize=(15,8))
# sns.barplot(data=grouped_city, x="city", y="count")
# plt.title("Most dangerous cities", fontsize=17)

"""# Rate of Death by Race

Find the share of each race in the top 10 cities. Contrast this with the top 10 cities of police killings to work out the rate at which people are killed by race for each city. 
"""

df_fatalities.groupby(['race'])['city'].value_counts(ascending=False)

top_cites = df_fatalities.groupby('city')['city'].count().sort_values(ascending=False).head(10)

top_city_race_df = pd.DataFrame(data={"city": "test",
                         "race": "test","death":0}, index=[0])

city = [ city for city in top_cites.index]
for i in city:
    filter_city_df = df_fatalities[df_fatalities['city'] == i]
    grouped = filter_city_df.groupby(['city'])['race'].value_counts()
    df = pd.DataFrame(grouped)
    df.rename(columns = {'race':'death'}, inplace = True)
    df.reset_index(inplace = True)
    top_city_race_df= top_city_race_df.append(df, ignore_index=True)

top_city_race_df.drop(0,0, inplace=True)

top_city_race_df.tail(20)

ax = sns.barplot(x="city", y="death", hue="race", dodge=False, data=top_city_race_df)

"""# Create a Choropleth Map of Police Killings by US State

Which states are the most dangerous? Compare your map with your previous chart. Are these the same states with high degrees of poverty? 
"""

state = df_fatalities['state'].value_counts()
state

fig = px.choropleth(df_fatalities, locations=state.index, locationmode="USA-states", color=state.values, labels={'color':'Police Killings'}, title='Police Killings by US States', scope="usa")
fig.show()

"""# Number of Police Killings Over Time

Analyse the Number of Police Killings over Time. Is there a trend in the data? 
"""

df_fatalities['date'] = pd.to_datetime(df_fatalities['date'])
df_fatalities['year'] = df_fatalities['date'].dt.year

Killings_Over_Time = df_fatalities.groupby('year')['gender'].count()

ax = sns.barplot(x=Killings_Over_Time.index, y=Killings_Over_Time.values)



"""# Epilogue

Now that you have analysed the data yourself, read [The Washington Post's analysis here](https://www.washingtonpost.com/graphics/investigations/police-shootings-database/).
"""

