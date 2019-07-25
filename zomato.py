import string
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import urllib
from collections import Counter 
import string
import json

def zomato_finder(city):
    #Zomato API KEY = 2179390cabf9a71c3b3835aeb0ddb9b5
    #Limit 1000 Calls/day
    
    #Part 1, identifying City ID number from city
    key = '2179390cabf9a71c3b3835aeb0ddb9b5'
    url_id = "https://developers.zomato.com/api/v2.1/cities?q="+city

    #if __name__ == '__main__':
    r = requests.get(url_id, headers={'user-key': key})
    if r.ok:
        id_data = r.json()
            #print(data) 
    else:
        print('Failure')
    #else:
    #    print('Level one Failure')
       
    #just parsing through to get to the ID we need
    g=id_data['location_suggestions']
    h=g[0]
    id=h['id']
    idreturn="The Zomato ID number for "+city+" is: "+str(id)
    #print(idreturn)

    #Now we have city id number
    #Check if collections available for this city
    url_col="https://developers.zomato.com/api/v2.1/collections?city_id="+str(id)

#if __name__ == '__main__':
    r = requests.get(url_col, headers={'user-key': key})
    if r.ok:
        col_data = r.json()
        #print(col_data) 
    else:
        print('Failure ')
            
    if len(col_data) !=4: #checks if collections exist for that city
        #we're sending collections back
        g=col_data['collections'] # now a list of many different collection dictionaries
        print('There are',len(g),'possible Zomato ads for',city)
        for x in g:
            h=x['collection']
            print(h['title'],': ',h['description'])
            #The following section is to snip out an error in the URL on zomatos end
            temp=h['url']
            partone=temp.rfind('zomato.com/')
            first=temp.find('/',10)
            second=temp.find('/',23)
            tempone=temp[0:first+1]
            temptwo=temp[second:]
            newurl=tempone+city+temptwo
            print(newurl)
        
    else:
        print('No Collections for this city on Zomato') 
        url_locdeets='https://developers.zomato.com/api/v2.1/location_details?entity_id='+str(id)+'&entity_type=city'
        #Must send something else back - establishment types
        if __name__ == '__main__':
            r = requests.get(url_locdeets, headers={'user-key': key})
            if r.ok:
                locdeets_data = r.json()
                i=locdeets_data['best_rated_restaurant']
                for x in i:
                    h=x['restaurant']
                    print(h['name'])
                    print(h['url'])
                    #adj_title=h['name']+": Best Rated food in "+city
        else:
            print('No restaurants in this city listed on Zomato')
  
  
#zomato('london')