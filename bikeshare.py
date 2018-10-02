import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago','new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july','august', 'september', 'october', 'november', 'december']
days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']

def format_seconds(seconds):
    """
    convert seconds into days, hours, minutes, seconds
    Args:
        (int) seconds - total number of seconds
    Returns:
        (str)formatted_time - string of 'days, hours, minutes, seconds' converted from the input seconds.
    """

    days = seconds // (24 * 3600)

    seconds %= (24 * 3600)
    hours = seconds // 3600

    seconds %= 3600
    minutes = seconds // 60

    seconds %= 60
    seconds = seconds

    formatted_time = "{} days {} hours {} minutes {} seconds".format(days,hours,minutes,seconds)
    return formatted_time

def inputCity():
    """
    Returns:
        (str) city - name of the city to analyze
    """
    while True:
        city = input("Would you like to explore Chicago, New York City or Washington?(Enter the name please): ")
        city = city.lower()
        if city in cities:
            return city
        else:
            print("Enter a valid city name.Please try again!")

def inputMonth():
    """
    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """
    while True:
        month = input("Choose a month between January-December : ")
        month = month.lower()
        if((month in months) or (month=='all')):
            return month
        else:
            print("Enter a valid month .Please try again!")

def inputDay():
    """
    Returns:
        (str) day - name of the day to filter by, or "all" to apply no month filter
    """
    while True:
        day = input("Choose a day between Sunday-Monday : ")
        day = day.lower()
        if((day in days) or (day=='all')):
            return day
        else:
            print("Enter a valid day .Please try again!")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = 'all'
    day = 'all'

    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = inputCity()
    while True:
        filter_via = input("Do you want to filter your data via MONTH, DAY, BOTH or NONE? ").lower()
        if(filter_via == 'none'):
            print('-'*40)
            return city, month, day
        elif(filter_via == 'month'):
            month = inputMonth()
            break
        elif(filter_via == 'day'):
            day = inputDay()
            break
        elif(filter_via == 'both'):
            month = inputMonth()
            day = inputDay()
            break
        else:
            print("Enter only 'MONTH', 'DAY', 'BOTH' or 'NONE'")
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
        month = months.index(month) + 1

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
    print("Most common month: {} ({} times)".format(df['month'].mode()[0], df['month'].value_counts().mode()[0]))

    # display the most common day of week
    print("Most common day of week:  {} ({} times)".format(df['day_of_week'].mode()[0], df['day_of_week'].value_counts().mode()[0]))

    # find the most popular hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    print("Most common Start Hour:  {} ({} times)".format(df['hour'].mode()[0], df['hour'].value_counts().mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used Start station: {} ({} times)".format(df['Start Station'].mode()[0], df['Start Station'].value_counts()[0]))

    # display most commonly used end station
    print("Most commonly used End station: {} ({} times)".format(df['End Station'].mode()[0], df['End Station'].value_counts()[0]))

    # display most frequent combination of start station and end station trip
    most_frequent_station_combination = df['Start Station']+"--"+df['End Station']
    print("Most frequent combination of start station and end station trip: {} ({} times)".format(most_frequent_station_combination.mode()[0],most_frequent_station_combination.value_counts()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_travel = format_seconds(df['Trip Duration'].sum())
    print("Total travel time: ",total_time_travel)

    # display mean travel time
    total_time_travel_mean = format_seconds(df['Trip Duration'].mean())
    print("Total mean Travel time: ",total_time_travel_mean)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types: \n",df['User Type'].value_counts())

    # Display counts of gender
    if(city == 'new york city' or city == 'chicago'):
        print("counts of gender: \n",df['Gender'].value_counts())
    # Display earliest, most recent, and most common year of birth
        print("\nEarliest year of birth: ",df['Birth Year'].min())
        print("Most recent year of birth: ",df['Birth Year'].max())
        print("Most common year of birth: {} ({} times)\n".format(df['Birth Year'].mode()[0], df['Birth Year'].value_counts().iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    This function asks user if he wants to access the raw data too and shows 20
    rows at first and asks user if he wants to look at more data, everytime user
    enters 'Y' the function shows next 20 rows asnd so on.
    Args:
        df - DataFrame
    """
    print('-'*40)
    answer = input('\n\n Do you want to see the Raw data too?(Y for YES or any other key to exit.)').lower()
    while True:
        if(answer == 'y'):
            start = 0
            end = 20
            while True:
                print(df[start:end])
                more = input('\n\n Do you want to see more Raw data too?(Y for YES or any other key to exit.)').lower()
                if(more == 'y'):
                    start = end
                    end += 20
                else:
                    return
        else:
            return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
