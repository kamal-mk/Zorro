import urllib.request
import json

#Retreive airport code from city to give it airport code
def airport_code(city,country):
    req_code=urllib.request.Request("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/"+country+"/USD/en-GB/?query="+city,
    headers={"X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com","X-RapidAPI-Key": "c8a84e947dmshd7a39c902a53de1p1dcb2bjsn70903089000f"})
    with urllib.request.urlopen(req_code) as response:
        the_page = response.read()
    decoded_data=json.loads(the_page)
    found_code=decoded_data["Places"][0]['PlaceId']
    return found_code


#retreive lowest quote for flights between two cities on a specified date
def air_quotes(origin_code,dest_code,date):
    req = urllib.request.Request("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/"+origin_code+"/"+dest_code+"/"+date+"?inboundpartialdate=2019-12-01",
    headers={"X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com","X-RapidAPI-Key": "c8a84e947dmshd7a39c902a53de1p1dcb2bjsn70903089000f"})

    with urllib.request.urlopen(req) as response:
       the_page = response.read()
    decoded_data=json.loads(the_page)
    min_price=decoded_data["Quotes"][0]['MinPrice']
    direct_flight=decoded_data["Quotes"][0]['Direct'] #returns boolean if flights is direct
    return min_price,direct_flight

