import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib
import string
from collections import Counter 

#Assume users location is in Boston
userloc='boston'
foundloc=['tokyo']
#First, identify if user is more than 100 km away. If so, reccomend hotels and flights.
#takes result of web.py, then finds distance between those two cities

ua = UserAgent()
query="distance from "+userloc+" to "+foundloc[0] +" in km"
google_url = "https://www.google.com/search?q=" + query
response = requests.get(google_url, {"User-Agent": ua.random})
soup = BeautifulSoup(response.text, "html.parser")

result_div = soup.find_all('div', attrs = {'class': 'dDoNo vk_bk'})
print(result_div)