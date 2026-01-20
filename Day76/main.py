import pandas as pd
import plotly.express as px
df_apps = pd.read_csv("apps.csv")
# How many rows and columns does df_apps have?
print(df_apps.shape)
# What are columns names ?
print(df_apps.columns)
#What does the data look like ?
print(df_apps.head())
#Look at a random sample of 5 different rows
print(df_apps.sample(5))
#Remove the columns called Last_Updated and Android_Version from the DataFrame. We will not use these columns.
df_apps.drop(["Last_Updated", "Android_Ver"], axis=1, inplace=True)
print(df_apps.head())
#How many rows have a NaN value (not-a-number) in the Rating column? Create DataFrame called df_apps_clean that does not include these rows.
print(df_apps.isna().values.any())
df_apps_clear = df_apps.dropna()
print(df_apps_clear.isna().values.any())
print(df_apps_clear.shape)
# Are there any duplicates in data? Check for duplicates using the .duplicated() function.
# How many entries can you find for the "Instagram" app? Use .drop_duplicates() to remove any duplicates from df_apps_clean.
duplicated_rows = df_apps_clear[df_apps_clear.duplicated()]
print(duplicated_rows.shape)
print(duplicated_rows.head())
print(df_apps_clear[df_apps_clear["App"] == "Instagram"])
#need to specify the subset for indetifying duplicates
df_apps_clear = df_apps_clear.drop_duplicates(subset=["App", "Type", "Price"])
print(df_apps_clear[df_apps_clear["App"] == "Instagram"])
#Identify which apps are the highest rated. What problem might you encounter if you rely exclusively on ratings alone to determine the quality of an app?
print(df_apps_clear.sort_values("Rating", ascending=False).head())
#What's the size in megabytes (MB) of the largest Android apps in the Google Play Store.
#Based on the data, do you think there could be a limit in place or can developers make apps as large as they please?
print(df_apps_clear.sort_values("Size_MBs", ascending=False).head())
#Which apps have the highest number of reviews? Are there any paid apps among the top 50?
print(df_apps_clear.sort_values("Reviews", ascending=False).head(50))
#Data Visualisation with Plotly: Create Pie and Donut Charts
ratings = df_apps_clear["Content_Rating"].value_counts()
print(ratings)
fig = px.pie(labels=ratings.index,
             values=ratings.values,
             title="Content Rating",
             names=ratings.index)
fig.update_traces(textposition="outside", textinfo="percent+label")
# fig.show()
#To create a donut chart, we can simply add a value for the hole argument
fig = px.pie(labels=ratings.index,
             values=ratings.values,
             title="Content Rating",
             names=ratings.index,
             hole=0.6)
fig.update_traces(textposition="outside", textinfo="percent+label")
# fig.show()
# How many apps had over 1 billion (that's right - BILLION) installations?
# How many apps just had a single install?
print(df_apps_clear["Installs"].describe())
print(df_apps_clear.info())
print(df_apps_clear[["App", "Installs"]].groupby("Installs").count())
df_apps_clear["Installs"] = df_apps_clear["Installs"].astype(str).str.replace(",","")
df_apps_clear["Installs"] = pd.to_numeric(df_apps_clear["Installs"])
print(df_apps_clear[["App", "Installs"]].groupby("Installs").count())
#Convert the price column to numeric data. Then investigate the top 20 most expensive apps in the dataset.
print(df_apps_clear[["App", "Price"]].groupby("Price").count())
df_apps_clear["Price"] = df_apps_clear["Price"].astype(str).str.replace("$","")
df_apps_clear["Price"] = pd.to_numeric(df_apps_clear["Price"])
print(df_apps_clear.sort_values('Price', ascending=False).head(20))
df_apps_clear = df_apps_clear[df_apps_clear["Price"] < 250]
print(df_apps_clear.sort_values("Price", ascending=False).head(5))
#We can work out the highest grossing paid apps now. All we need to do is multiply the values in the price and the installs column to get the number
df_apps_clear["Revenue_Estimate"] = df_apps_clear["Installs"].mul(df_apps_clear["Price"])
print(df_apps_clear.sort_values("Revenue_Estimate",ascending=False)[:10])
# Plotly Bar Charts & Scatter Plots: The Most Competitive & Popular App Categories
print(df_apps_clear["Category"].nunique())
# To calculate the number of apps per category we can use our old friend .value_counts()
top10_category = df_apps_clear["Category"].value_counts()[:10]
print(top10_category)
# To visualise this data in a bar chart we can use the plotly express (our px) bar() function:
bar = px.bar(x = top10_category.index, y = top10_category.values)
# bar.show()
# First, we have to group all our apps by category and sum the number of installations:
category_installs = df_apps_clear.groupby("Category").agg({"Installs": pd.Series.sum})
category_installs.sort_values("Installs", ascending = True, inplace=True)
# Then we can create a horizontal bar chart, simply by adding the orientation parameter:
h_bar = px.bar(x = category_installs.Installs,
               y = category_installs.index,
               orientation="h",
               title="Category Popularity")

h_bar.update_layout(xaxis_title="Number of Downloads", yaxis_title="Category")
# h_bar.show()
#As a challenge, let’s use plotly to create a scatter plot that looks like this:
#First, we need to work out the number of apps in each category (similar to what we did previously).
cat_number = df_apps_clear.groupby("Category").agg({"App": pd.Series.count})
#Then we can use .merge() and combine the two DataFrames.
cat_merged_df = pd.merge(cat_number, category_installs, on="Category", how="inner")
print(f'The dimensions of the DataFrame are: {cat_merged_df.shape}')
print(cat_merged_df.sort_values('Installs', ascending=False))
#Now we can create the chart. Note that we can pass in an entire DataFrame and specify which columns should be used for the x and y by column name.
scatter = px.scatter(cat_merged_df,  # data
                     x='App',  # column name
                     y='Installs',
                     title='Category Concentration',
                     size='App',
                     hover_name=cat_merged_df.index,
                     color='Installs')

scatter.update_layout(xaxis_title="Number of Apps (Lower=More Concentrated)",
                      yaxis_title="Installs",
                      yaxis=dict(type='log'))

# scatter.show()
# Extracting Nested Column Data using .stack()
# How many different types of genres are there?
# Can an app belong to more than one genre? Check what happens when you use .value_counts() on a column with nested values?
# See if you can work around this problem by using the .split() function and the DataFrame's .stack() method.
#Number of Genres
print(len(df_apps_clear["Genres"].unique()))
#Problem: Have multiple categories separated by ;
print(df_apps_clear["Genres"].value_counts().sort_values(ascending=True)[:5])
#This is where the string’s .split() method comes in handy.
# After we’ve separated our genre names based on the semi-colon, we can add them all into a single column with .stack() and then use .value_counts().
stack = df_apps_clear["Genres"].str.split(";", expand=True).stack()
print(f'We now have a single column with shape: {stack.shape}')
num_genres = stack.value_counts()
print(f'Number of genres: {len(num_genres)}')
#Can you create this chart with the Series containing the genre data?
bar = px.bar(x=num_genres.index[:15],  # index = category name
             y=num_genres.values[:15],  # count
             title='Top Genres',
             hover_name=num_genres.index[:15],
             color=num_genres.values[:15],
             color_continuous_scale='Agsunset')

bar.update_layout(xaxis_title='Genre',
                  yaxis_title='Number of Apps',
                  coloraxis_showscale=False)

# bar.show()
#Grouped Bar Charts and Box Plots with Plotly
print(df_apps_clear["Type"].value_counts())
#We see that the majority of apps are free on the Google Play Store. But perhaps some categories have more paid apps than others.
# Let’s investigate. We can group our data first by Category and then by Type.
df_free_vs_paid = df_apps_clear.groupby(["Category", "Type"], as_index=False).agg({"App" : pd.Series.count})
print(df_free_vs_paid.head())
#Use the plotly express bar chart examples and the .bar() API reference to create this bar chart:
g_bar = px.bar(df_free_vs_paid,
               x = "Category",
               y = "App",
               title="Free vs Paid Apps by Category",
               color = "Type",
               barmode = "group")

g_bar.update_layout(xaxis_title='Category',
                    yaxis_title='Number of Apps',
                    xaxis={'categoryorder':'total descending'},
                    yaxis=dict(type='log'))

g_bar.show()
#Create a box plot that shows the number of Installs for free versus paid apps.
# How does the median number of installations compare? Is the difference large or small?
box = px.box(df_apps_clear,
             x="Installs",
             y="Type",
             color="Type",
             notched=True,
             points="all",
             title='How Many Downloads are Paid Apps Giving Up?')
box.update_layout(yaxis=dict(type='log'))
box.show()

#What is the median price for a paid app? Then compare pricing by category by creating another box plot. But this time examine the prices (instead of the revenue estimates) of the paid apps.
# I recommend using {categoryorder':'max descending'} to sort the categories.
df_paid_apps = df_apps_clear[df_apps_clear['Type'] == 'Paid']
df_paid_apps.Price.median()
box = px.box(df_paid_apps,
             x='Category',
             y="Price",
             title='Price per Category')

box.update_layout(xaxis_title='Category',
                  yaxis_title='Paid App Price',
                  xaxis={'categoryorder': 'max descending'},
                  yaxis=dict(type='log'))

box.show()