import string
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import urllib
from collections import Counter 
import string
import json

userloc='doha'
citylist=set()
with open('cities.json') as json_file:
    data=json.load(json_file)
    for p in data:
        citylist.add(p['name'])
    print('Succesfully loaded',len(cities),'cities')
   
query="where is wimbledon located. It's in london"
query=query.lower()
query=query.translate(str.maketrans('', '', string.punctuation))
query=query.split()
print(query)

jack=set(query).intersection(citylist)
print(jack)