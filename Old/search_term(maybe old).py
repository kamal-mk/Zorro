  
###################################################################    
#Part 1, searches actual term for city name
#Part 1, finds Location of city if present in search term
#citylist=['delhi','boston','london','paris','new york city','bangkok','dubai','tokyo','mumbai','rio de janeiro','doha']

def search_term(query):
    term_p1=query.lower() #make lowercase
    term_p2=term_p1.translate(str.maketrans('', '', string.punctuation))
    splitterm=term_p2.split()  #split into array
    
    def intersection(splitterm, citylist): 
        return list(set(splitterm) & set(citylist))
    
    foundloc=intersection(splitterm,citylist)

    if len(foundloc) ==0:
        print('No cities found, performing web search')
        prob_city=search_web(query)
    elif len(foundloc)==1:
        print('One City found, location is:',foundloc[0])
        prob_city=foundloc[0]
    else:
        print('Multiple cities found, performing web search to verify')
        #Potentially remove all mentions of cities? Just keeping the event. NOTE
        #print(foundloc)
        prob_city=search_web(query)
        
    return prob_city
