"""                                                                main()
                                                                     |
                                                                     |while(restart == 'yes')
                                                                     |
            -----------------------------------------------------get_filter()-----------------------------------
            |                                                       |                                          |
            |                                                       |                                          |
            |day                                                    |month                                     |none
            |                                                       |                                          |
            |                                                       |                                          |
            |                                                       |                                          |
     filter_by_day(df)                                       filter_by_month(df)                          filterless(df)
            |                                                       |                                          |
            |                                                       |                                          |
            |                                                       |                                          |
time_stats(df,day_name)                              time_stats(df,month_number)                          time_stats(df)
station_stats(df,day_name)                           station_stats(df,month_number)                    station_stats(df)
user_stats(df,day_name)                              user_stats(df,month_number)                          user_stats(df)
trip_duration_stats(df,day_name)                     trip_duration_stats(df,month_number)        trip_duration_stats(df)
"""
import time
import pandas as pd
import numpy as np
import statistics as st

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = {'january': 1, 'february':2, 'march':3 ,'april':4,
          'may':5, 'june':6, 'july':7, 'august':8,
          'september':9, 'october':10, 'november':11, 'december':12}

days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city_choice = input('Please enter a city of the following: {chicago, new york city, washington}\n')
    while city_choice.lower() not in CITY_DATA:
        city_choice = input('Please enter a valid city '
                            '\n{chicago, new york city, washington} ')
    filename = CITY_DATA[city_choice.lower()]
    df = pd.read_csv(filename)
    extract_data(df)

    filter_choice = input('please specify what type of filters you would like by '
                          '{day ,month , none} "(none) for no time filter \n')

    while True:
        if filter_choice.lower() == 'day' or filter_choice.lower() == 'month' or filter_choice.lower() == 'none':
            return (filter_choice.lower(),df)
        else:
            filter_choice = input('please Enter a valid input of the following:'
                                  ' {day ,month , none} "(none) for no time filter \n')

def extract_data(df):
    """extracting more columns (features) from the original columns
    Args: df
    Returns: none """
    dateTimeVar = pd.to_datetime(df['Start Time'])  #creating a datetime variable
    #creating the new features
    df['hour'] = dateTimeVar.dt.hour;hour = df['hour']
    df['minute'] = dateTimeVar.dt.minute;min = df['minute']
    df['second'] = dateTimeVar.dt.second;sec = df['second']
    df['year'] = dateTimeVar.dt.year;year = df['year']
    df['month'] = dateTimeVar.dt.month;mon = df['month']
    # df['day'] = dateTimeVar.dt.day;day = df['day']
    df['day'] = dateTimeVar.dt.day_name();day_of_week = df['day']


def time_stats(df ,choosen = 'none'):
    """Displays statistics on the most frequent times of travel."""
    # Check if the required filter is month but wasn't available in the given dataset
    if (type(choosen) == int) and (choosen not in df['month'].unique()):
        print('No trips done in this month')
        return

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # print(choosen ,filter[0] ,df['hour'].mode()[0])
    # TO DO: display the most common month
    filter = df['month'] #assume user picekd MONTH filter
    if choosen in days: filter = df['day'] # if not, assigning filter to days

    li = []    #contains of all occurences of MONTH based on the required filter
    mon = 0    #most frequency MONTH (number)
    if choosen == 'none':
        mon = df['month'].mode()[0]
    else:
        for i in range(df.shape[0]):    #looping through the rows of dataset
            if filter[i] == choosen:
                li.append(df['month'][i]) #append if the indexed data equal to choosen filter a day_name or month_num
        mon = st.mode(li)   #by statistics module calc the most freq MONTH of the list

    for month_name, month_num in months.items(): #search in months dictionary to get the associated name of that most freq. month
        if month_num == mon:
            print('most popular month: {}'.format(month_name))
            break

    # TO DO: display the most common day of week
    # print(choosen ,filter[0] ,df['day'].mode()[0])

    #working the same as month above
    day, li = '', []
    if choosen == 'none':
        day = df['day'].mode()[0]
    else:
        for i in range(df.shape[0]):
            if filter[i] == choosen:
                li.append(df['day'][i])

        day = st.mode(li)
    print('most popular day: {}'.format(day))

    # TO DO: display the most common start hour
    # working the same as day above
    hr, li = 0, []

    if choosen == 'none':
        hr = df['hour'].mode()[0]
    else:
        for i in range(df.shape[0]):
            if filter[i] == choosen:
                li.append(df['hour'][i])
                # print(df['hour'][i])
                #
        hr = st.mode(li)
    print('most popular hour: {}'.format(hr))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df ,choosen = 'none'):
    """Displays statistics on the most popular stations and trip."""
    # Check if the required filter is month but wasn't available
    if (type(choosen) == int) and (choosen not in df['month'].unique()):
        print('No trips done in this month')
        return

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    filter = df['month']    #assume user picekd MONTH filter
    if choosen in days: filter = df['day']  # if not, assigning filter to days

    li_st, li_end = [], []  #saving occurrence of start station ,end station
    if choosen == 'none':
        start = df['Start Station'].mode()[0]
        end = df['End Station'].mode()[0]
    else:
        for i in range(df.shape[0]):
            if filter[i] == choosen:
                li_st.append(df['Start Station'][i])
                li_end.append(df['End Station'][i])
        start = st.mode(li_st)
        end = st.mode(li_end)
    print('Start station is: {}\nEnd station is: {}'.format(start, end))

    # TO DO: display most commonly used end station


    # TO DO: display most frequent combination of start station and end station trip
    li = []     #contains of all occurences of start to end stations based on the required filter
    mode = 0
    if choosen == 'none':
        for i in range(df.shape[0]):
            li.append(df['Start Station'][i] + '-' + df['End Station'][i])  #saving start and end station in a single element of list
    else:
        for i in range(df.shape[0]):
            if filter[i] == choosen:
                li.append(df['Start Station'][i] + '-' + df['End Station'][i])   #saving start and end station in a single element of list
    mode = st.mode(li)
    print('\n\nStart Station - End Station\n{} '.format(mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, choosen='none'):
    """Displays statistics on bikeshare users."""
    start_time = time.time()
    filter = df['month']    #assume user picekd MONTH filter
    if choosen in days: filter = df['day']  # if not, assigning filter to days
    # Check if the required filter is month but wasn't available in the given dataset
    if (type(choosen) == int) and (choosen not in df['month'].unique()):
        print('No trips done in this month')
        return

    print('\nCalculating User Stats...\n')

    # print(choosen ,filter[0] ,df['day'].mode()[0])

    # TO DO: Display counts of user types
    if 'User Type' not in df.columns :
        print('User Type info isn\'t provided for this city')
    subscriber, customer = 0, 0

    if choosen == 'none':
        print(df['User Type'].value_counts())
    else:
        for i in range(df.shape[0]):
            if filter[i] == choosen:
                if df['User Type'][i] == 'Subscriber':
                    subscriber += 1
                elif df['User Type'][i] == 'Customer':
                    customer += 1
        print('Membership type')
        print('no. of subscribers {}\nno. of customers {}'.format(subscriber, customer))

    # TO DO: Display counts of gender

    female, male = 0, 0
    if 'Gender' not in df.columns :
        print('Gender data isn\'t provided for this city')
    else:
        if choosen == 'none':
            print(df['Gender'].value_counts())
        else:
            for i in range(df.shape[0]):
                if filter[i] == choosen:
                    if df['Gender'][i] == 'Female':
                        female += 1
                    elif df['Gender'][i] == 'Male':
                        male += 1
            print('Gender of user:')
            print('no. of males {}\nno. of females {}'.format(male, female))

    # TO DO: Display earliest, most recent, and most common year of birth
    li = []
    if 'Birth Year' not in df.columns :
        print('Birth Year data isn\'t provided for this city')

    else:
        print('the oldest, the youngest ,and most popular year of birth')
        if choosen == 'none':
            print("({}, {} ,{})".format(min(df['Birth Year']), max(df['Birth Year']), df['Birth Year'].mode()[0])
                  )
        else:
            for i in range(df.shape[0]):
                if filter[i] == choosen:
                    li.append(df['Birth Year'][i])

            print("({}, {} ,{})".format(min(df['Birth Year']), max(df['Birth Year']), st.mode(li))
                  )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df ,choosen = 'none'):
    """Displays statistics on the total and average trip duration."""
    if (type(choosen) == int) and (choosen not in df['month'].unique()):
        print('No trips done in this month')
        return
    start_time = time.time()
    filter = df['month']
    if choosen in days: filter = df['day']
    print('\nCalculating Trip Duration...\n')
    # TO DO: display total travel time
    total_duration_secs ,average_duration_secs = 0,0    #saving total trip duration by seconds
    if choosen == 'none':
        total_duration_secs = df['Trip Duration'].sum()
    else:
        for i in range(df.shape[0]):
            if filter[i] == choosen:
                total_duration_secs += df['Trip Duration'][i]

    average_duration_secs = round(total_duration_secs / df.shape[0])

    dys = total_duration_secs // (24 * 3600); total_duration_secs = total_duration_secs % (24 * 3600) #calc. no. of days
    hrs = total_duration_secs // 3600;        total_duration_secs %= 3600   #calc. no. of hours
    mins = total_duration_secs // 60;         total_duration_secs %= 60     ##calc. no. of minute
    secs = total_duration_secs
    print('total traveling done ==> {} days {}:{}:{}'.format(int(dys),int(hrs),int(mins),int(secs)))
    # TO DO: display mean travel time
    avg_hours = average_duration_secs // 3600; avg_mins = average_duration_secs // 60
    avg_sec = average_duration_secs % 3600 % 60
    print('average traveling done ==> {}:{}:{}'.format(int(avg_hours),
                                                               int(avg_mins), int(avg_sec))) #get rid of fractions in time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def filter_by_day(df):
    day_choice = input("please enter what day to show {"
                       "Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'}\n")
    while day_choice.title() not in days:
        day_choice = input("please enter a valid input out of"
                           " the following days {Monday','Tuesday','Wednesday',"
                           "'Thursday','Friday','Saturday','Sunday'} \n")

    #days will be passed as week_day names(string)
    time_stats(df, day_choice.title())
    station_stats(df, day_choice.title())
    user_stats(df, day_choice.title())
    trip_duration_stats(df, day_choice.title())

def filter_by_month(df):
    month_choice = input("please enter what month to show 'january', 'february', 'march' 'april','may',"
                       " 'june', 'july', 'august','september', 'october', 'november', 'december' \n")
    while month_choice.lower() not in months:
        month_choice = input("please enter a valid input \n")

    #months will be passed as month numbers(int)
    time_stats(df, months[month_choice.lower()])
    station_stats(df, months[month_choice.lower()])
    user_stats(df, months[month_choice.lower()])
    trip_duration_stats(df, months[month_choice.lower()])

def filterless(df):
    time_stats(df)
    station_stats(df)
    user_stats(df)
    trip_duration_stats(df)

def main():

    while True:
        filter_type, df = get_filters() #filter_type contains one of the following (month, day, none) ,df contains the choosen file
        if filter_type.lower() == 'month':
            filter_by_month(df)
        elif filter_type.lower() == 'day':
            filter_by_day(df)
        else:
            filterless(df)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thanks for unsing our app! exit()')
            break

if __name__ == "__main__":
	main()
