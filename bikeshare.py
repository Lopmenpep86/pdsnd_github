import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york city', 'washington']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()
        if city.lower() in CITIES:
            break
    # get user input for month (all, january, february, ... , june)

    while True:
        month = input('Which month would you like to see data from? I.e.: January - June or "all" if you do not want to apply month filter.\n').lower()
        if month.lower() in MONTHS:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input('Which day would you like to see data from? I.e.: Monday - Sunday or "all" if you do not want to apply day filter.\n').lower()
        if day.lower() in DAYS:
            break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month =  months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    top_month=df['month'].mode()[0]
    print('The most common month is: {}'.format(top_month))

    # display the most common day of week

    top_day=df['day_of_week'].mode()[0]
    print('The most common day is: {}'.format(top_day))

    # display the most common start hour

    top_start_hour=df['hour'].mode()[0]
    print('The most common start hour is: {}'.format(top_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    top_start_station=df['Start Station'].mode()[0]
    print('The most commonly used start station is: {}'.format(top_start_station))

    # display most commonly used end station

    top_end_station=df['End Station'].mode()[0]
    print('The most commonly used end station is: {}'.format(top_end_station))

    # display most frequent combination of start station and end station trip

    top_start_end_stations = df[['Start Station', 'End Station']].mode().loc[0]
    print('The most commonly used start and end stations are : {}, {}'.format(top_start_end_stations[0], top_start_end_stations[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time=df['Trip Duration'].sum()
    print("The total travel time is: {}".format(total_travel_time))

    # TO DO: display mean travel time

    avg_travel_time=df['Trip Duration'].mean()
    print("The average travel time is: {}".format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:

        birth_year = df['Birth Year']

        earliest_year = birth_year.min()
        print('The earliest birth year is: {}'.format(earliest_year))

        most_recent_year = birth_year.max()
        print('The most recent birth year is: {}'.format(most_recent_year))

        most_common_year = birth_year.value_counts().idxmax()
        print('The most common birth year is: {}'.format(most_common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #To give the option to retrieve raw data, I got some guidance from Udacity Knowledge Centre (https://knowledge.udacity.com/questions/26261)

        raw_data = input('\nWould you like to see 5 rows of data? Please enter yes or no:\n').lower()
        if raw_data in ('yes', 'y'):
            i = 0
            while True:
                print(df.iloc[i:i+5])
                i += 5
                more_data = input('Would you like to see even more data? Please enter yes or no:\n').lower()
                if more_data not in ('yes', 'y'):
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
