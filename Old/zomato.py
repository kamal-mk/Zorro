import importlib
import unirest
#later on, import the query, for now i'll assume i know items
location='london'
response = unirest.post("https://ZomatoraygorodskijV1.p.rapidapi.com/getCities",
  headers={
    "X-RapidAPI-Host": "ZomatoraygorodskijV1.p.rapidapi.com",
    "X-RapidAPI-Key": "c8a84e947dmshd7a39c902a53de1p1dcb2bjsn70903089000f",
    "Content-Type": "application/x-www-form-urlencoded"
  }
)