from loc_finder import search_web, possible_alternatives
import string
eventlist={'outside lands':'san francisco','lollapalooza':'chicago',\
'statue of liberty':'new york city','world cup 2022':'doha',\
'rio carnival':'rio de janeiro','Mardi gras':'new orleans',\
'MaerzMusik':'Berlin','the louvre':'paris','oktoberfest 2020':'munich',\
'disneyland':'anaheim','leaning tower of pisa':'pisa','coachella':'indio'\
}

print(len(eventlist),'events to be tested:')
count=0

for event in eventlist:
    print('Search term:',event)
    fmtd_query='what city is'+event+'located in'
    a=search_web(fmtd_query)
    b=possible_alternatives(event,a[0],a[1],a[2])
    print('-----------------')
    print('Correct Answer:',eventlist[event])
    print(b)
    b=b.strip()
    if b==eventlist[event].lower():
        print('Location correct!')
        count=count+1
    else:
        print('Failed to identify correctly')
    print('****************************************************')
    print('****************************************************')
acc=round((count/len(eventlist))*100)
print('Total Accuracy:',acc,'%')