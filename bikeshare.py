# Generic/Built-in Libraries
from datetime import timedelta
import time
# Other Libraries
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    isValid = False 

    while True: 
        city = str(input("\nEnter a city from the following list (Chicago, New York city, Washington) to explore bikeshare data: ").strip().lower())

        if city not in CITY_DATA.keys():
            print("\nYou entered an invalid city name. Please enter a valid city name from the specified list of cities")
            continue
        else:
            print("\nIt looks like you want to explore the bikeshare data for: '{}' ".format(city.title()))
            validate_input()
            break

    while True:
        month = str(input("\nFrom January to June, for what month do you want to filter the data?: ").strip().lower())

        if month not in months and month != 'all':
            print("\nYou entered an invalid month. Please enter a valid month (or \"all\" to select every month)")
            continue
        else:
            print("\nIt looks like you want to filter the bikeshare data by: '{}' ".format(month.title()))
            validate_input()
            break

    while True:
        day = str(input("\nFrom Sunday to Saturday, for what day do you want to filter the data?: ").strip().lower())

        if day not in weekdays and day != 'all':
            print("You entered an invalid day. Please enter a valid day (or \"all\" to select every day)")
            continue
        else:
            print("\nIt looks like you want to filter the bikeshare data by: '{}' ".format(day.title()))
            validate_input()
            break

    print("\nYou selected '{}' as city, '{}' as month, and '{}' as day. \nFiltering the bikeshare data by your parameters....".format(city.title(), month.title(), day.title()))
    print()
    print('-'*40)
    return city, month, day


def validate_input(): 
    
    while True: 
        isValid = str(input("Is your input correct? Type 'y' for Yes to continue or 'n' for No to restart: \n").strip().lower())
        if isValid not in ("y", "n"):
            print("\nInvalid input. Please try again")
            continue
        elif isValid == 'y':
            break
        else: 
            get_filters()


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
    
    print("\nThe program is loading the bikeshare data as per your selected parameters.")

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.day_name()
    df['Start_Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # to get the index/ number of selected month
        month = months.index(month) + 1

        # month column is in type(integer)
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_Week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    
    # to calculate the execution time
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print("1. The most common month was: ", str(months[most_common_month-1]).title())

    # display the most common day of week
    most_common_day = df['Day_of_Week'].mode()[0]
    print("2. The most common day of the week was: {}".format(most_common_day))

    # display the most common start hour
    most_common_start_hour = df['Start_Hour'].mode()[0]
    print('3. The most common start hour was:', most_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    
    # to calculate the execution time
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("1. Most commonly used start station was: '{}'".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("2. Most commonly used end station was: '{}'".format(most_common_end_station))
    
    # display most frequent combination of start station and end station trip
    df['Start_End_Station_Trip_Combination'] = (df['Start Station'] + ' - ' + df['End Station'])
    most_frequent_station_trip_combination = str(df['Start_End_Station_Trip_Combination'].mode()[0])
    print("3. The most frequent combination of start station and end station trip is '{}'".format(most_frequent_station_trip_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    # to calculate the execution time
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    t2 = total_travel_time.astype('float64', copy=False)
    time_in_duration = timedelta(seconds=t2)
    print("1. The total travel time in seconds is: '{}' which is converted to '{}' in duration. ".format(total_travel_time, time_in_duration))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("2. The average (mean) travel time in seconds is: '{}' ".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    
    # to calculate the execution time
    start_time = time.time()

    # Display counts of user types
    user_types_count = df["User Type"].value_counts()
    print("1. The counts of user types: ")
    print(user_types_count)

    # Display counts of gender
    try:
        if "Gender" in df.columns: 
            gender_count = df['Gender'].value_counts().to_string()
            
            # to count null values.
            missing_values_count = df["Gender"].isna().sum()
            
            print("\n2. Counts of Gender: \n{}".format(gender_count))
            print("\n*NOTE: There are '{}' missing values (NaN) in the 'Gender' column".format(missing_values_count))
        else:
            print("\nNo column named 'Gender' exists in this dataset")
    except KeyError:
        print("There is no data of user gender for {}.".format(city.title()))
        

    # Display earliest, most recent, and most common year of birth
    try:
        if "Birth Year" in df.columns:
            earliest_birth_year = df['Birth Year'].min()
            most_recent_birth_year = df['Birth Year'].max()
            most_common_birth_year = df['Birth Year'].mode()[0]
            print("\n3. Earliest birth year: '{}'. \nMost recent birth year: '{}'. \nMost common birth year: '{}'.".format(earliest_birth_year, most_recent_birth_year, most_common_birth_year))
        else:
            print("\nNo column named 'Birth Year' exists in this dataset")
    except:
        print("There is no data of birth year for {}.".format(city.title()))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df, mark_place): 
    """
    Displays 5 lines of raw data.
    
    mark_place - this variable holds where the user last stopped
    """
    
    display_raw_input = input("\nWould you like to see raw data? Enter 'yes' or 'no'\n").strip().lower()
    if display_raw_input in ("yes", "y"):
        while True:
            for i in range(mark_place, len(df.index)):
                print("\n")
                print(df.iloc[mark_place:mark_place+5].to_string())
                print("\n")
                mark_place += 5

                show_next_five_input = input("\nWould you like to see the next 5 rows? Enter 'yes' or 'no'\n").strip().lower()
                if show_next_five_input == "yes" or  show_next_five_input == "y":
                    continue
                else:
                    print("\nThanks for viewing the Raw data !!!")
                    break
            break

    return mark_place


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        mark_place=0

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df, mark_place)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
