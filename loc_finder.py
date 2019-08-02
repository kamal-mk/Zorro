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
citydata={}
with open("expanded_citylist.json",encoding='utf-8', errors='ignore') as json_data:
    data = json.load(json_data, strict=False)
    for p in data:
        temp_city=(p['cityLabel']).lower()
        temp_country=(p['countryLabel']).lower()
        temp_pop=(p['population'])
        citylist.add(temp_city)
        countrylist.add(temp_country)
        citydata[temp_city]={'country':temp_country,'population':temp_pop}
    print('Succesfully loaded',len(citydata),'cities')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

#Part 2, finds location of city by scraping google web results
def search_web(new_query):
    #print('Google search query is:',new_query)
    new_query = urllib.parse.quote_plus(new_query) # Format into URL encoding if there are spaces
    number_result = 100 #number of google results to parse
    ua = UserAgent()
    google_url = "https://www.google.com/search?q=" + new_query + "&num=" + str(number_result)
    #response = requests.get(google_url, {"User-Agent": ua.random})
    response = requests.get(google_url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    #print(soup)
    soop=str(soup)
    #print(soop)
    check_block=soop.find('This page appears when Google automatically detects requests')
    #print(check_block)
    if check_block!=-1:
        print('Google has blocked this request')
        exit()
    result_div = soup.find_all('div', attrs = {'class': 'g'})
    #print('Google URL to go to',google_url)
    titles = []
    descriptions = set()
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            title = r.find('div', attrs={'class':'r'}).get_text()
            description = r.find('div', attrs={'class':'s'}).get_text()
            # Check to make sure everything is present before appending
            if title != '' and description != '': 
                titles.append(title)
                descriptions.add(description)
      
        # Next loop if one element is not present
        except:
            #couldn't find those classes for that result. Not a readable google result
            continue
    alltext=' '.join(descriptions) #all descriptions joined
    #print('Alltext',alltext) #string
    
    #GEOTEXT PART
    ranked_cities={}
    lower_cities=[]
    places = GeoText(alltext) #extracts cities using GeoText package
    for p in places.cities:  #makes lowercase
        lower_cities.append(p.lower()) 
        #print('Geotext city',p)
    alltext_p1=alltext.lower() #make lowercase
    alltext_p2=alltext_p1.translate(str.maketrans('', '', string.punctuation)) #remove punctuation
    all_split=alltext_p2.split()  #split into list
    all_cities=all_split+lower_cities
    citymatches=(set(all_cities) & set(citydata))
    #print('type is',type(all_split))
    #countrymatches=(set(all_split) & countrylist)
    #print('City matches',citymatches)
    for y in citymatches:
        ranked_cities.update({y:all_cities.count(y)})
    #print(ranked_cities)
    #for y in countrymatches:
    #    ranked_countries.update({y:all_split.count(y)})
    return ranked_cities,alltext, citydata
    
def chooser(ranked_cities,ratio_cutoff,alltext):    
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
    print('Highest val city:',max_keys)
    if len(max_keys)==1:
        print(max_keys[0])
        #compare to list of cities
        
        #print(new_dict)
        #print(new_dict)
        #delete initial entry
        #Add in new scores, subtract totalcount from main player
        print(max_keys[0],"is ",round(ratio,1),"x more common than second largest city")
        if ratio>ratio_cutoff: #if ratio is high enough, we found our city
            return max_keys[0]
def possible_alternatives(query,ranked_cities,alltext,citydata):
    #PUT IN ERROR CATCHING IN CASE OF LESS THAN 4 OPTIONS
    
    print('Ranked Cities',ranked_cities)
    temp_cities=dict(ranked_cities)
    #temp_cities=dict(ranked
    ranked_5=[]
    num_it=5
    if len(temp_cities)<5:
        num_it=len(temp_cities)
    for x in range(0,num_it):
        j=max(temp_cities, key=temp_cities.get)
        temp_cities.pop(j)
        ranked_5.append(j)
    
    #print('Top 5 cities:',ranked_5)   

    possible=[] 
    alltext=alltext.lower()
    new_dict={}
    error_dict={}
    
    for x in citylist:
        for y in ranked_5:
            if y in x:
                if y==x:
                    continue
                #print('Scanning google text for',x)
                temp=alltext.count(x)
                #print(temp,'results found')
               # print('------------')                
                if temp==0:
                    continue
                error_dict[x]=temp
                new_dict[x]=temp
                ranked_cities[y]=ranked_cities[y]-temp
                
    #scan for mentions of country
    for x in ranked_5:
        temp_country=citydata[x]['country']
        country_mentions=alltext.count(temp_country)
        ranked_cities[x]=ranked_cities[x]+(0.5*country_mentions)
    
    print('----------------------------')
    #print('New Dictionary: ',new_dict)
    #print('error dict',error_dict)
    #add to new values, subtract old ones
    #ranked_cities[ranked_5[0]]=ranked_cities[ranked_5[0]]-totalcount
    
    #add in new cities that were picked up to the dict
    for z in new_dict:
        if z in ranked_cities:
            ranked_cities[z]=ranked_cities[z]+new_dict[z]
        else:
            if new_dict[z]==0:
                continue
            ranked_cities[z]=new_dict[z]
    
    #print('Final order of ranked cities',ranked_cities)
    final_guess=max(ranked_cities, key=ranked_cities.get)
    
    temp_2=dict(ranked_cities)
    new_ranked_5=[]
    for x in range(0,num_it):
        j=max(temp_2, key=temp_2.get)
        temp_2.pop(j)
        new_ranked_5.append(j)
    #print('NEW Top 5 cities:',new_ranked_5) 
    
    #NAME AND POPUALTION CHECKING
    temp_pop=[]
    pop_flag=0
    for x in new_ranked_5:
        temp_pop.append(citydata[x]['population'])
    max_pop=max(temp_pop)
    #print(max_pop)
    final_pop=citydata[final_guess]['population']
    #print(final_pop)
    #FIX THIS: NOT WORKING WELL
    if max_pop>(5*final_pop):
        pop_flag=1
        print('Potential small city misattribution, penalizing 50%')
        ranked_cities[final_guess]=ranked_cities[final_guess]*0.5
        
    name_flag=0
    if final_guess in query:
        name_flag=1
        print('potential query name misattribution, penalizing 50%')
        #SEARCH WEB FOR 
        #search_web(
        ranked_cities[final_guess]=ranked_cities[final_guess]*0.5
    #print('Updated Ranked cities',ranked_cities)
    final_guess=max(ranked_cities, key=ranked_cities.get)
    print('----------------------------')

    print('Ranked Cities after adjustments',ranked_cities)
   
    #final_guess=max(ranked_cities, key=ranked_cities.get)

    #Put this search term flag logic into place
    
    rank_sort=sorted(ranked_cities.values())
      
    ratio=rank_sort[-1]/rank_sort[-2] #finds ratio of two highest
    ratio_cutoff=1.5
    print('----------------------------')
    print(final_guess,"is ",round(ratio,1),"x more common than 2nd largest city")
    #if ratio>ratio_cutoff: #if ratio is high enough, we found our city
    print('Final guess: ',final_guess)
    return final_guess

#----------------------------------------------------------------------

query='statue of liberty'
fmtd_query='what city is'+query+'located in'
a=search_web(fmtd_query)
b=possible_alternatives(query,a[0],a[1],a[2])

