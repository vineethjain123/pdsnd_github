import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
   # take user input for name of city (chicago,new york,washington).
    while True:
        city = input("Enter one of the cities you want to see data for:\n Chicago, New York, Washington\n").lower()
        if city in cities:
            break
        else:
            print('Enter valid city!')
    # take user input for month
    while True:
        month = input("Enter name of month you want to see data for:\n Enter months between January to June only. If you don't want to filter by month enter 'all'\n").lower()
        if month in months:
            break
        else:
            print('Enter Valid Month!')
    # take user input for day
    while True:
          day = input("Enter day of week you want to see data for:\n If you don't want to filter by day enter 'all'\n").lower()
          if day in days:
                  break
          else:
                  print('Enter Valid Day!')

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
# load required file into data frame
    df = pd.read_csv(CITY_DATA[city])

# convert Start Time and End Time columns into correct date format yyyy-mm-dd
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

# Take out month from Start Time into new column named month
    df['month'] = df['Start Time'].dt.month

# filter by month
    if month != 'all':
   # Make use of index of months list to get corresponding integer value
      months = ['january', 'february', 'march', 'april', 'may', 'june']
      month = months.index(month) + 1

    # filter by month to create new data frame
      df = df[df['month'] == month]

    # Take out day from Start TIme column into new column named day_week
    df['day_week'] = df['Start Time'].dt.weekday_name

   # Filter by day of week if to be used
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display common month
    common_month = df['month'].value_counts().idxmax()

    # Change number to month
    if common_month == 1:
        common_month = "January"
    elif common_month == 2:
        common_month = "February"
    elif common_month == 3:
        common_month = "March"
    elif common_month == 4:
        common_month = "April"
    elif common_month == 5:
        common_month = "May"
    elif common_month == 6:
        common_month = "June"
    print ("Most Common Month is: ",common_month)

    # Display common day of week
    print("Most common day of week is: ", df['day_week'].value_counts().idxmax())


    # Display common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("Most common hour is: ",df['hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used Start Station
    print("Most common used start station is: ", df['Start Station'].value_counts().idxmax())

    # Display most commonly used end station
    print("Most common used end station is: ", df['End Station'].value_counts().idxmax())

    # Display most frequent combination of start station and end station trip
    most_common_start_and_end_stations = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print("Most frequent combination of start station and end station is ", most_common_start_and_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 3600.0
    print("Total travel time is ", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 3600.0
    print("Mean travel time is ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Count of User Type ", user_types)

    # Display counts of gender
    try:
          gender_count = df['Gender'].value_counts()
          print("Count of Gender ", gender_count)
    except:
          print("No gender data available for {} city".format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_birth = int(df['Birth Year'].min())
        recent_year_birth = int(df['Birth Year'].max())
        most_common_year_birth = int(df['Birth Year'].value_counts().idxmax())
        print("Earliest year of birth is ",earliest_year_birth)
        print("Recent year of birth is ",recent_year_birth)
        print("Common year of birth is ",most_common_year_birth)
    except:
           print("No birth year data available for {} city".format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def ind_data(df):
    # Prompt user if they want to see individual trip data.
    start_data = 0
    end_data = 5
    df_length = len(df.index)

    while start_data < df_length:
        raw_data = input("\n Do you want to see individual data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':

            print("\nDisplaying 5 rows of data only.\n")
            if end_data > df_length:
                end_data = df.length
            print (df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        ind_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
