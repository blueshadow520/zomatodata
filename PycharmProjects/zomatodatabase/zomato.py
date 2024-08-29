import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.figsize'] = (20, 12)
plt.rcParams["figure.autolayout"] = True

df = pd.read_csv(r"C:\Users\jugal\Desktop\zomatodata.csv", encoding='latin-1')
print(df.shape)  # Printing number of rows and columns
print(df.head())  # Printing first 5 rows of dataset
print(df.columns)  # Printing list of all columns
print(df.info())  # Gives information about data type of rows, and null count of each column
print(df.describe())  # Provides statistical information about each numerical column, like standard deviation, mean, quartiles, etc.

print(df.isnull().sum())  # Printing number of null values in each column
print([features for features in df.columns if df[features].isnull().sum() > 0])  # Printing columns with > 0 null values

plt.bar(df.columns, df.isnull().sum())
plt.xlabel("Columns")
plt.ylabel("Null Count")
plt.xticks(rotation=45)
plt.show()

df_country = pd.read_excel(r"C:\Users\jugal\Downloads\Country-Code.xlsx")  # There are additional columns, containing country codes of each country
print(df_country.head())

final_df = pd.merge(df, df_country, on="Country Code", how="left")  # Adding a Country Code column to dataframe, using merge method of pandas
print(final_df.head())
print([f for f in final_df.columns if final_df[f].isnull().sum() > 0])  # Checking if Country Code has any null values
print(df['Country Code'].dtype)  # Checking data type of country code
print(final_df.columns)  # These are the final columns in df
print(final_df.Country.value_counts())  # India has highest ratings, then US and UK

final_df_numec = final_df.select_dtypes(exclude='object')  # Using select_dtypes to exclude non-numerical values
print(final_df_numec.corr())  # We can see correlation between each column

Country_name = final_df.Country.value_counts().index  # This is list of country names
Country_val = final_df.Country.value_counts().values  # These are the values associated with each country
plt.pie(Country_val[:3], labels=Country_name[:3], autopct='%.2f%%')  # Pie chart showing percentage of ratings of top three countries
plt.show()

# Observation From Above Pie
# Zomato has it maximum records and transactions with India, then US and then UK

ratings = final_df.groupby(['Aggregate rating', 'Rating color', 'Rating text']).size().reset_index().rename(columns={0: 'Rating count'})
print(ratings)

# Observation
# Ratings Range and text
# 4.5 - 4.9 => Excellent, Dark Green
# 4.0 - 4.4 => Very Good, Green
# 3.5 - 4.9 => Good, Yellow
# 2.5 - 3.0 => Average, Orange
# 0.1 - 2.4 => Poor, Red
# 0 => Not Rated, White

print(ratings.head())
plt.bar(ratings['Aggregate rating'], ratings['Rating count'], width=0.07, color='blue')  # We decrease width so that each bar could be visible, otherwise they were overlapping
plt.xlabel("Aggregate rating")
plt.ylabel("Rating count")
plt.show()

# So we can see that most ratings are 0, and other ratings are following a normal distribution

# Observations
# 1) Most of the people have not rated
# 2) Maximum rating is between 2.5-3.4 i.e., average

rating_color_count = final_df.groupby(['Rating color']).size().reset_index().rename(columns={0: "Count"})  # Making a new df which shows count of each rating colour
print(rating_color_count)
colors = ['darkgreen', 'green', 'orange', 'red', 'white', 'yellow']
plt.bar(rating_color_count['Rating color'], rating_color_count['Count'], color=colors, edgecolor='black')  # Using bar graph for the same graph as above
plt.show()

# So we can see that most reviews are Orange, i.e., [2.5,3.0]

plt.hist(final_df['Rating color'], color='blue')  # We can use histogram for categorical data also
plt.show()

# Finding out which country has given zero ratings

country_with_zero_rating_count = final_df[final_df['Rating color'] == 'White'].groupby(['Country']).size().reset_index().rename(columns={0: 'Country count'})
print(country_with_zero_rating_count)
plt.bar(country_with_zero_rating_count['Country'], country_with_zero_rating_count['Country count'], color='red')
plt.xlabel("Countries")
plt.ylabel("Count")
plt.show()

# So we can see that India has given most zero ratings

# Observations
# 1) Maximum No. of people from India have not rated

# Finding out which currency is used in which country

currency_of_countries = final_df.groupby(['Country', 'Currency']).size().reset_index()
print(currency_of_countries.columns)
currency_of_countries = currency_of_countries.drop(0, axis=1)
print(currency_of_countries)  # So we get to know currency of each country

# Which Countries Have Online Delivery Options

online_delivery_countries = final_df.groupby(['Country', 'Has Online delivery']).size().reset_index()
print(online_delivery_countries)
availiblity_online_delivery_option = online_delivery_countries.drop(online_delivery_countries.loc[online_delivery_countries['Has Online delivery'] == 'No'].index)
availiblity_online_delivery_option = availiblity_online_delivery_option.reset_index()
availiblity_online_delivery_option = availiblity_online_delivery_option.drop('index', axis=1)
availiblity_online_delivery_option = availiblity_online_delivery_option.drop(0, axis=1)
print(availiblity_online_delivery_option)
print(final_df[final_df['Has Online delivery'] == 'Yes'].Country.value_counts())

# Observations:
# Online Delivery Options are available in India and UAE

# Create a pie chart same as countries for city

cities_name = final_df.City.value_counts().index
cities_val = final_df.City.value_counts().values
plt.pie(cities_val[:5], labels=cities_name[:5], autopct='%.2f%%')
plt.show()

# Finding top 10 food items

cuisines_count = final_df.groupby(['Cuisines']).size().reset_index().rename(columns={0: 'Cuisines count'})
print(cuisines_count)
cuisines_count = cuisines_count.sort_values(by='Cuisines count', ascending=False).reset_index().drop('index', axis=1)
cuisines_count.head(10)
plt.bar(cuisines_count['Cuisines'][:10], cuisines_count['Cuisines count'][:10], color='blue')
plt.xticks(rotation=45)
plt.show()

india_df = final_df[final_df['Country'] == 'India']
print(india_df)
plt.hist(india_df['Average Cost for two'], bins=10, color='green')
plt.show()

# So we can see that most meals have average cost for two between Rs.0-1000
