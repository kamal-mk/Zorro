temp='https://www.zomato.com/boston/healthy-restaurants?utm_source=api_basic_user&utm_medium=api&utm_campaign=v2.1'
partone=temp.rfind('zomato.com/')
first=temp.find('/',10)
second=temp.find('/',23)
tempone=temp[0:first+1]
temptwo=temp[second:]
newurl=tempone+'doha'+temptwo
print(newurl)
