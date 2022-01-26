#TO DO: Import Python libraries
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('\nPlease enter one of the available cities --> Chicago, New York City or Washington: \n'))
            city = city.lower()
            if city in ['chicago','new york city','washington']:
                break
            else:
                print('Sorry, but this city (\'{}\') is not available or there was a typing mistake. Please try again.'.format(city))
        except KeyboardInterrupt:
            print('\nNo input taken')


    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('\nIt is possible to filter the data by month --> January up to June.\nPlease enter the month or type \'all\' to not filter the data: \n'))
            month = month.lower()
            if month in ['january','february','march','april','may','june','all']:
                break
            else:
                print('Sorry, but this month option (\'{}\') is not available or there was a typing mistake. Please try again.'.format(month))
        except KeyboardInterrupt:
            print('\nNo input taken')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('\nIt is possible to filter the data by the day of the week --> Sunday up to Saturday.\nPlease enter the day or type \'all\' to not filter the data: \n'))
            day = day.lower()
            if day in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']:
                break
            else:
                print('Sorry, but this day option (\'{}\') is not available or there was a typing mistake. Please try again.'.format(day))
        except KeyboardInterrupt:
            print('\nNo input taken')


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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        pop_month=df['month'].mode()[0]
        print('\nMost popular Month for {} is:'.format(city.title()), pop_month)
    else:
        print('\nMonth selected:', month.title())

    # TO DO: display the most common day of week
    if day == 'all':
        pop_day_of_week=df['day_of_week'].mode()[0]
        print('\nMost popular Day of the Week for {} is:'.format(city.title()), pop_day_of_week)
    else:
        print('\nDay of the Week selected:', day.title())

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour']=df['Start Time'].dt.hour

    # find the most popular hour
    pop_hour=df['hour'].mode()[0]
    print('\nMost popular Start Hour:', pop_hour)

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start_station = df['Start Station'].value_counts().idxmax()
    print('\nMost popular Start Station:', pop_start_station)

    # TO DO: display most commonly used end station
    pop_end_station = df['End Station'].value_counts().idxmax()
    print('\nMost popular End Station:', pop_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip path'] = df['Start Station'] + ' / ' + df['End Station']
    pop_trip = df['Trip path'].value_counts().idxmax()
    print('\nMost popular combination of Start / End Station:', pop_trip)

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    total_hours = int(total_time/3600)
    total_min = int((total_time%3600)/60)
    total_sec = (total_time%3600)%60
    print('\nTotal travel time (all bike rentals with filters applied):', total_hours, 'hours +', total_min, 'minutes +', total_sec, 'seconds' )


    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_hours = int(mean_time/3600)
    mean_min = int((mean_time%3600)/60)
    mean_sec = int((mean_time%3600)%60)
    print('\nMean travel time (all bike rentals with filters applied):', mean_hours, 'hours +', mean_min, 'minutes +', mean_sec, 'seconds' )


    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):

    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types=df['User Type'].value_counts()
    print('User Types:')
    print(user_types)

    # TO DO: Display counts of gender (Only valid for Chicago and New York City)
    if city in ['chicago', 'new york city']:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Gender:')
        print(gender_counts)

        # TO DO: Display earliest, most recent, and most common year of birth
        early_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])

        print('\nEarliest Year of Birth:', early_year)
        print('Most recent Year of Birth:', recent_year)
        print('Most common Year of Birth:', common_year)

    else:
        print('\n*Bikeshare Users Statistics not available for {}.'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):

    """Displays 5 rows of raw data (with the filters applied) at a time if the user enters yes"""

    i = 0
    #While loop to verify if users input is yes or no. It breaks if no is entered.
    while True:
          try:
              answer_raw_data = str(input('\nWould you like to view 5 rows of raw data? Please enter yes or no: \n'))
              answer_raw_data = answer_raw_data.lower()
              if answer_raw_data in ['yes','no']:
                  if answer_raw_data == 'yes' and i < len(df):
                      i+=5
                      print('\n')
                      print(df[i-5:i])
                  else:
                      break
              else:
                  print('Sorry, but this answer (\'{}\') is not valid or there was a typing mistake. Please try again.'.format(answer_raw_data))
          except KeyboardInterrupt:
              print('\nNo input taken')

def main():
    while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
