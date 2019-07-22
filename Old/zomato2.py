#API KEY = 2179390cabf9a71c3b3835aeb0ddb9b5
import json
import requests
import string

#Part 1, identifying City ID number from city
query='boston' #query should come straight from first part


key = '2179390cabf9a71c3b3835aeb0ddb9b5'
url_id = "https://developers.zomato.com/api/v2.1/cities?q="+query


if __name__ == '__main__':
    r = requests.get(url_id, headers={'user-key': key})
    if r.ok:
        id_data = r.json()
        #print(data) 
    else:
        print('Failure')
        
#just parsing through to get to the ID we need
g=id_data['location_suggestions']
h=g[0]
id=h['id']
idreturn="The ID for "+query+" is: "+str(id)
print(idreturn)

#Now we have city id number
#Check if collections available for this city

url_col="https://developers.zomato.com/api/v2.1/collections?city_id="+str(id)

if __name__ == '__main__':
    r = requests.get(url_col, headers={'user-key': key})
    if r.ok:
        col_data = r.json()
        #print(col_data) 
    else:
        print('Failure')
        
if len(col_data) !=4: #checks if collections exist for that city
    #we're sending collections back
    g=col_data['collections'] # now a list of many different collection dictionaries
    print(len(g))
    for x in g:
        h=x['collection']
        print(h['title'],': ',h['description'])
        print(h['url'])
    
else:
    print('No Collections') 
    url_locdeets='https://developers.zomato.com/api/v2.1/location_details?entity_id='+str(id)+'&entity_type=city'
    #Must send something else back - establishment types
    if __name__ == '__main__':
        r = requests.get(url_locdeets, headers={'user-key': key})
        if r.ok:
            locdeets_data = r.json()
            #print(locdeets_data) 
            print(len(locdeets_data))
            i=locdeets_data['best_rated_restaurant']
            for x in i:
                h=x['restaurant']
                print(h['name'])
                print(h['url'])
                #adj_title=h['name']+": Best Rated food in "+query
        



