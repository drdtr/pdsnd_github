"""
Solution for Bikeshare data analysis assignment in Udacity course https://www.udacity.com/course/programming-for-data-science-nanodegree--nd104
"""

import calendar
import datetime as dt
import time

import pandas as pd

# city names and corresponding csv data files
city_filenames = {'chicago': 'chicago.csv',
                  'new york city': 'new_york_city.csv',
                  'washington': 'washington.csv'}


# mapping of names to numbers for days of week
day_of_week_dict = dict((d.lower(), n) for n, d in enumerate(calendar.day_name))

# mapping of names to numbers for months
month_dict = dict((d.lower(), n) for n, d in enumerate(calendar.month_name) if n > 0)


# Column names
class Col:
    trip_number = "Trip Number"
    start_time = "Start Time"
    end_time = "End Time"
    trip_duration = "Trip Duration"
    start_station = "Start Station"
    end_station = "End Station"
    user_type = "User Type"
    gender = "Gender"
    birth_year = "Birth Year"
    month = "month"
    day_of_week = "day_of_week"
    month_name = "month_name"
    day_name = "day_name"
    hour = "hour"


def input_str_from_valid(valid_inputs, input_msg, err_msg, lower_case=True):
    """
    Asks the user to input a value and returns it. Space at beginning and end of the input will be removed.

    If the input is not in the given set of valid_inputs then the err_msg is shown and the input request is repeated.

    Spaces at the beginning and the end of the string will be removed.

    :param lower_case: if True then the user input will be converted to lower case. The valid_inputs must then also contain lower case strings.
    """
    res = None

    while res is None:
        res = input(input_msg).strip()
        if lower_case:
            res = res.lower()
        if res not in valid_inputs:
            print(err_msg)
            res = None

    return res


def input_yes_no(msg) -> bool:
    """
    Asks the user to answer the question given by msg and returns True iff the user entered 'yes'.
    Upper/lower case and spaces at beginning/end of the string will be ignored.
    """
    return input('\n' + msg + ' Enter yes or no:\n').strip().lower() == 'yes'


def pd_options():
    pd.options.display.width = 220
    pd.options.display.max_columns = 20


def print_hline(length = 80):
    print("-" * length)


def print_duration(duration):
    print("This took {:.1f} seconds.".format(duration))


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
    city = input_str_from_valid(
        valid_inputs=city_filenames.keys(),
        input_msg="Enter city name from {}:".format(list(city_filenames.keys())),
        err_msg="Unknown city.")

    # get user input for month (all, january, february, ... , june)
    month = input_str_from_valid(
        valid_inputs={'all'}.union(month_dict.keys()),
        input_msg="Enter 'all' or month from {}:".format(list(month_dict.keys())),
        err_msg="Unknown month.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input_str_from_valid(
        valid_inputs={'all'}.union(day_of_week_dict.keys()),
        input_msg="Enter 'all' or week day from {}:".format(list(day_of_week_dict.keys())),
        err_msg="Unknown week day.")

    print()
    print_hline()
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
    print("Loading data for city={} and filtering by month={}, day={}".format(city, month, day))
    start_time = time.time()
    filename = city_filenames[city]
    df = pd.read_csv(filename)
    df.rename(columns={df.columns[0]: Col.trip_number}, inplace=True)

    # convert the Start Time column to datetime
    df[Col.start_time] = pd.to_datetime(df[Col.start_time])

    # add columns with month, day of week, and hour from Start Time
    df[Col.month] = df[Col.start_time].dt.month
    df[Col.day_of_week] = df[Col.start_time].dt.dayofweek
    df[Col.month_name] = df[Col.start_time].dt.day_name()
    df[Col.day_name] = df[Col.start_time].dt.month_name()
    df[Col.hour] = df[Col.start_time].dt.hour

    if month != 'all':
        month_num = month_dict[month]
        df = df[df[Col.month] == month_num]

    if day != 'all':
        day_num = day_of_week_dict[day.lower()]
        df = df[df[Col.day_of_week] == day_num]

    # After probably filtering out some records, reset the index so that it starts a 0 and is contiguous
    df.reset_index(inplace=True, drop=True)

    print("Data row count: {} ".format(len(df)))

    print()
    print_duration(time.time() - start_time)
    print_hline()

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_mode = df[Col.month].mode()[0]
    print("The most common month is {}".format(calendar.month_name[month_mode]))

    # display the most common day of week
    day_mode = df[Col.day_of_week].mode()[0]
    print("The most common day of week is {}".format(calendar.day_name[day_mode]))

    # display the most common start hour
    hour_mode = df[Col.hour].mode()[0]
    print("The most common hour is {}".format(hour_mode))

    print()
    print_duration(time.time() - start_time)
    print_hline()


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_mode = df[Col.start_station].mode()[0]
    print("The most commonly used start station is {}".format(start_station_mode))

    # display most commonly used end station
    end_station_mode = df[Col.end_station].mode()[0]
    print("The most commonly used end station is {}".format(end_station_mode))

    # display most frequent combination of start station and end station trip
    start_end_stations = df[Col.start_station].combine(df[Col.end_station], lambda a, b: (a, b))
    start_end_stations_mode = start_end_stations.mode()[0]
    print("The most frequent combination of start station and end station is {}".format(start_end_stations_mode))

    print()
    print_duration(time.time() - start_time)
    print_hline()


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df[Col.trip_duration].sum()
    print("Total travel time is {} seconds = {}".format(
        total_trip_duration, dt.timedelta(seconds = float(total_trip_duration))))

    # display mean travel time
    mean_trip_duration = df[Col.trip_duration].mean()
    print("Mean travel time is {:.2f} seconds = {}".format(
        mean_trip_duration, dt.timedelta(seconds = round(mean_trip_duration, 2))))

    print()
    print_duration(time.time() - start_time)
    print_hline()


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df[Col.user_type].value_counts()
    print("User type counts:")
    print(user_type_counts.to_string())

    # Display counts of gender
    try:
        gender_counts = df[Col.gender].value_counts()
        print("\nGender counts:")
        print(gender_counts.to_string())
    except:
        print("\nNo gender data available.")

    # Display earliest, most recent, and most common year of birth
    print()
    try:
        print("The earliest year of birth is {}".format(int(df[Col.birth_year].min())))
        print("The most recent year of birth is {}".format(int(df[Col.birth_year].max())))
        print("The most common year of birth is {}".format(int(df[Col.birth_year].mode()[0])))
    except:
        print("No birth dates available.")

    print()
    print_duration(time.time() - start_time)
    print_hline()


def show_raw_data(df: pd.DataFrame, chunk_size = 5):
    """
    Asks the user if he/she wants to see a chunk of raw data rows, and if yes, displays them.
    After each chunk, the user is asked if he/she wants to see more.
    Returns when the user enters anything other than 'yes' or when all data has been shown.
    """
    curr_pos = 0
    keep_going = curr_pos < len(df) and input_yes_no("Would you like to see first {} raw data entries?".format(chunk_size))
    while keep_going:
        print(df[curr_pos: curr_pos + chunk_size])
        curr_pos += chunk_size
        keep_going = curr_pos < len(df) and input_yes_no("Would you like to see {} more raw data entries?".format(chunk_size))


def main():
    keep_going = True
    while keep_going:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            show_raw_data(df)
        else:
            print("No data found for the input.")

        keep_going = input_yes_no('Would you like to restart?')


if __name__ == "__main__":
    pd_options()
    main()