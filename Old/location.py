import string
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import urllib
from collections import Counter 

userloc='boston'
#seperate into 2 functions, run the first, if we get a return then we find
#distance and set a bool on whether or not they need travel/accomodation, 
#otherwise run the 2nd function that scrapes web.
#Part 1, finds Location of city if present in search term
citylist=['boston','london','paris','new york city','bangkok','dubai','tokyo']

term="Is Wimbledon in London or Paris?"

term_p1=term.lower() #make lowercase
term_p2=term_p1.translate(str.maketrans('', '', string.punctuation))
splitterm=term_p2.split()  #split into array
#print(splitterm)

def intersection(splitterm, citylist): 
    return list(set(splitterm) & set(citylist))

foundloc=intersection(splitterm,citylist)

if len(foundloc) ==0:
    print('No cities found, perform web search')
elif len(foundloc)==1:
    print('One City found, location match!')
    print(foundloc[0])
else:
    print('Multiple cities found, perform web search to verify')
    #Potentially remove all mentions of cities? Just keeping the event. NOTE
    print(foundloc)
    
 
#-----------------------------------------------------------------------
#Part 2, finds location of city by scraping google web results
