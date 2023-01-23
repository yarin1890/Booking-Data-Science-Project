#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import pdb
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns
from matplotlib import ticker
import seaborn as sns
import matplotlib as mpl
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


def check_for_missing_index_values(df):
    index_list = [1,2,3,4,5,6,7,10]
    for idx in index_list:
        try:
            temp = df.loc[idx][0]
        except:
            df.loc[idx] = [0]

    df = df.sort_index()
    return df


# In[3]:


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


# In[4]:


def add_new_coulmns_dates(df,day_in_a_week_array,day_date_array,month_array,year_array):
    df.insert(loc=1, column='day', value=day_in_a_week_array)
    df.insert(loc=2, column='date_day', value=day_date_array)
    df.insert(loc=3, column='month', value=month_array)
    df.insert(loc=4, column='year', value=year_array)
    
    return df2


# In[5]:


# df_june = df2[df2['check_in'].dt.strftime('%Y-%m') == '2023-06']


def create_graph(df,df_result,year,month,first_time_run):
    if month<10:
        df_by_month = df[df['check_in'].dt.strftime('%Y-%m') == str(year)+'-0'+str(month)]
    else:
        df_by_month = df[df['check_in'].dt.strftime('%Y-%m') == str(year)+'-'+str(month)]
    df_groupby_available_rooms = df_by_month['available_rooms'].value_counts()
    how_many_available_rooms = sorted(df_groupby_available_rooms.keys().tolist())
    df_final = pd.DataFrame(df_groupby_available_rooms,index=how_many_available_rooms)
    if(first_time_run):
        
        df_temp = pd.DataFrame(index=how_many_available_rooms)
        ## https://www.geeksforgeeks.org/python-pandas-dataframe-assign/ ## 
        df_temp = df_temp.assign(month_name=df_final.values)
        df_temp = check_for_missing_index_values(df_temp)
        df_temp.rename(columns = {'month_name':str(month)+"."+str(year)[int(len(str(year))/2):]}, inplace = True)
        df_result = df_temp
       
    else:
        try:
            df_final = check_for_missing_index_values(df_final)
            df_result = df_result.assign(month_name=df_final.values)
        except:
            pdb.set_trace()
        df_result = check_for_missing_index_values(df_result)
        df_result.rename(columns = {'month_name':str(month)+"."+str(year)[int(len(str(year))/2):]}, inplace = True)

        
    return df_result
    


# In[6]:


def get_grapah_for_avaialble_room_by_paramater(df2,first_month,year,parm,parameter_type):
    i = first_month
    month = 13 
    df_result = pd.DataFrame()
    first_time_run = True
    while(month != 0):
        df_result = create_graph(df2,df_result,year,i,first_time_run)
        first_time_run = False
        if( i == 12 ):
            i = 1 
            year = str(int(year)+1)
        else:
            i = i +1

        month= month -1
    
    df_result = df_result.T
    
    df_result_part1 = df_result.drop(df_result.index[6:13])
    df_result_part2 = df_result.drop(df_result.index[0:6])
    
    ## https://datatofish.com/bar-chart-python-matplotlib/ ##

    df_result_part1.plot(kind='bar')
    plt.ylabel('Available Rooms by '+ '\n'+str(parm)+ '\n'+parameter_type)
    plt.xlabel('Month and Year')

    
     
    df_result_part2.plot(kind='bar')
    plt.ylabel('Available Rooms by '+ '\n'+str(parm)+ '\n'+parameter_type)
    plt.xlabel('Month and Year')

    
    plt.show()

    return 


# In[7]:


def add_date_coulmns(df2):
    dates_coulmns = df2['check_in']
    day_in_a_week_array,day_date_array,month_array,year_array = split_checkin_to_date_coulmns(dates_coulmns)
    df2 = add_new_coulmns_dates(df2,day_in_a_week_array,day_date_array,month_array,year_array)
    return df2


# In[8]:


def get_graph_by_paramter(df2,parameter,parameter_list,parameter_type):
    df2['check_in'] = pd.to_datetime(df2['check_in'])  
    first_month = df2['check_in'][0].month
    year = df2['check_in'][0].year
    
    if (parameter_type == "Star" ) :
        for parm in parameter_list:
            df_by_param = df2[df2[parameter] == parm]
            df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
            get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,parm,parameter_type)
    
    
    if (parameter_type == "Distance From Center" ) :

        ### distance_from_center < 0.5 ##
        parm = parameter_list[0]
        df_by_param = df2[parameter_list[0] > df2[parameter]]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm)+">",parameter_type)
        
        ##    0.5 < distance_from_center < 1 ##
        parm = "0.5 < distance < 1 "
        df_by_param = df2[  (parameter_list[0] < df2[parameter]) &  ( parameter_list[1] > df2[parameter])]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm),parameter_type)
    
    
        ## distance_from_center > 1 ## 
        
        parm = "distance > 1 "
        df_by_param = df2[parameter_list[1] < df2[parameter]]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm),parameter_type)
            
            
    if (parameter_type == "Hotel Rating" ) :

       ### Hotel Rating < 8 ##
        parm = parameter_list[0]
        df_by_param = df2[parameter_list[0] > df2[parameter]]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm)+">",parameter_type)
        
        ##    8 < Hotel Rating < 9 ##
        parm = "8 < rating < 9 "
        df_by_param = df2[  (parameter_list[0] < df2[parameter]) &  ( parameter_list[1] > df2[parameter])]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm),parameter_type)
    
    
        ## Hotel Rating > 9 ## 
        
        parm = "rating > 9 "
        df_by_param = df2[parameter_list[1] < df2[parameter]]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm),parameter_type)
        
        
        
    if (parameter_type == "Hotel Price" ) :

       ### Hotel Price < 300 ##
        parm = parameter_list[0]
        df_by_param = df2[parameter_list[0] > df2[parameter]]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm)+">",parameter_type)
        
        ##    300 < Price < 600 ##
        parm = "300 < Price < 600 "
        df_by_param = df2[  (parameter_list[0] < df2[parameter]) &  ( parameter_list[1] > df2[parameter])]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm),parameter_type)
    
        ## 600 < Price < 1000  ## 
        parm = "600 < Price < 1000 "
        df_by_param = df2[  (parameter_list[1] < df2[parameter]) &  ( parameter_list[2] > df2[parameter])]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm),parameter_type)
        
         ## 1000 < Price < 2000 ## 
        parm = "1000 < Price < 2000 "
        df_by_param = df2[  (parameter_list[2] < df2[parameter]) &  ( parameter_list[3] > df2[parameter])]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm),parameter_type)
    
        
        ## Price > 2000 ##
        parm = "Price > 2000 "
        df_by_param = df2[parameter_list[3] < df2[parameter]]
        df_by_param = df_by_param.iloc[:, :].reset_index(drop=True)
        get_grapah_for_avaialble_room_by_paramater(df_by_param,first_month,year,str(parm),parameter_type)
        
    return 
    


# In[9]:





def get_graph_for_stars_count(df):
    parameter = 'stars_count'
    parameter_list = [0,3,4,5]
    parameter_type = "Star"
    get_graph_by_paramter(df,parameter,parameter_list,parameter_type)
    return

def get_graph_for_distance_from_center(df):
    parameter = "distance_from_center"
    parameter_list = [0.5,1] 
    parameter_type = "Distance From Center"
    get_graph_by_paramter(df,parameter,parameter_list,parameter_type)
    return

def get_graph_for_hotel_rating(df):
    parameter = "hotel_rating"
    parameter_list = [8,9] 
    parameter_type = "Hotel Rating"
    get_graph_by_paramter(df,parameter,parameter_list,parameter_type)
    return

def get_graph_for_hotel_price(df):
    parameter = "hotel_price"
    parameter_list = [300,600,1000,2000] 
    parameter_type = "Hotel Price"
    get_graph_by_paramter(df,parameter,parameter_list,parameter_type)
    return


# In[ ]:





# In[10]:








if __name__ == "__main__":
    df = pd.read_csv('./data/Hotels365Day.csv')
    df.sort_values('check_in', inplace=True)
    df2 = df.iloc[:, 1:].reset_index(drop=True)
    df2.drop(df2[df2['hotel_rating'] < 3].index, inplace = True)
    df2.drop(df2[df2['number_of_reviews'] < 10].index, inplace = True)
    print("----------Graph Info---------")
    print(df2.info())
    print('\n')
    print("----------Null Cells Check---------")
    print(df2.isna().sum())
    print('\n')
    print("----------Duplicated Check---------")
    print("There are "+str(df.duplicated().sum())+" duplicated rows")
    print('\n')
    df2 = add_date_coulmns(df2)
#     get_graph_for_stars_count(df2)
#     get_graph_for_distance_from_center(df2)
#     get_graph_for_hotel_rating(df2)
# #     get_graph_for_hotel_price(df2)
#     df2 = create_mean_on_graph(df2,1)
#     df2["hotel_price"].mean()
        


# In[17]:


def get_avg_price(df,hotel_name):
    if hotel_name == "all":
        df2 = df.groupby("month")["hotel_price"].mean()
    else:
        df2= df[df['hotel_name'] == hotel_name].groupby("month")["hotel_price"].mean()
     
    return df2
    


# In[18]:




def get_avg_available_rooms(df,hotel_name):
    if hotel_name == "all":
        df2 = df.groupby("month")["available_rooms"].mean()
    else:
        df2= df[df['hotel_name'] == hotel_name].groupby("month")["available_rooms"].mean()
     
    return df2
 


# In[25]:


def get_avg_price_vs_available_room_graph(df):
    
    avg_price_df = get_avg_price(df,'all')
    avg_avaialble_room_df=  get_avg_available_rooms(df,'all')
    
    fig = plt.figure()

    for frame in [avg_price_df, avg_avaialble_room_df]:
        plt.plot(frame['hotel_price'], frame['available_rooms'])

    plt.xlim(0,18000)
    plt.ylim(0,30)
    plt.show()
#     avg_price_df.plot(kind='line')
#     avg_avaialble_room_df.plot(kind='line')
#     plt.ylabel('Price')
#     plt.xlabel('Month')
#     plt.show()

## אני מסיקים שככל שמספרי החדרים נגמר ככה המחיר עולה ## 
## ובגלל שיש יותר ביקוש בחודשים החמים אז יש פחות חדרים ולכן המחיר עולה ## 
get_avg_price_vs_available_room_graph(df2)

