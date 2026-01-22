import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
df_data = pd.read_csv("nobel_prize_data.csv")


#Challenge 1
#What is the shape of df_data? How many rows and columns?
print(df_data.shape)
#What are the column names and what kind of data is inside of them?
print(df_data.columns)
#In which year was the Nobel prize first awarded?
print(df_data.sort_values("year", ascending=True).iloc[0]["year"])
#Which year is the latest year included in the dataset?
print(df_data.sort_values("year", ascending=False).iloc[0]["year"])

#Challenge 2
# Are there any duplicate values in the dataset?
print(df_data.duplicated().values.any())
# Are there NaN values in the dataset?
print(df_data.isna().values.any())
#Which columns tend to have NaN values?
print(df_data.isna().sum())
#Filtering on the NaN values in the birth date column we see that we get back a bunch of organisations, like the UN or the Red Cross.
col_subset = ['year','category', 'laureate_type',
              'birth_date','full_name', 'organization_name']
print(df_data.loc[df_data["birth_date"].isna()][col_subset])
print(df_data.loc[df_data["organization_name"].isna()][col_subset])
#Challenge 3
#Convert the birth_date column to Pandas Datetime objects
df_data["birth_date"] = pd.to_datetime(df_data["birth_date"])
#Add a Column called share_pct which has the laureates' share as a percentage in the form of a floating-point number.
separated_values = df_data["prize_share"].str.split("/", expand=True)
numerator = pd.to_numeric(separated_values[0])
denomenator = pd.to_numeric(separated_values[1])
df_data['share_pct'] = numerator / denomenator
print(df_data.info())

#Challenge 2
#Create a donut chart using plotly which shows how many prizes went to men compared to how many prizes went to women.
# What percentage of all the prizes went to women?
biology = df_data["sex"].value_counts()
fig = px.pie(labels= biology.index,
             values=biology.values,
             title="Percentage of Male vs. Female Winners",
             names=biology.index,
             hole=0.4)
fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')

# fig.show()

#Challenge 3
#What are the names of the first 3 female Nobel laureates?
print(df_data[df_data["sex"] == "Female"].sort_values('year', ascending=True)[:3])

#Challenge 4
#Did some people get a Nobel Prize more than once? If so, who were they?
is_winner = df_data.duplicated(subset=["full_name"], keep=False)
multiple_winners = df_data[is_winner]
print(f'There are {multiple_winners.full_name.nunique()}'
      ' winners who were awarded the prize more than once.')
col_subset = ['year', 'category', 'laureate_type', 'full_name']
print(multiple_winners[col_subset])

#Challange 5
#Did some people get a Nobel Prize more than once? If so, who were they?
print(df_data["category"].nunique())
prizes_per_category = df_data.category.value_counts()
v_bar = px.bar(
    x=prizes_per_category.index,
    y=prizes_per_category.values,
    color=prizes_per_category.values,
    color_continuous_scale="Aggrnyl",
    title="Number of Prizes Awarded per Category")

v_bar.update_layout(xaxis_title='Nobel Prize Category',
                    coloraxis_showscale=False,
                    yaxis_title='Number of Prizes')
# v_bar.show()

#Challenge 6
#When was the first prize in the field of Economics awarded?
print(df_data[df_data["category"] == "Economics"].sort_values("year")[:3])

#Challenge 7
#Create a plotly bar chart that shows the split between men and women by category.
cat_men_women = df_data.groupby(['category','sex'], as_index=False).agg({"prize": pd.Series.count})
cat_men_women.sort_values('prize', ascending=False, inplace=True)

v_bar_split = px.bar(x = cat_men_women.category,
                     y = cat_men_women.prize,
                     color = cat_men_women.sex,
                     title="Number of Prizes Awarded per Category split by Men and Women")
v_bar_split.update_layout(xaxis_title='Nobel Prize Category',
                          yaxis_title='Number of Prizes')
# v_bar_split.show()

#Using Matplotlib to Visualise Trends over Time

#Challange 1
#Count the number of prizes awarded every year.
prize_per_year = df_data.groupby(by="year").count().prize
print(prize_per_year)
moving_average = prize_per_year.rolling(window=5).mean()
print(moving_average)

plt.figure(figsize=(8,4), dpi= 200)

plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5),
           fontsize=14,
           rotation=45)

ax = plt.gca()  # get current axis
ax.set_xlim(1900, 2020)

ax.scatter(x=prize_per_year.index,
           y=prize_per_year.values,
           c='dodgerblue',
           alpha=0.7,
           s=100, )

ax.plot(prize_per_year.index,
        moving_average.values,
        c='crimson',
        linewidth=3, )

plt.show()

#Challange 2
yearly_avg_share = df_data.groupby(by='year').agg({'share_pct': pd.Series.mean})
share_moving_average = yearly_avg_share.rolling(window=5).mean()

plt.figure(figsize=(8, 4), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=np.arange(1900, 2021, step=5),
           fontsize=14,
           rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()  # create second y-axis
ax1.set_xlim(1900, 2020)

ax1.scatter(x=prize_per_year.index,
            y=prize_per_year.values,
            c='dodgerblue',
            alpha=0.7,
            s=100, )

ax1.plot(prize_per_year.index,
         moving_average.values,
         c='crimson',
         linewidth=3, )

# Adding prize share plot on second axis
ax2.plot(prize_per_year.index,
         share_moving_average.values,
         c='grey',
         linewidth=3, )

plt.show()