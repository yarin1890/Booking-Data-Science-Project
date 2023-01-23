#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pdb
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
# from datetime import datetime
import datetime
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn import preprocessing

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


def split_checkin_to_date_coulmns(df):
    
    day_date_array = [] 
    month_array = [] 
    year_array = [] 
    day_in_a_week_array = []
    week_days_js = {
            0 : 2,
            1 : 3,
            2 : 4,
            3 : 5,
            4 : 6, 
            5 : 7, 
            6 : 1 , 

        }
    for part in df:
        date = datetime.datetime.strptime(part ,'%Y-%m-%d').date()
        day = date.day
        month = date.month
        year = date.year     
        day_in_week = week_days_js[datetime.date(day=day, month=month, year=year).weekday()]
        day_date_array.append(day)
        month_array.append(month)
        year_array.append(year)
        day_in_a_week_array.append(day_in_week)
       
        
    return day_in_a_week_array,day_date_array,month_array,year_array


# In[3]:


def add_new_coulmns_dates(df,day_in_a_week_array,day_date_array,month_array,year_array):
    df.insert(loc=1, column='day', value=day_in_a_week_array)
    df.insert(loc=2, column='date_day', value=day_date_array)
    df.insert(loc=3, column='month', value=month_array)
    df.insert(loc=4, column='year', value=year_array)
    
    return df2
    


# In[4]:


def create_mean_on_graph(df2,i):
    
    ## https://stackoverflow.com/questions/65693824/pandas-get-column-average-for-rows-with-a-certain-value ## 
    
    hotel_price_mean = df2.groupby("hotel_name")["hotel_price"].mean()
    available_rooms_mean = df2.groupby("hotel_name")["available_rooms"].mean()
    hotel_rating_mean = df2.groupby("hotel_name")["hotel_rating"].mean()
    preferred_hotel_mean = df2.groupby("hotel_name")["preferred_hotel"].mean()
    nnumber_of_reviews_meas = df2.groupby("hotel_name")["number_of_reviews"].mean()
    distance_from_center_mean = df2.groupby("hotel_name")["distance_from_center"].mean()
    stars_count_mean = df2.groupby("hotel_name")["stars_count"].mean()
    new_hotel_mean = df2.groupby("hotel_name")["new_hotel"].mean()
#     month_mean = df2.groupby("hotel_name")["month"].mean()
    
    new_df = pd.DataFrame({
                "month": i,
                "hotel_name" : hotel_price_mean.keys(), 
                "available_rooms" : available_rooms_mean.values,
                "hotel_price" : hotel_price_mean.values,
                "hotel_rating" : hotel_rating_mean.values,
                "preferred_hotel" : preferred_hotel_mean.values, 
                "number_of_reviews" : nnumber_of_reviews_meas.values,
                "distance_from_center" : stars_count_mean.values, 
                "stars_count" : stars_count_mean.values,
                "new_hotel" : new_hotel_mean.values,
                })    
    return new_df


# In[5]:


def return_r_squre(df,i):
    print("size of rows: "+str(len(df)))
    print("free available hotels: "+ str(len(df[df['available_rooms'] == 10])))
    df.drop(df[df['available_rooms'] == 10].index, inplace = True)
    df = create_mean_on_graph(df,i)
    x = df[[
    'month',    
    'stars_count',
    'hotel_price',
     'number_of_reviews',
     'distance_from_center',
    'hotel_rating',
     ]]

 ## https://labs.vocareum.com/main/main.php?m=editor&asnid=537364&stepid=537365&hideNavBar=1 ## 


    y = df['available_rooms']

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 10)

    lr = LinearRegression()
    lr.fit(X = x, y=y)
    predictions = lr.predict(X_test)

    pred = pd.DataFrame({'Actual': y_test.tolist(), 'Predicted': predictions}).head(25)





    print("Slope:",lr.coef_)
    print("Intercept:",lr.intercept_)

    print("R2:",lr.score(x,y))
    print("R2:",r2_score(y,lr.predict(x.values)))

    pred.head(100)


# In[6]:


df = pd.read_csv('./data/Hotels365Day.csv')
df.sort_values('check_in', inplace=True)
df2 = df.iloc[:, 1:].reset_index(drop=True)
dates_coulmns = df2['check_in']

day_in_a_week_array,day_date_array,month_array,year_array = split_checkin_to_date_coulmns(dates_coulmns)
## this is the new data frame after split the date to 3 coulmns ## 
df2 = add_new_coulmns_dates(df2,day_in_a_week_array,day_date_array,month_array,year_array)

df2.drop(df2[df2['hotel_rating'] < 3].index, inplace = True)
df2.drop(df2[df2['number_of_reviews'] < 10].index, inplace = True)


  
for i in range(1,13):
    print("month number "+ str(i))    
    return_r_squre(df2[df2['month'] == i],i)
    print('-----------------\n\n')





