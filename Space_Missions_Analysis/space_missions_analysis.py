import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# These might be helpful:
from iso3166 import countries
from datetime import datetime, timedelta

# %% [markdown]
# ### Notebook Presentation

# %%
pd.options.display.float_format = '{:,.2f}'.format

# %% [markdown]
# ### Load the Data

# %%
df_data = pd.read_csv('mission_launches.csv')

# %% [markdown]
# # Preliminary Data Exploration
# 
# * What is the shape of `df_data`? 
# * How many rows and columns does it have?
# * What are the column names?
# * Are there any NaN values or duplicates?

# %%
df_data.shape
df_data.index
df_data.columns
df_data.rename(columns = {'Date':'Date_Time'}, inplace = True)



# %%
df_data.duplicated()
df_data.isnull()



# %% [markdown]
# ## Data Cleaning - Check for Missing Values and Duplicates
# 
# Consider removing columns containing junk data. 

# %%
df_data.drop('Unnamed: 0', axis=1, inplace=True)
df_data.drop('Unnamed: 0.1', axis=1, inplace=True)

df_data = df_data.dropna(how='all')

df_data["Price"] = [float(str(i).replace(",", "")) for i in df_data["Price"]]
price_mean=df_data['Price'].astype(float).mean()
df_data['Price'].fillna(price_mean, inplace=True)

df_data.head()



# %%
df_data.drop_duplicates(keep='first', inplace=True)
df_data.shape
# df_data.info()

# %% [markdown]
# ## Descriptive Statistics

# %%
#data processing
df_data['DateTime'] = pd.to_datetime(df_data['Date_Time'])
#getting the launch year
df_data['Year'] = df_data['DateTime'].apply(lambda datetime: datetime.year)
#getting the country of launch
df_data["Country"] = df_data["Location"].apply(lambda location: location.split(", ")[-1])
#getting the launch day of week
df_data['Day']= df_data['Date_Time'].apply(lambda date: date.split()[0])
#getting the month of launch
df_data['Month']= df_data['Date_Time'].apply(lambda date: date.split()[1])
#getting the date of launch ( in a month )
df_data['Date']=df_data['Date_Time'].apply(lambda datum: datum.split()[2][:2]).astype(int)
#getting the hour of launch
df_data['Hour']= df_data['Date_Time'].apply(lambda datum: int(datum.split()[-2][:2]) if datum.split()[-1]=='UTC' else np.nan)

df_data.head()

# %%
list_countries = {'Gran Canaria': 'USA', 
                'Barents Sea': 'Russian Federation',
                'Russia': 'Russian Federation',
                'Pacific Missile Range Facility': 'USA', 
                'Shahrud Missile Test Site': 'Iran, Islamic Republic of', 
                'Yellow Sea': 'China', 
                'New Mexico': 'USA',
                'Iran': 'Iran, Islamic Republic of',
                'North Korea': "Korea, Democratic People's Republic of",
                'Pacific Ocean': 'United States Minor Outlying Islands',
                 'South Korea': 'Korea, Republic of'}
for country in list_countries:
    df_data.Country = df_data.Country.replace(country, list_countries[country])

df_data.head()


# %% [markdown]
# # Number of Launches per Company
# 
# Create a chart that shows the number of space mission launches by organisation.

# %%


# %%
plt.figure(figsize=(18,8))
plt.bar(df_data["Organisation"].value_counts().index, df_data["Organisation"].value_counts())
plt.xticks(df_data["Organisation"].value_counts().index, rotation=90)
plt.xlabel('organisations')
plt.ylabel('num of launches')

plt.show()

# %% [markdown]
# # Number of Active versus Retired Rockets
# 
# How many rockets are active compared to those that are decomissioned? 

# %%


# %%
plt.bar(df_data["Rocket_Status"].value_counts().index, df_data["Rocket_Status"].value_counts())
plt.xticks(df_data["Rocket_Status"].value_counts().index)
plt.xlabel('Rocket_Status')
plt.ylabel('Num Of Rockets')

plt.show()

# %% [markdown]
# # Distribution of Mission Status
# 
# How many missions were successful?
# How many missions failed?

# %%
plt.figure(figsize=(10,6))
ax = sns.countplot(x="Mission_Status", data=df_data, order=df_data["Mission_Status"].value_counts().index, palette="pastel")
ax.axes.set_title("Distribution of Mission Status",fontsize=18)
ax.set_xlabel("Mission Status",fontsize=16)
ax.set_ylabel("Count",fontsize=16)
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.show()

# %%


# %% [markdown]
# # How Expensive are the Launches? 
# 
# Create a histogram and visualise the distribution. The price column is given in USD millions (careful of missing values). 

# %%
plt.figure(figsize=(10,6))
sns.distplot(df_data.Price, hist=False, rug=True)


# %%



# %% [markdown]
# # Use a Choropleth Map to Show the Number of Launches by Country
# 
# * Create a choropleth map using [the plotly documentation](https://plotly.com/python/choropleth-maps/)
# * Experiment with [plotly's available colours](https://plotly.com/python/builtin-colorscales/). I quite like the sequential colour `matter` on this map. 
# * You'll need to extract a `country` feature as well as change the country names that no longer exist.
# 
# Wrangle the Country Names
# 
# You'll need to use a 3 letter country code for each country. You might have to change some country names.
# 
# * Russia is the Russian Federation
# * New Mexico should be USA
# * Yellow Sea refers to China
# * Shahrud Missile Test Site should be Iran
# * Pacific Missile Range Facility should be USA
# * Barents Sea should be Russian Federation
# * Gran Canaria should be USA
# 
# 
# You can use the iso3166 package to convert the country names to Alpha3 format.

# %%
def iso(country):
    return countries.get(country).alpha3
df_data['ISO'] = df_data.Country.apply(lambda country: iso(country))

# %%
iso = df_data.ISO.value_counts()
px.choropleth(df_data, locations=iso.index, color=iso.values, hover_name=iso.index, title='Number of Lauches', color_continuous_scale="Viridis")

# %% [markdown]
# # Use a Choropleth Map to Show the Number of Failures by Country
# 

# %%
Failures_data = df_data[df_data['Mission_Status']=='Failure']
failures = Failures_data.groupby(['ISO'])['Mission_Status'].value_counts()
country = [ country[0] for country in failures.index]
px.choropleth(df_data, locations=country, color=failures.values, hover_name=country, title='Number Of Failures', color_continuous_scale="redor")


# %%


# %% [markdown]
# # Create a Plotly Sunburst Chart of the countries, organisations, and mission status. 

# %%
fig = px.sunburst(df_data, path = ["ISO", "Organisation", "Mission_Status"], values = "Year", title = "Sunburst Chart")
fig.show()

# %%


# %%


# %% [markdown]
# # Analyse the Total Amount of Money Spent by Organisation on Space Missions

# %%
df_data.head(1)

# %%
# spaceX = df_data[df_data['Organisation']=='SpaceX']
RVSN_USSR = df_data[df_data['Organisation']=='RVSN USSR']
RVSN_USSR.groupby(['Organisation'])['Price'].sum()
# spaceX.groupby(['Organisation'])['Price'].sum()
total_amount = df_data.groupby(["Organisation"])['Price'].sum()
total_amount



# %%
plt.figure(figsize=(18,8))
plt.bar(total_amount.index, total_amount.values)
plt.xticks(total_amount.index, rotation=90)
plt.xlabel('organisations')
plt.ylabel('total amount')
plt.show()

# %% [markdown]
# # Analyse the Amount of Money Spent by Organisation per Launch

# %%
df_data.head(1)

# %%
amount_per_launch = df_data.groupby(["Organisation"])['Price'].mean()
amount_per_launch

# %%
plt.figure(figsize=(18,8))
plt.bar(amount_per_launch.index, amount_per_launch.values)
plt.xticks(amount_per_launch.index, rotation=90)
plt.xlabel('organisations')
plt.ylabel('total amount')
plt.show()

# %% [markdown]
# # Chart the Number of Launches per Year

# %%
df_data.head(1)

# %%
plt.figure(figsize=(22,6))
ax = sns.countplot(x=df_data['Year'])
ax.axes.set_title("Year vs. Number of Launches",fontsize=14)
ax.set_xlabel("Year", fontsize=16)
plt.xticks(rotation=45, ha='right')
ax.set_ylabel("Number of Launches",fontsize=16)
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.show()

# %% [markdown]
# # Chart the Number of Launches Month-on-Month until the Present
# 
# Which month has seen the highest number of launches in all time? Superimpose a rolling average on the month on month time series chart. 

# %%
plt.figure(figsize=(22,6))
ax = sns.countplot(x=df_data['Month'])
ax.axes.set_title("Month vs. Number of Launches",fontsize=14)
ax.set_xlabel("Month", fontsize=16)
plt.xticks(rotation=45, ha='right')
ax.set_ylabel("Number of Launches",fontsize=16)
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.show()

# %%


# %% [markdown]
# # Launches per Month: Which months are most popular and least popular for launches?
# 
# Some months have better weather than others. Which time of year seems to be best for space missions?

# %%
most_popular = df_data['Month'].value_counts()
print(f'December is the most popular for launches')
most_popular.max()

# %%
least_popular = df_data['Month'].value_counts()
print(f'January is the least popular for launches')
least_popular.min()

# %% [markdown]
# # How has the Launch Price varied Over Time? 
# 
# Create a line chart that shows the average price of rocket launches over time. 

# %%
avg_price_per_year = df_data.groupby('Year')['Price'].mean()
avg_price_per_year

# %%

fig = px.line(avg_price_per_year, x=avg_price_per_year.index, y=avg_price_per_year.values, title='average price of rocket launches')
fig.show()

# %% [markdown]
# # Chart the Number of Launches over Time by the Top 10 Organisations. 
# 
# How has the dominance of launches changed over time between the different players? 

# %%
Top_Organisations = df_data['Organisation'].value_counts().head(11)
Number_Of_Launches = Top_Organisations.values
Top_Organisation =Top_Organisations.index

# %%

fig = px.bar(Top_Organisations, x=Top_Organisation, y=Number_Of_Launches, color ='Organisation')
fig.show()


# %% [markdown]
# # Cold War Space Race: USA vs USSR
# 
# The cold war lasted from the start of the dataset up until 1991. 

# %%
USA = df_data[df_data['ISO'] == 'USA'].count()
USA

# %%

RUS = df_data[df_data['ISO'] == 'RUS'].count()

RUS.Mission_Status


# df_data['ISO'].unique()


# %% [markdown]
# ## Create a Plotly Pie Chart comparing the total number of launches of the USSR and the USA
# 
# Hint: Remember to include former Soviet Republics like Kazakhstan when analysing the total number of launches. 

# %%
USSR_VS_USA_DF = df_data[(df_data['ISO']== 'USA') | (df_data['ISO']== 'RUS') | (df_data['ISO']== 'KAZ')]
grouped = USSR_VS_USA_DF.groupby(['ISO'])['Mission_Status'].count()
grouped.values

# %%
fig = px.pie(grouped, values=grouped.values, names=grouped.index)
fig.show()


# %% [markdown]
# ## Create a Chart that Shows the Total Number of Launches Year-On-Year by the Two Superpowers

# %%
USSR_VS_USA_DF = df_data[(df_data['ISO']== 'USA') | (df_data['ISO']== 'RUS')]
USSR_VS_USA_DF.head(5)


# %%
plt.figure(figsize=(18,5))
ax = sns.countplot(x='Year',hue="ISO",data= USSR_VS_USA_DF)
ax.axes.set_title("Total Number of Launches Year-On-Year by the Two Superpowers",fontsize=14)
ax.set_xlabel("Year",fontsize=16)
ax.set_ylabel("Number of Launches",fontsize=16)
ax.tick_params(labelsize=12)
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.ylim(0,100)
plt.show()

# %% [markdown]
# ## Chart the Total Number of Mission Failures Year on Year.

# %%
Failure_DF = USSR_VS_USA_DF[(df_data['Mission_Status'] == 'Failure') | (df_data['Mission_Status'] == 'Partial Failure')|(df_data['Mission_Status'] == 'Prelaunch Failure')]


# %%
plt.figure(figsize=(18,5))
ax = sns.countplot(x='Year',hue="Mission_Status",data= Failure_DF)
ax.axes.set_title("Total Number of Mission Failures Year on Year",fontsize=14)
ax.set_xlabel("Year",fontsize=16)
ax.set_ylabel("Number of Launches",fontsize=16)
ax.tick_params(labelsize=12)
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.ylim(0,100)
plt.show()

# %% [markdown]
# ## Chart the Percentage of Failures over Time
# 
# Did failures go up or down over time? Did the countries get better at minimising risk and improving their chances of success over time? 

# %%

Failure_Percentage_DF= pd.DataFrame(Failure_DF.groupby(['Year'])['Mission_Status'].value_counts())
Failure_Percentage_DF = Failure_Percentage_DF.reset_index(level=[0,0])
Failure_Percentage_DF
x = pd.DataFrame(Failure_Percentage_DF.groupby(['Year'])['Mission_Status'].sum())
x = x.reset_index(level=[0,0])


# %%
plt.figure(figsize=(18,8))
plt.bar(x['Year'], x['Mission_Status'])
plt.xticks(x['Year'], rotation=90)
plt.xlabel('Year')
plt.ylabel('Percentage of Failures')

plt.show()

# %%


# %% [markdown]
# # For Every Year Show which Country was in the Lead in terms of Total Number of Launches up to and including including 2020)
# 
# Do the results change if we only look at the number of successful launches? 

# %%
country_df = pd.DataFrame(df_data.groupby(["Country", "Year"])["Location"].count())
country_df = country_df.reset_index(level=[0,1])

# %%

fig = px.bar(country_df, x='Year', y='Location', color ='Country')
fig.show()

# %% [markdown]
# # Create a Year-on-Year Chart Showing the Organisation Doing the Most Number of Launches
# 
# Which organisation was dominant in the 1970s and 1980s? Which organisation was dominant in 2018, 2019 and 2020? 

# %%
organisation_df = pd.DataFrame(df_data.groupby(["Organisation", "Year"])["Location"].count())
organisation_df = organisation_df.reset_index(level=[0,1])

# %%
fig = px.bar(organisation_df, x='Year', y='Location', color ='Organisation')
fig.show()


