#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US Bikeshare data!')

    # get user input for city (chicago, new york city, washington).

    city = input('Would you like to see data from Chicago, New York or Washington? ').lower()
    while city not in CITY_DATA.keys():
        print("Sorry, it seems like you didn\'t choose one of the 3 Available Cities")
        city = input('Would you like to see data from Chicago, New York or Washington? ').lower()

    # get user input for filter type (month, day or not at all).

    filter_data = input('Would you like to filter the data by month, day,or not at all? ').lower()
    while filter_data not in ['month', 'day', 'not at all']:
        print('Sorry, You provided an invalid filter')
        filter_data = input('Would you like to filter the data by month, day,or not at all? ').lower()

    # get user input for month (all, january, february, ... , june)

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    if filter_data == 'month':
        month = input('Please Choose a specific month: January, February, March, April, May, June ? ').title()
        while month not in months:
            print('Sorry, You provided an invalid month')
            month = input('Please Choose a specific month: January, February, March, April, May, June ? ').title()
    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)

    days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    if filter_data == 'day':
        day = input('Please Choose a specific day: Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday ').title()
        while day not in days:
            print('Sorry, You provided an invalid day')
            day = input('Please Choose a specific day: Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday ').title()
    else:
        day = 'all'

    print('-' * 40)
    return city, month, day

#####################################################################################

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Reading the Csv file using Pandas

    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime using the pandas function

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month& week days from Start Time then create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if Chosen
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by a week day if Chosen
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


#####################################################################################


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    common_month = df['month'].mode()[0]
    print("The most common month is: {} ".format(months[common_month - 1]))

    # display the most common week day

    common_day = df['day_of_week'].mode()[0]
    print('The most common day of week is: {}'.format(common_day))

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    #####################################################################################


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is: {}'.format(common_start_station))

    # display most commonly used end station

    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is: {}'.format(common_end_station))

    # display most frequent combination of start station and end station trip

    common_trip = df['Start Station'] + ' to ' + df['End Station']
    print('The most frequent trip is from {}'.format(common_trip.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


#####################################################################################

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    days = total_travel_time.days
    hours = total_travel_time.seconds // (60 * 60)
    minutes = total_travel_time.seconds % (60 * 60) // 60
    seconds = total_travel_time.seconds % (60 * 60) % 60
    print('Total travel time is: {} days {} hours {} minutes {} seconds'.format(days, hours, minutes, seconds))

    # display mean travel time

    average_travel_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    average_days = average_travel_time.days
    average_hours = average_travel_time.seconds // (60 * 60)
    average_minutes = average_travel_time.seconds % (60 * 60) // 60
    average_seconds = average_travel_time.seconds % (60 * 60) % 60
    print('Average travel time is: {} days {} hours {} minutes {} seconds'.format(average_days, average_hours, average_minutes, average_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


#####################################################################################

def user_stats(df):
    """Displays statistics on Bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(user_type, '\n')

    # Display counts of gender

    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(user_gender, '\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        year = df['Birth Year']
        earliest_year = int(year.min())
        most_recent_year = int(year.max())
        most_common_year = int(year.mode()[0])
        print('Earliest birth year is: {}\n most recent is: {}\n and most common birth year is:{}'.format(earliest_year, most_recent_year, most_common_year))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


#####################################################################################

def display_raw_data(df):
    """Asks the user if he wants to display 5 raw data rows at once """
    raw_data = input('\nWould you like to display raw data?\n').lower()
    while raw_data not in ['yes','no']:
        print('Please Make sure to type Yes or No')
        raw_data = input('\nWould you like to display raw data?\n').lower()

    if raw_data == 'yes':
        counter = 0
        while True:
            pd.set_option('display.max_columns',200)
            print(df.iloc[counter: counter + 5])
            counter += 5
            next_five_rows = input('Do you want to see the next 5 rows?').lower()
            if next_five_rows != 'yes':
                break



#####################################################################################

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()


# In[ ]:




