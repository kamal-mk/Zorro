#part 2 will be here until i move it back
import string
from bs4 import BeautifulSoup
import requests

citylist=['boston','london','paris','new york city','bangkok','dubai','tokyo']

term='tickets to wimbledon' 
googleterm='where is '+term

searchurl='https://www.google.com/search?q='+googleterm
response=requests.get(searchurl)
print(response.text)
soup = BeautifulSoup(response.text,"lxml")
#texters=soup.get_text()
for item in soup.select(".r a"):
    print (item.text)
    break