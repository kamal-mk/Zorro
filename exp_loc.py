# TO DO:
#1. Import new list with Country code for Skyscanner purposes
#2. New processing of cities into dictionary format
#3. Include in the function a country thing as well. How to deal with abbreviations?
#4. Run multiple searches with different variations of query's. "what city is ____ located in"
#5. Can split functions into additional functions so I can run queries without needing lots of duplicate code.

import string
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import urllib
from collections import Counter 
import string
import json
from geotext import GeoText



citylist=set()
countrylist=set()
with open("expanded_citylist.json",encoding='utf-8', errors='ignore') as json_data:
    data = json.load(json_data, strict=False)
    for p in data:
        temp_city=(p['cityLabel']).lower()
        temp_country=(p['countryLabel']).lower()
        citylist.add(temp_city)
        countrylist.add(temp_country)
    print('Succesfully loaded',len(citylist),'cities', 'and ', len(countrylist), 'countries')

#Part 2, finds location of city by scraping google web results
def search_web(new_query):
    #print('Google search query is:',new_query)
    new_query = urllib.parse.quote_plus(new_query) # Format into URL encoding if there are spaces
    number_result = 100 #number of google results to parse
    ua = UserAgent()
    google_url = "https://www.google.com/search?q=" + new_query + "&num=" + str(number_result)
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})
   
    titles = []
    descriptions = set()
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
            description = r.find('div', attrs={'class':'s3v9rd'}).get_text()
            
            # Check to make sure everything is present before appending
            if title != '' and description != '': 
                titles.append(title)
                descriptions.add(description)
        # Next loop if one element is not present
        except:
            continue
    alltext=' '.join(descriptions) #all descriptions joined
    #print(alltext)
    
    #GEOTEXT PART
    ranked_cities={}
    lower_cities=[]
    places = GeoText(alltext) #extracts cities using GeoText package
    for p in places.cities:  #makes lowercase
        lower_cities.append(p.lower()) 
    
    alltext_p1=alltext.lower() #make lowercase
    alltext_p2=alltext_p1.translate(str.maketrans('', '', string.punctuation)) #remove punctuation
    all_split=alltext_p2.split()  #split into list
    all_cities=all_split+lower_cities
    citymatches=(set(all_cities) & citylist)
    #print('type is',type(all_split))
    #countrymatches=(set(all_split) & countrylist)
    #print(citymatches)
    for y in citymatches:
        ranked_cities.update({y:all_cities.count(y)})
    #print(ranked_cities)
    #for y in countrymatches:
    #    ranked_countries.update({y:all_split.count(y)})
    return ranked_cities
    
def chooser(ranked_cities,ratio_cutoff):    
    rank_sort=sorted(ranked_cities.values())
    ratio=rank_sort[-1]/rank_sort[-2] #finds ratio of two highest
    
    max_val=0
    max_keys=[]
    for k, v in ranked_cities.items():
        if v >= max_val:
            if v> max_val:
                max_val=v
                max_keys=[k]
            else:
                max_keys.append(k)
    if len(max_keys)==1:
        print(max_keys[0],"is ",round(ratio,1),"x more common than second largest city")
        if ratio>ratio_cutoff: #if ratio is high enough, we found our city
            return max_keys[0]
        

#Finds distance between cities using Google's map feature. More accurate but breaks often     
#def distance_cities(city1,city2):
#    newquery='distance from '+city1+' to '+city2
#    new_query = urllib.parse.quote_plus(newquery) # Format into URL encoding if there are spaces
#    ua = UserAgent()
#    google_url = "https://www.google.com/search?q=" + new_query + "&num=1"
#    response = requests.get(google_url, {"User-Agent": ua.random})
#    soup = BeautifulSoup(response.text, "html.parser")
#    result_div = soup.find_all('div')
#    print(result_div)
  


