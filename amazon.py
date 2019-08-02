import string
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import urllib
from collections import Counter 
import csv
import time
import random

query="nike"

    
    
results=[]
#Part 1, search the term on amazon and get all the links, price, title
error_count=0
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

def collect_links(new_query):
    new_query = urllib.parse.quote_plus(new_query) # Format into URL encoding if there are spaces
    amazon_url = "https://www.amazon.com/s?k="+new_query
    ua = UserAgent()
    #IMPLEMENT ROBOT DETECTION CHECK
    
    #response = requests.get(amazon_url, {"User-Agent": ua.random})
    response = requests.get(amazon_url, headers=headers)
    soup = BeautifulSoup(response.text,"lxml")
    #print(soup)
    link_result= soup.find_all('div', attrs = {'class':'a-section a-spacing-none'}) #entire webpage of search term found
    price_result=soup.find_all('div',attrs={'class':'a-row'})
    print(price_result)
    #print(result)
    q=str(result) #stringify results
    num_results=q.count('<a class="a-link-normal a-text-normal" href="')
    num_results_print=num_results
    if num_results_print ==0:
        print('Failed to collect any results. May be blocked. Waiting 5 mins')
        return 'blocked'
        #exit()
    print('Number of results found for',new_query,':',num_results)
    count=0
    term_array=[]
    while num_results>0:
        start=q.find('<a class="a-link-normal a-text-normal" href="',count) #search for beginning of link
        temp_link=q[start+45:start+200] #cuts 150 characters out
        end_quote=temp_link.find('"')
        end_ref=temp_link.find('/ref')
        #print(end_quote,end_ref)
        if end_quote == -1 :
            cleaned_link=temp_link[0:end_ref]
        elif end_ref == -1:
            cleaned_link=temp_link[0:end_quote]
        elif end_quote>end_ref:
            cleaned_link=temp_link[0:end_ref]
        elif end_ref>end_quote:
            cleaned_link=temp_link[0:end_quote]           
        #print(cleaned_link)
        count=start+1
        #verifying that this is actually a link
        ver=cleaned_link.find('/dp/')
        if ver==-1:
            num_results_print=num_results_print-1
            continue
        term_array.append(cleaned_link)
        num_results=num_results-1
    
    print('Successfully collected',num_results_print,'links.')
    return term_array


links=collect_links(query)
print(links)