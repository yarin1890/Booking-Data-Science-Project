#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import pandas as pd
import datetime
import pdb
from threading import Thread
import time


# In[2]:


def get_distance_from_center(txt):
    if ("מ'" in txt):
        # https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python # 
        distance_from_center = float(re.findall("\d+",txt)[0])
        return distance_from_center/1000
    elif ("." in txt):
        distance_from_center = float(re.findall("\d+\.\d+", txt)[0])
        return  distance_from_center
    else:
        distance_from_center = float(re.findall("\d+",txt)[0])
        return  distance_from_center
     


# In[3]:


def get_hotels_info_from_page(hotels):
    for i in range(0,25):
        hotel = hotels[i]
        hotel_name,preferred_hotel,stars_count,distance_from_center,available_rooms,hotel_price,hotel_rating,number_of_reviews = get_hotel_data(hotel)
        hotel_name_list.append(hotel_name)
        available_rooms_list.append(available_rooms)
        hotel_price_list.append(hotel_price)
        hotel_rating_list.append(hotel_rating)
        preferred_hotel_list.append(preferred_hotel)
        number_of_reviews_list.append(number_of_reviews)
        distance_from_center_list.append(distance_from_center)
        stars_count_list.append(stars_count)
    return 


# In[ ]:





# In[4]:



def get_hotel_data(hotel):   
    hotel_name = hotel.find("div", {"class": "fcab3ed991"}).text
    
    try:
        preferred_hotel = (hotel.find("span", {"data-testid": "preferred-badge"})["data-testid"] == "preferred-badge")
        preferred_hotel = 1 
        
    except:
        preferred_hotel = 0

    stars_count = len(hotel.findAll("span", {"class": "b6dc9a9e69 adc357e4f1 fe621d6382"}))
    
    ## source : https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string ## 
    distance_from_center = get_distance_from_center(hotel.find("span", {"data-testid": "distance"}).text)

    try:
        hotel_price_txt = hotel.find("span", {"data-testid": "price-and-discounted-price"}).text            
        if (',' not in hotel_price_txt):     
            hotel_price = int(re.findall("\d+",hotel_price_txt)[0])
                   
        else:
            hotel_price = int(re.findall("\d+\,\d+",hotel_price_txt)[0].replace(",", ""))
                         
    except AttributeError:
        hotel_price = -1 

    try:
        available_rooms_txt = hotel.find("div", {"class": "cb1f9edcd4"}).text
        if ('אחד' in available_rooms_txt):
            available_rooms  = 1
        elif ( hotel_price == -1):
            available_rooms = 0 
        else:
            available_rooms  = int(re.findall("\d+",available_rooms_txt)[0])
                           
    except AttributeError:
        if (hotel_price == -1):
            available_rooms = -1
        else:
            available_rooms = 10

   
    
    
    if (hotel.find("div", {"class": "b5cd09854e d10a6220b4"}) is not None):
        if (hotel.find("div", {"class": "b5cd09854e d10a6220b4"}).text == '10'):
            hotel_rating = 10
        else:
            # https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python # 
            hotel_rating = float(re.findall("\d+\.\d+", hotel.find("div", {"class": "b5cd09854e d10a6220b4"}).text)[0])
    else:
        hotel_rating = 0 

    
    if (hotel.find("span", {"class": "e2f34d59b1"}) is not  None):
        new_hotel = 1
    else:
        new_hotel = 0

    if (hotel.find("div", {"class": "d8eab2cf7f c90c0a70d3 db63693c62"}) is not None):
        number_of_reviews_txt = hotel.find("div", {"class": "d8eab2cf7f c90c0a70d3 db63693c62"}).text
        if (',' not in number_of_reviews_txt): 
            number_of_reviews = int(re.findall("\d+",number_of_reviews_txt)[0])
        else:
            number_of_reviews = int(re.findall("\d+\,\d+",number_of_reviews_txt)[0].replace(",", ""))
    else:
        number_of_reviews = 0

   
        
    return hotel_name,preferred_hotel,stars_count,distance_from_center,available_rooms,hotel_price,hotel_rating,number_of_reviews,new_hotel
    


# In[5]:


def get_data_from_page(current_url,offset,checkin_date):
    ## https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit-a-k-a-and-generate-user-agent ##
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = current_url+"&offset="+str(offset)
    requests.get(url)
    response=requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content,'html.parser')
    hotels = soup.findAll("div", {"data-testid": "property-card"})
    

    for i in range(0,len(hotels)):
        hotel_name = [] 
        available_rooms = [] 
        hotel_price = [] 
        hotel_rating = []
        preferred_hotel = [] 
        number_of_reviews = [] 
        distance_from_center = [] 
        stars_count = []
        new_hotel = []
        hotel = hotels[i]
        hotel_name,preferred_hotel,stars_count,distance_from_center,available_rooms,hotel_price,hotel_rating,number_of_reviews,new_hotel = get_hotel_data(hotel)
        hotel_name_list.append(hotel_name)
        available_rooms_list.append(available_rooms)
        hotel_price_list.append(hotel_price)
        hotel_rating_list.append(hotel_rating)
        preferred_hotel_list.append(preferred_hotel)
        number_of_reviews_list.append(number_of_reviews)
        distance_from_center_list.append(distance_from_center)
        stars_count_list.append(stars_count)
        new_hotel_list.append(new_hotel)
        check_in_list.append(checkin_date)
        
      
    return hotels


# In[6]:


def get_data_by_date(current_url,checkin_date):
    offset = 0
    ## https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit-a-k-a-and-generate-user-agent ## 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = current_url+"&offset="+str(offset)
    requests.get(url)
    response=requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content,'html.parser')
    hotels = soup.findAll("div", {"data-testid": "property-card"})
    number_of_pages = soup.find('ol', {'class': 'a8b500abde'})
    num_of_last_page = number_of_pages.findChildren("li" , recursive=False)[-1].text
    
    
    
    url_pages_data_list = [] 
    
    for i in range(0,int(num_of_last_page)):
         
        url_pages_data_list.append([url,offset,checkin_date])
        offset = offset +25
        url = current_url+"&offset="+str(offset)
    
    threads = [] 
   
    for unit in url_pages_data_list:
        url,offset,checkin_date = unit
        
        thread = Thread(target=get_data_from_page, args=(url,offset,checkin_date))
        threads.append(thread)
        
        
    for thread in threads:
        thread.start()


    for thread in threads:
        thread.join()


    return 


# In[7]:





if __name__ == "__main__":
    check_in_list = []
    hotel_name_list = [] 
    available_rooms_list = [] 
    hotel_price_list = [] 
    hotel_rating_list = []
    preferred_hotel_list = [] 
    number_of_reviews_list = [] 
    distance_from_center_list = [] 
    stars_count_list = [] 
    new_hotel_list = []



    ## https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python ##
    now = datetime.date.today()
    next_year  = now + datetime.timedelta(days=2)

    # https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python ##

    daterange = pd.date_range(now, next_year)
    url_list = []
    for single_date in daterange:
        checkin_date = single_date.strftime("%Y-%m-%d")
        checkout_date =  str(single_date.date() +  datetime.timedelta(days=1))
        url  = 'https://www.booking.com/searchresults.he.html?ss=%D7%90%D7%99%D7%9C%D7%AA&ssne=%D7%90%D7%99%D7%9C%D7%AA&ssne_untouched=%D7%90%D7%99%D7%9C%D7%AA&efdco=1&label=gog235jc-1FCAEoggI46AdIDlgDaGqIAQGYAQ64ARfIAQzYAQHoAQH4AQKIAgGoAgO4AvTcsp0GwAIB0gIkMTQ1YzMwMTEtMjFjMS00NWRkLThkMGItYzEyYTk3MTM3OWJi2AIF4AIB&sid=0300b6aa5d7b69c879512d1732ad5fe2&aid=397594&lang=he&sb=1&src_elem=sb&src=searchresults&dest_id=-779626&dest_type=city&checkin='+checkin_date+'&checkout='+checkout_date+'&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&nflt=ht_id%3D204'
        url_list.append([url,checkin_date])

    threads = [] 

    for unit in url_list:
        url,checkin_date = unit
        thread = Thread(target=get_data_by_date, args=(url,checkin_date))
        threads.append(thread)



    for thread in threads:
        thread.start()


    for thread in threads:
        thread.join()


    df = pd.DataFrame({
            "check_in" : check_in_list,
            "hotel_name" : hotel_name_list, 
            "available_rooms" : available_rooms_list,
            "hotel_price" : hotel_price_list,
            "hotel_rating" : hotel_rating_list,
            "preferred_hotel" : preferred_hotel_list, 
            "number_of_reviews" : number_of_reviews_list,
            "distance_from_center" : distance_from_center_list, 
            "stars_count" : stars_count_list,
            "new_hotel" : new_hotel_list,
            })    

    print("crawling finish")
    
#     df.to_csv('./data/Hotels365Day.csv')
df


# In[ ]:





# In[ ]:





# In[ ]:




