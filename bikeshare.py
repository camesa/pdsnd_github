import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
cities = ['chicago','new york', 'washington']
city = 0
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')


    #gets user input for city to analyze (chicago, new york city, washington).
    city_message = 'Which city would you like to see data from? Chicago, New York, or Washington?: \n'
    global city
    city = input(city_message).lower()
    while city not in cities:
        print('Seems you may have misspelled the name the city.\n')
        city = input(city_message)

    #gets user input for month (all, january, february, ... , june)
    month_message = '\nWhich month would you like to see data from? January, February, March, April, May or June? \nYou can type "all" for no filter: \n'
    month = input(month_message).lower()
    while month not in MONTHS:
        print('Seems you may have misspelled the month.\n')
        month = input(month_message).lower()

    #gets user input for day of week (all, monday, tuesday, ... sunday)
    day_message = '\nWhich day of the week would you like to analyze? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\nYou can type "all" for no filter : \n'
    day = input(day_message).title()
    while day not in days:
        print('Seems you may have misspelled the day.\n')
        day = input(day_message).title()

    print('\nThank you! Your filter selection has been City: {} - Month: {} - Day: {}:\n'.format(city, month, day))
    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])

    # converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extracts day of week from the Start Time column to create an 'Day of Week' column
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # extracts month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month
    # extracts hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #if filter by month  applicable, it will use the index of the months list to get the corresponding int
    if month != 'all':
        month = MONTHS.index(month)
        # filter by month to create the new dataframe
        df = df[df['month'] == month + 1]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Displays the most common month
    popular_month = df['month'].mode()[0]
    # use the index of the months list to get the corresponding int
    popular_month = MONTHS[popular_month - 1]
    print('Most popular month for travel is {}\n'.format(popular_month))

    #Displays the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print('Most popular day of the week for travel is {}\n'.format(popular_dow))

    # Displays the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular time of the day for travel is at {}hs\n'.format(popular_hour))


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    popular_station = df['Start Station'].mode()[0]
    print('Most popular start station is {}\n'.format(popular_station))

    # Displays most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station is {}\n'.format(popular_end_station))


    # Displays most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most popular combination is from {} to {}'.format(popular_combination[0],popular_combination[1]))

    if popular_combination[0] == popular_combination[1]:
        print('This means the most popular travel is a round trip!')


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time, converted from seconds to weeks and days
    total_trip =  df['Trip Duration'].sum()
    days = total_trip // (24 * 3600)
    weeks = days // 7
    remainder = days % 7
    print('The total travel time based on your filter selection is {} weeks and {} day(s)'.format(weeks, remainder))

    # Displays mean travel time in minutes
    trip_duration =  df['Trip Duration'].mean()
    print('The average travel time is {} minutes'.format(round(trip_duration / 60, 2)))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

        # Displays counts of user types in tabulate. Separated keys and values and converts count values to percentage
    user_types = df['User Type'].value_counts().keys().tolist()
    ut_count = df['User Type'].value_counts().tolist()
    ut_percent = df['User Type'].value_counts(normalize=True)
    ut_data = [[user_types[0], ut_count[0], '{}%'.format(round(ut_percent[0]*100), 2)],
        [user_types[1], ut_count[1], '{}%'.format(round(ut_percent[1]*100), 2)]]

    print(tabulate(ut_data, headers=['User Type', 'Count', 'Percentage']))
    print('')

    # Verifies selected city is not Washington before continue to gender and birth year analysis.
    if city != 'washington':
        # Displays counts of gender in tabulate. Separated keys and values and converts count values to percentage
        gender = df['Gender'].value_counts().keys().tolist()
        gender_count = df['Gender'].value_counts().tolist()
        gender_percent = df['Gender'].value_counts(normalize=True)

        print('')
        gender_data = [[gender[0], gender_count[0], '{}%'.format(round(gender_percent[0]*100), 2)],
            [gender[1], gender_count[1], '{}%'.format(round(gender_percent[1]*100), 2)]]

        print(tabulate(gender_data, headers=['Gender', 'Count', 'Percentage']))
        print('\nThis took %s seconds.' % (time.time() - start_time))
        print('-'*40)

    # Display earliest, most recent, and most common year of birth
        earliest_byear = df['Birth Year'].min()
        recent_byear = df['Birth Year'].max()
        common_byear = df['Birth Year'].mode()[0]

        print('')
        by_data = [['Earliest year', earliest_byear],
            ['Most recent', recent_byear],
            ['Most common', common_byear]]

        print(tabulate(by_data, headers=['Data', 'Birth Year']))
        print('\nThis took %s seconds.' % (time.time() - start_time))
        print('-'*40)

    else:
        print('\nSorry! We don´t have any gender or birth year data for the city of Washington.')

def raw_data(df):
    """
    Asks user to if he/she wants to see raw data for the selected city.
    It will display 5 rows of data at a time until user decides types 'no'

    """
    view_rdata = input('\nWould you like to see raw data of individual trips? Enter yes or no\n').lower()
    rdata_index = 0
    while view_rdata.lower() == 'yes':
        print(df.iloc[rdata_index:rdata_index+5])
        rdata_index += 5
        rdata_cont = input('Would you like to see 5 more rows?:Enter yes or no.\n' ).lower()
        if rdata_cont.lower() != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
