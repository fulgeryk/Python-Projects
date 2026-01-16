import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("QueryResults.csv", names=["Date", "TAG", "POSTS"], header=0)
print(data.head()) # Display the first few rows of the dataframe
print(data.tail()) # Display the last few rows of the dataframe
print(data.shape) # Display the shape of the dataframe (rows, columns)]
print(data.count()) # Display the count of non-null values in each column
number_posts_per_language = data.groupby("TAG")["POSTS"].sum() # Group by programming language and sum the number of posts
print(number_posts_per_language) # Display the total number of posts per programming language
print(number_posts_per_language.idxmax()) # Display the programming language with the highest number of posts
months_post_per_language = data.groupby("TAG").count() # Group by programming language and count the number of months with posts
print(months_post_per_language) # Display the number of months with posts per programming language
print(data["Date"][1]) # Display the date of the second row 
#Alternative way to get the date of the second row
print(type(data.Date[1])) # Display the date of the second row
print(type(pd.to_datetime(data["Date"][1]))) # Convert the date string to a datetime object
data.Date = pd.to_datetime(data["Date"]) # Convert the entire "Date" column to datetime objects
print(data.head()) # Display the first few rows of the dataframe with updated "Date" column
reshaped_df = data.pivot(index="Date", columns="TAG", values="POSTS") # Reshape the dataframe using pivot
print(reshaped_df.shape) # Display the shape of the reshaped dataframe
print(reshaped_df.columns) # Display the columns of the reshaped dataframe
print(reshaped_df.head()) # Display the first few rows of the reshaped dataframe
print(reshaped_df.count()) # Display the count of non-null values in each column of the reshaped dataframe
reshaped_df = reshaped_df.fillna(0) # Fill NaN values with 0 in the reshaped dataframe
print(reshaped_df.head()) # Display the first few rows of the reshaped dataframe after filling NaN values
print(reshaped_df.isna().values.any()) # Check if there are any NaN values left in the reshaped dataframe
# The window is number of observations that we averaged
roll_df = reshaped_df.rolling(window=12).mean() # Calculate the rolling mean with a window of 12 months
plt.figure(figsize=(12,10)) # Set the figure size for the plot
plt.xticks(fontsize=14) # Set the font size for x-axis ticks
plt.yticks(fontsize=14) # Set the font size for y-axis ticks
plt.xlabel("Date", fontsize=16) # Set the x-axis label
plt.ylabel("Number of Posts", fontsize=16) # Set the y-axis label
plt.ylim(0, 35000) # Set the y-axis limits
# plt.plot(reshaped_df.index, reshaped_df.java, label="Java") # Plot the number of posts for Java over time
# plt.plot(reshaped_df.index, reshaped_df.python, label="Python") # Plot the number of posts for Python over time
# plot all languages using a loop
for column in roll_df.columns:
    plt.plot(roll_df.index, roll_df[column], linewidth=3, label = roll_df[column].name) # Plot the number of posts for each programming language over time
plt.legend(fontsize=14) # Add a legend to the plot
plt.show() # Display the plot