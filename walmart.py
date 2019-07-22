import urllib.request
import json
#username=zorro-project
#5 Calls/Second up to 5000 calls per day
#figure out how to limit number of responses
def get_items(query):
    new_query = urllib.parse.quote_plus(query)
    api_key='jehfzh4v7ybpgmg4cx6zxsa7'
    req_code=urllib.request.Request("http://api.walmartlabs.com/v1/search?query="+new_query+"&format=json&apiKey="+api_key)

    with urllib.request.urlopen(req_code) as response:
        the_page = response.read()
    decoded_data=json.loads(the_page)
    items=[]
    for p in decoded_data['items']:
        items.append(p['name'])
    return items
    
print(get_items("ipad"))
#add price and other functionality. eventually want to be pulling pictures etc
        