import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': './chicago.csv',
              'new york city': './new_york_city.csv',
              'washington': './washington.csv' }

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
        city = input('Would you like to see data for Chicago, New York City or Washington?\n')
        city = city.lower()
        try:
            CITY_DATA[city]
            break
        except Exception as e:
            print("Exception occurred: {}".format(e))
            print("Please give a valid selection")


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Would you like to see data for a special month or for all months?\nChoose one month between january and june or choose all\n')
        month =  month.lower()
        month_test = ['january', 'february', 'march', 'april', 'may', 'june','all']
        try:
            month_test.index(month)
            break
        except Exception as e:
            print("Exception occurred: {}".format(e))
            print("Please give a valid selection. Choose 'january', 'february', 'march', 'april', 'may', 'june' or 'all'")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Would you like to see data for a special day of the week or for all days?\n')
        day = day.lower()
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday','all']
        try:
            days_of_week.index(day)
            break
        except Exception as e:
            print("Exception occurred: {}".format(e))
            print("Please give a valid selection. Choose 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' or 'all'")
    

    print('-'*40)
    return city, month, day

def raw_data(city):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Raw Data display if requested
    raw_data = input('Would you like to see first 5 lines of raw data? Please enter yes/y or no/n.\n')
    i=0
    while raw_data == 'yes' or raw_data == 'y':
        print(df.iloc[i:i+5])
        raw_data = input('Would you like to see next 5 lines of raw data? Please enter yes/y or no/n.\n')
        i += 5


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
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

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


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month, if not filtered by one month
    if month == 'all':
        df['month'] = df['Start Time'].dt.month

        # find the most popular month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        popular_month = months[df['month'].mode()[0]-1]

        print('Most Popular Month:', popular_month.title())

    # display the most common day of week, if not filtered by one day
    if day == 'all':
        df['day_of_week'] = df['Start Time'].dt.strftime("%A")

        # find the most popular day of week
        popular_day = df['day_of_week'].mode()[0]

        print('Most Popular Day of week:', popular_day)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_stat=df['Start Station'].mode()[0]
    print('Most Popular Start Station:', most_start_stat,'\n')
    # display most commonly used end station
    most_end_stat=df['End Station'].mode()[0]
    print('Most Popular End Station:', most_end_stat,'\n')

    # display most frequent combination of start station and end station trip
    most_combination=df.groupby('Start Station')['End Station'].value_counts()
    print('Most popular combination of start and end station is:\n',most_combination.head(1).to_string())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_timedelta= datetime.timedelta(seconds=int(df['Trip Duration'].sum()))
    total_travel_time = [total_travel_timedelta.days, total_travel_timedelta.seconds//3600, total_travel_timedelta.seconds//60%60, total_travel_timedelta.seconds%60]
    
    print('Total trip duration is about:',total_travel_time[0],'days',total_travel_time[1],'hours',total_travel_time[2],'minutes and',total_travel_time[3],'secondss.\n')

    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()/60
    print('Mean trip duration is about:',mean_travel_time,' minutes.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Different types of user:\n',user_types.to_string(),'\n')

    # Display counts of gender
    # Only for Chicago and New York City available
    try:
        gender_count =df['Gender'].value_counts()
        print('Different counts of gender:\n',gender_count.to_string(),'\n')
    except:
        print('No Data about Gender available.\n')

    # Display earliest, most recent, and most common year of birth
    # Only for Chicago and New York City available
    try:
        youngest=df['Birth Year'].max()
        oldest=df['Birth Year'].min()
        most_year=df['Birth Year'].mode()[0]
        print('Year of Birth of youngest users:',youngest,'\n')
        print('Year of Birth of oldest users:',oldest,'\n')
        print('Most common Year of Birth:',most_year,'\n')
    except:
        print('No Data about Year of Birth available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats_choose = input("Would you like to see statistics on the most frequent times of travel?\nPlease Enter y/yes or no.\n")
        if time_stats_choose == 'yes' or time_stats_choose == 'y':
            time_stats(df,month,day)
        
        station_stats_choose = input("Would you like to see statistics on the most popular stations?\nPlease Enter y/yes or no.\n")
        if station_stats_choose == 'yes' or station_stats_choose == 'y':
            station_stats(df)
        
        trip_duration_stats_choose = input("Would you like to see statistics on the duration of travel?\nPlease Enter y/yes or no.\n")
        if trip_duration_stats_choose == 'yes' or trip_duration_stats_choose == 'y':
            trip_duration_stats(df)
        
        user_stats_choose = input("Would you like to see user statistics?\nPlease Enter y/yes or no.\n")
        if user_stats_choose == 'yes' or user_stats_choose == 'y':
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
