from geo_distance import calc_distance 
from skyscanner import airport_code, air_quotes
from zomato import zomato_finder
from loc_finder import search_web, chooser
from walmart import get_items
from tabulate import tabulate

#hyperparameters
user_loc='boston'
min_travel_distance=160 #if user is farther away than this, show travel and accomodation


#Call to loc_finder
print('Enter search request: ', end='') 
query=input() 
loc_query="what city is "+query+" located in"
ranked_cities=search_web(loc_query)
chosen_city=chooser(ranked_cities,2) #give it all cities dict and ratio cutoff (3x bigger than 2nd most common in this case)
print('The chosen city is: ',chosen_city)

#Call to geo_distance.py to find distance between user and event location
try:
    distance=calc_distance(user_loc,chosen_city) #distance between two cities
except:
    print('No likely cities found.')
    exit()
    
    
#Finds Applicable ad categories
if distance>=min_travel_distance: #user is 160+ km away (100+ miles), may need travel and accomodation
    needs_travel=True
    needs_hotel=True
    print('User is',distance,'km away from event location. Showing travel and accomodation ads.')
    


#Calls to each API
#SkyScanner API Call

#Need to find these automatically
countrycode_user='USA' 
countrycode_destination='USA' 
date='2019-09-01'

#air_code_user=airport_code(user_loc,countrycode_user)
#air_code_destination=airport_code('Delhi',countrycode_destination)
#quotes=air_quotes(air_code_user,air_code_destination,date)
#print(quotes)

#Booking.com API Call


#Walmart API Call
try:
    list_products=get_items('lolapalooza music festival')
    print('Product Ads from Walmart:')
    for x in range(0,len(list_products)):
        print(list_products[x])
    
except:
    print('No possible product ads found on Walmart.com')


#Zomato API Call
try:
    zomato_finder(chosen_city)
except:
    print('No possible restaurants found for that city')
    #check if a city collections would work.
    
#Eventbrite API Call


#Yelp API Call


#Print list of applicable ads