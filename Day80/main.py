import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
import numpy as np
import seaborn as sns
import scipy.stats as stats

df_yearly = pd.read_csv("annual_deaths_by_clinic.csv")
df_monthly = pd.read_csv("monthly_deaths.csv")

#Challenge 1: Preliminary Data Exploration
#What is the shape of df_yearly and df_monthly? How many rows and columns?
print(df_yearly.shape)
print(df_monthly.shape)
#What are the column names?
print(df_yearly.info())
print(df_monthly.info())
#Which years are included in the dataset?
print(df_yearly.sort_values("year", ascending=False))
#Are there any NaN values or duplicates?
print(df_monthly.isna().values.any())
print(df_yearly.isna().values.any())
print(df_monthly.duplicated().values.any())
print(df_yearly.duplicated().values.any())
#What were the average number of births that took place per month?
print(df_monthly.describe())
#What were the average number of deaths that took place per month?
print(df_yearly.describe())
#Challenge 2: Percentage of Women Dying in Childbirth
#How dangerous was childbirth in the 1840s in Vienna?
prob = df_yearly.deaths.sum() / df_yearly.births.sum() * 100
print(f'Chances of dying in the 1840s in Vienna: {prob}%')
#Challenge 3: Visualise the Total Number of Births 🤱 and Deaths 💀 over Time

years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

plt.figure(figsize=(8, 4), dpi=200)
plt.title('Total Number of Monthly Births and Deaths', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('Births', color='skyblue', fontsize=18)
ax2.set_ylabel('Deaths', color='crimson', fontsize=18)

# Use Locators
ax1.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.grid(color='grey', linestyle='--')

ax1.plot(df_monthly.date,
         df_monthly.births,
         color='skyblue',
         linewidth=3)

ax2.plot(df_monthly.date,
         df_monthly.deaths,
         color='crimson',
         linewidth=2,
         linestyle='--')

# plt.show()

#Analysing the Yearly Data Split By Clinic
#Challenge 1: The Yearly Data Split by Clinic
#Analysing the Yearly Data Split By Clinic
#Which clinic is bigger or more busy judging by the number of births?
bigger_clinic = df_yearly.groupby("clinic").agg({"births" : pd.Series.sum})
print(bigger_clinic)

line = px.line(df_yearly,
        x="year",
        y="births",
        color="clinic",
        title='Total Yearly Births by Clinic')
# line.show()

line = px.line(df_yearly,
        x="year",
        y="deaths",
        color="clinic",
        title='Total Yearly Births by Clinic')
# line.show()

#Challenge 2: Calculate the Proportion of Deaths at Each Clinic
#Calculate the proportion of maternal deaths per clinic. That way we can compare like with like.
#Work out the percentage of deaths for each row in the df_yearly DataFrame by adding a column called "pct_deaths".
df_yearly["pct_deaths"] = df_yearly["deaths"] / df_yearly["births"]
#Calculate the average maternal death rate for clinic 1 and clinic 2 (i.e., the total number of deaths per the total number of births).
clinic_1 = df_yearly[df_yearly["clinic"] == "clinic 1"]
avg_c1 = clinic_1["deaths"].sum() / clinic_1["births"].sum() * 100
print(f'Average death rate in clinic 1 is {avg_c1:.3}%.')
clinic_2 = df_yearly[df_yearly.clinic == 'clinic 2']
avg_c2 = clinic_2.deaths.sum() / clinic_2.births.sum() * 100
print(f'Average death rate in clinic 2 is {avg_c2:.3}%.')

#Create another plotly line chart to see how the percentage varies year over year with the two different clinics.
line = px.line(df_yearly,
               x='year',
               y='pct_deaths',
               color='clinic',
               title='Proportion of Yearly Deaths by Clinic')

# line.show()
#The Effect of Handwashing
#Challenge 1: The Effect of Handwashing
#Add a column called "pct_deaths" to df_monthly that has the percentage of deaths per birth for each row.
df_monthly["pct_deaths"] = df_monthly["deaths"] / df_monthly["births"]
#Create two subsets from the df_monthly data: before and after Dr Semmelweis ordered washing hand.
handwashing_start = '1846-06-01'
before_washing = df_monthly[df_monthly["date"] < handwashing_start]
after_washing = df_monthly[df_monthly.date >= handwashing_start]
bw_rate = before_washing.deaths.sum() / before_washing.births.sum() * 100
aw_rate = after_washing.deaths.sum() / after_washing.births.sum() * 100
print(f'Average death rate before 1847 was {bw_rate:.4}%')
print(f'Average death rate AFTER 1847 was {aw_rate:.3}%')
#Challenge 2: Calculate a Rolling Average of the Death Rate
#Create a DataFrame that has the 6-month rolling average death rate prior to mandatory handwashing.
#Hint: You'll need to set the dates as the index in order to avoid the date column being dropped during the calculation
roll_df = before_washing.set_index('date')
roll_df = roll_df.rolling(window=6).mean()
print(roll_df)

#Challenge 3: Highlighting Subsections of a Line Chart

plt.figure(figsize=(8, 4), dpi=200)
plt.title('Percentage of Monthly Deaths over Time', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

plt.ylabel('Percentage of Deaths', color='crimson', fontsize=18)

ax = plt.gca()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)
ax.set_xlim([df_monthly.date.min(), df_monthly.date.max()])

plt.grid(color='grey', linestyle='--')

ma_line, = plt.plot(roll_df.index,
                    roll_df.pct_deaths,
                    color='crimson',
                    linewidth=3,
                    linestyle='--',
                    label='6m Moving Average')
bw_line, = plt.plot(before_washing.date,
                    before_washing.pct_deaths,
                    color='black',
                    linewidth=1,
                    linestyle='--',
                    label='Before Handwashing')
aw_line, = plt.plot(after_washing.date,
                    after_washing.pct_deaths,
                    color='skyblue',
                    linewidth=3,
                    marker='o',
                    label='After Handwashing')

plt.legend(handles=[ma_line, bw_line, aw_line],
           fontsize=18)

# plt.show()
#Visualising Distributions and Testing for Statistical Significance
#Challenge 1: Calculate the Difference in the Average Monthly Death Rate
#What was the average percentage of monthly deaths before handwashing (i.e., before June 1847)?
avg_prob_before = before_washing["pct_deaths"].mean() * 100
print(f'Chance of death during childbirth before handwashing: {avg_prob_before:.3}%.')
avg_prob_after = after_washing.pct_deaths.mean() * 100
print(f'Chance of death during childbirth AFTER handwashing: {avg_prob_after:.3}%.')
mean_diff = avg_prob_before - avg_prob_after
print(f'Handwashing reduced the monthly proportion of deaths by {mean_diff:.3}%!')
times = avg_prob_before / avg_prob_after
print(f'This is a {times:.2}x improvement!')

#Challenge 2: Using Box Plots to Show How the Death Rate Changed Before and After Handwashing
df_monthly["washing_hands"] = np.where(df_monthly.date < handwashing_start, "No", "Yes")
print(df_monthly.head())

box = px.box(df_monthly,
             x="washing_hands",
             y="pct_deaths",
             color="washing_hands",
             title='How Have the Stats Changed with Handwashing?')

box.update_layout(xaxis_title='Washing Hands?',
                  yaxis_title='Percentage of Monthly Deaths', )

box.show()

#Challenge 3: Use Histograms to Visualise the Monthly Distribution of Outcomes

hist = px.histogram(df_monthly,
                    x='pct_deaths',
                    color='washing_hands',
                    nbins=30,
                    opacity=0.6,
                    barmode='overlay',
                    histnorm='percent',
                    marginal='box', )

hist.update_layout(xaxis_title='Proportion of Monthly Deaths',
                   yaxis_title='Count', )

hist.show()

#Challenge 4: Use a Kernel Density Estimate (KDE) to visualise a smooth distribution

plt.figure(dpi=200)
sns.kdeplot(before_washing.pct_deaths,
            fill=True,
            clip=(0,1))
sns.kdeplot(after_washing.pct_deaths,
            fill=True,
            clip=(0,1))
plt.title('Est. Distribution of Monthly Death Rate Before and After Handwashing')
plt.xlim(0, 0.40)
plt.show()

#Challenge 5: Use a T-Test to Show Statistical Significance
t_stat, p_value = stats.ttest_ind(a=before_washing.pct_deaths,
                                  b=after_washing.pct_deaths)
print(f'p-value is {p_value:.10f}')
print(f't-statstic is {t_stat:.4}')
