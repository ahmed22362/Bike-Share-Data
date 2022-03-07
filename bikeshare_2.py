import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',  'Sunday ']
months = ['january', 'february', 'march', 'april', 'may', 'june']

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
    c = str(input('please input city (Chicago as CH, New Yourk as NY, Washington as WA) you want to analyze\n')).lower()
    if c == 'ch' or c == 'chicago':
            city = 'chicago'
    elif c == 'ny' or c == 'new yourk' or c == 'new yourk city':
        city = 'new york'
    elif c == 'wa' or c == 'washington':
        city = 'washington'
    else: 
        city = None

    # get user input for month (all, january, february, ... , june)
   
    month = input('Enter which you want to filtered by or \"all\" to apply no month filter (january, february, ....,june )\n')
    if month != 'all':
        try:
            val = int(month)
            month = val 
            if val > 6 :
                month = None
        except ValueError:
            if month not in months: 
                month = None
            else:
                month = months.index(month.lower()) +1


    day = input('enter the name of the day of week to filter by(monday, tuesday,... sunday), or \'all\' to apply no day filter\n Tip: if you enter a number start with monday \n')
    if day != 'all':
        try:
            val = int(day)
            if val > 7:
                day = None
            else:
                day = days[val-1]
        except ValueError:
            if day not in days :
                day = None
            else: 
                day = day.title()
    # get user input for day of week (all, monday, tuesday, ... sunday)

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
    
    #filter by month
    
    df['Start Time'] =pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() 


    if month != 'all':
        df = df[df['month']== month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    common_month = df['month'].value_counts().idxmax()
    num_cmmon_month = df['month'].value_counts().max()
    print('the most common month is {} with count {} '.format(common_month , num_cmmon_month) )


    # display the most common day of week
    common_day = df['day_of_week'].value_counts().idxmax()
    num_common_day =  df['day_of_week'].value_counts().max()
    print('the most cmmon day is {} with count {}'.format(common_day , num_common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].value_counts().idxmax()
    num_common_hour = df['hour'].value_counts().max()
    print('the most common hour in 24 Format is {} with count of {}'.format(common_hour, num_common_hour) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_starion = df['Start Station'].value_counts().idxmax()
    print('the most common start station is' ,common_start_starion)
    # display most commonly used end station
    
    common_end_starion = df['End Station'].value_counts().idxmax()
    print('the most common end station is ' , common_end_starion)

    # display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station' , 'End Station']).size().idxmax()
    
    print('this is the most popular trip' , common_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    day = total // 1440
    left_min = total % 1440
    hour = left_min //60
    min = left_min -hour*60
    print('the total time traviling in mints is {} or {} day(s) {} hour(s) {} min(s)'.format (total , day , hour, min))
    # display mean travel time
    mea = df['Trip Duration'].mean()
    print('the mean duration of trip is', round(mea , 2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_type = df['User Type'].value_counts()
    print('the numbers of each cutomer type are\n' , count_type.to_string())
    
    try:
        # Display counts of gender
        counts_of_gender  = df['Gender'].value_counts()
        print('the numbers of each gender are\n' , counts_of_gender.to_string())

        # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].value_counts().idxmax()
        print('\n this is earliest',str(int(earliest)) + ' \n this is the most recent ',str(int(recent)) + '\n and this is the most common year ', str(int(common)) )
    except KeyError:
        print('' , sep='')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
        Display 5 rows of the raw data at a time if the user asked.

        Args:
            (Data Frame) df - name of the data frame which the data retrived from
        
        Returns:
            None      
    """
    i = 5
    show = input('Do you want to see the raw data ?\n').lower() 
    
    while True :
        if show =='yes':
            print(df.head(i).to_string())
            i+=5
            show = input('Do you want to see the more raw data ?\n').lower() 

        elif show == 'no':
            break
        else :
            show = input('\nyour input is invalid enter either yes or no \n').lower()
            





def main():

    
    #city , month , day = get_filters()
    # df = load_data(city= 'chicago' , month=  'march' , day= 1 )
    # print(df)
    #time_stats(df)
    #station_stats(df)
    #trip_duration_stats(df)
    #user_stats(df)
    
    
    while True:
        city, month, day = get_filters()
        if(city == None):
            print('enter a valid city')
            continue
        elif(month == None):
            print('enter a valid month')
            continue
        elif(day == None):
            print('enter a valid day')
            continue

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)


        restart = str(input('\nWould you like to restart? Enter yes or no.\n')).lower()
        if restart =='yes':
            continue
        elif restart == 'no':
            break
        else:
            print('enter yes or no')
            restart = str(input('\nWould you like to restart? Enter yes or no.\n')).lower()


        
            

if __name__ == "__main__":
	main()
