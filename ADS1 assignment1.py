#Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#defining a line plot function 
def lineplot(df, region_to_plot):
    """ Function to create a lineplot. 
    Arguments:
    A dataframe with a column "x" and column "y".
    A list containing values of a column to iterate over to plot.

    """
    plt.figure()

    for region in region_to_plot:
        plt.plot(df["x"], df["y"], label=region)


    plt.xlabel("x")
    plt.ylabel("y")
    #removing white space left and right.
    plt.xlim(min(df["x"]), df["x"].max())
    plt.legend()
    plt.show()
    return plt.figure()


#defining a stacked bar chart function
def stacked_bar_chart(data, x_col, y_col, stacked_cols, title='', xlabel='',
                      ylabel='', legend_labels=None, figsize=(5,5)):
    """
    Generate a stacked bar chart.

    Parameters:
    - data: DataFrame containing the data.
    - x_col: Column name for the x-axis.
    - y_col: Column name for the y-axis.
    - stacked_cols: List of column names to stack.
    - title: Title of the plot (optional).
    - xlabel: Label for the x-axis (optional).
    - ylabel: Label for the y-axis (optional).
    - legend_labels: List of legend labels for stacked columns (optional).
    

    Returns:
    - None (displays the plot).
    """
    plt.figure()

    # Plot stacked bars
    data.set_index(x_col)[stacked_cols].plot(kind='bar', stacked=True)

    # Customize the plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if legend_labels:
        plt.legend(labels=legend_labels)

    plt.show()
    return


#defining a pie chart function
def pie_chart(data, values_col, labels_col, title='', figsize=(5,5)):
    """
    Generate a pie chart.

    Parameters:
    data: DataFrame containing the data.
    values_col: Column name for the values.
    labels_col: Column name for the labels.
    title: Title of the plot (optional).
    figsize: Tuple specifying the figure size (optional).

    Returns:
    None (displays the plot).
    """
    plt.figure()

    # Plot pie chart
    plt.pie(data[values_col], labels=data[labels_col], 
            autopct='%1.1f%%', startangle=100)

    # Customize the plot
    plt.title(title)

    plt.show()

    return 


#read dataset into dataframe
covid_deaths = pd.read_csv(r"C:\Users\IFECHUKWU\Downloads\
                           nhse_total_deaths_by_region.csv")
print(covid_deaths.head())

#let's explore the datset for any missing values
print(covid_deaths.isna().sum())
print(covid_deaths.info())

#let's change the data type of the date column to datetime
covid_deaths['date'] = pd.to_datetime(covid_deaths['date'])
print(covid_deaths['date'].info())

#extracting the year and month from the date column
covid_deaths['year'] = (covid_deaths['date']).dt.year
covid_deaths['month'] = (covid_deaths['date']).dt.month
print(covid_deaths)

#subsetting dataframe to columns to work with
covid_deaths = covid_deaths[["nhs_england_region",
        "year", "month","new_deaths_with_positive_test", 
        "new_deaths_without_positive_test", "new_deaths_total"]].set_index(
        ['nhs_england_region', 'year', 'month'])
print(covid_deaths.info())

#extracting summary statistics to plot
covid_deaths_by_region = covid_deaths.groupby(["nhs_england_region", 
                    "year", "month"])["new_deaths_with_positive_test"].sum(
                        ).reset_index()
#rename statistic values column                       
covid_deaths_by_region = covid_deaths_by_region.rename(columns=
              {'new_deaths_with_positive_test':'deaths_sum'})
print(covid_deaths_by_region)

#define the list to iterate over the for loop
regions_to_plot = ['East Of England','London', 'Midlands',
                  'North East And Yorkshire','North East','North West',
                  'South East', 'South West']


plt.figure(figsize=(7,4))

for region in regions_to_plot:
     region_data = covid_deaths_by_region[covid_deaths_by_region[
         'nhs_england_region'] == region]
     plt.plot(region_data['year'].astype(str) + '-' + region_data[
         'month'].astype(str), region_data['deaths_sum'], label=region)

# Customize the plot
plt.xlabel('Year-Month')
plt.ylabel('Number of New Deaths with Positive Test')
plt.title('New Deaths with Positive Test Over Time by Region')
plt.legend()

# Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=45)

plt.show()


#regrouping the data 
covid_death_totals_by_region = covid_deaths.groupby('nhs_england_region')
['new_deaths_with_positive_test', 'new_deaths_without_positive_test'].sum(
   ).reset_index()
print(covid_death_totals_by_region)

#calling the stacked_bar_chart function
stacked_bar_chart(covid_death_totals_by_region, covid_death_totals_by_region[
    'nhs_england_region'].unique(), 'new_deaths_total_', 
    ['new_deaths_with_positive_test', 'new_deaths_without_positive_test'], 
    title='Death Totals', xlabel='region', ylabel='deaths')

#calling the pie chart function
pie_chart(covid_death_totals_by_region, 'new_deaths_with_positive_test', 
          'nhs_england_region', title= 'covid Deaths by Region')

