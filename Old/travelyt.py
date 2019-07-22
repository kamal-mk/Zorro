from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

userloc='boston'
foundloc=['tokyo']
query="distance from "+userloc+" to "+foundloc[0] +" in km"
my_url = "https://www.google.com/search?q=" + query
