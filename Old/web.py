import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib
import string
from collections import Counter 

print('Enter search request: ', end='') 
query=input()
query = urllib.parse.quote_plus(query) # Format into URL encoding
number_result = 20 #number of google results to parse
ua = UserAgent()
google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
response = requests.get(google_url, {"User-Agent": ua.random})
soup = BeautifulSoup(response.text, "html.parser")

result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

titles = []
descriptions = []
for r in result_div:
    # Checks if each element is present, else, raise exception
    try:
        title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
        description = r.find('div', attrs={'class':'s3v9rd'}).get_text()
        
        # Check to make sure everything is present before appending
        if title != '' and description != '': 
            titles.append(title)
            descriptions.append(description)
    # Next loop if one element is not present
    except:
        continue
alltext=' '.join(descriptions)
#print(descriptions)
alltext_p1=alltext.lower() #make lowercase
alltext_p2=alltext_p1.translate(str.maketrans('', '', string.punctuation))
all_split=alltext_p2.split()  #split into array
#print(all_split)

result = [item for items, c in Counter(all_split).most_common() 
                                      for item in [items] * c] 

#print(result)
citylist=['boston','london','paris','new york city','bangkok','dubai','tokyo']

def intersection(result, citylist): 
    return list(set(result) & set(citylist))


foundloc=intersection(result,citylist)
print(foundloc[0]) #prints the most common found city