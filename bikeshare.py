# import numpy and pandas libraries
import time
import pandas as pd
import numpy as np
import json
import click

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

citys = ['chicago', 'new york city', 'washington']
months = ['all', 'january', 'february', 'march',
          'april', 'may', 'june']

days = ['all', 'sunday', 'monday', 'tuesday',
        'wednesday', 'thursday', 'friday', 'saturday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = input("From which city today you wanted to see the data ?,list of "
                 "available cities are  NEW YORK,CHICAGO,WASHINGTON: \n").lower()
    # city.lower()
    while (True):
        if (city == 'new york city' or city == 'chicago' or
                city == 'washington' or city == 'all'):
            break
        else:
            city = input(
                "Please Enter valid city. For details see above: \n").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input(
        "\nEnter which month? January, February, March, April, May, or June?, \n").lower()
    # month.lower()
    while (True):
        if (month == 'january' or month == 'february' or month == 'march' or
                month == 'april' or month == 'may' or month == 'june' or month == 'all'):
            break
        else:
            month = input(
                'Please enter  the valid month. For details please see above\n').lower()
            # month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day  monday, tuesday, wednesday, thursday, friday, '
                'saturday , sunday or all to display data of all days?\n').lower()
    # day.lower()
    while (True):
        if (day == 'monday' or day == 'tuesday' or day == 'wednesday' or
                day == 'thursday' or day == 'friday' or day == 'saturday' or
                day == 'sunday' or day == 'all'):
            break
        else:
            day = input('Please enter  the Correct day: ').lower()
            # day.lower()

    print('-' * 80)
    return city, month, day


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
    print("\nThe program is loading the data for filter of your choice.")
    # start_time = time.time()
    # filter data based on selected city and load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # obtain month from Start Time
    df['month'] = df['Start Time'].dt.month
    # Obtain day of week from Start Time
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the month
    if month != 'all':
        months_selected = ['january', 'february',
                           'march', 'april', 'may', 'june']
        month = months_selected.index(month) + 1

        # filter data by month to create new dataframe
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nDisplaying the statistics on the most frequent '
          'times of  travel...\n')
    start_time = time.time()

    # look_up dictionary
    look_up = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May',
               '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November',
               '12': 'December'}

    # display the most common month
    popular_month = df['month'].mode()[0]
    month_in_string = look_up[str(popular_month)]
    print("The most common month is: ", month_in_string)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day of the week is: {}".format(popular_day))

    # display the most common start hour
    popular_hour = df['Start Hour'].mode()[0]
    print('The most common start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print()
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print(' Station Stats '.center(40, '-'))

    # TO DO: display most commonly used start station
    if 'Start Station' in df.columns:
        print('commonly used Start station '
              'station '.ljust(40, '.'), df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    if 'End Station' in df.columns:
        print('commonly used End Station '
              'station '.ljust(40, '.'), df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['travel'] = df['Start Station'] + ' -> ' + df['End Station']
        print('Most frequent travel route '.ljust(
            40, '.'), df['travel'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    temp = total_travel_time
    day = temp // (24 * 3600)
    temp = temp % (24 * 3600)
    hour = temp // 3600
    temp %= 3600
    minutes = temp // 60
    temp %= 60
    seconds = temp
    print('\nThe total travel time is {} days {} hours {} minutes {} seconds'.format(
        day, hour, minutes, seconds))

    # TO DO: display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    temp2 = mean_travel_time
    temp2 = temp2 % (24 * 3600)
    mean_hour = temp2 // 3600
    temp2 %= 3600
    mean_minute = temp2 // 60
    temp2 %= 60
    mean_seconds = temp2
    print('\nThe mean travel time is {} hours {} minutes {} seconds'.format(
        mean_hour, mean_minute, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("Distribution for user types:")
    print(user_types)

    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:")
        print(gender)
    except KeyError:
        print("There is no data for user genders {}."
              .format(city.title()))

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = str(int(df['Birth Year'].min()))
        print("\nFor the selected filter, the oldest person to ride one "
              "bike was born in: " + earliest)
        most_recent = str(int(df['Birth Year'].max()))
        print("For the selected filter, the youngest person to ride one "
              "bike was born in: " + most_recent)
        most_common = str(int(df['Birth Year'].mode()[0]))
        print("For the selected filter, the most common birth year amongst "
              "riders is: " + most_common)
    except:
        print("We're sorry! There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def raw_data(df):
    """5 rows of data will added in each key press and
    pressing no will end displaying the data"""
    print('Please enter y for yes to see 5 rows data at a time, press n for no to skip')
    # display row of data after key press for yes
    i = 0
    while (input().lower() != 'n'):
        i = i+5
        print(df.head(i))


def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw_data(df)

        restart = input(
            '\nWould you like to start the program again? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()

# https://towardsdatascience.com/top-python-libraries-numpy-pandas-8299b567d955
