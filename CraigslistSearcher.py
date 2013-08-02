#
#Jeff Haak
#Craigslist Scraper

import urllib
import copy
import re

#Builds the Urls to be scraped
def scraper(urlz, optionz, keywordz = []):
    results = []
    completeUrls = []

    #For every url in the list
    for url in urlz:
        if(keywordz != []):
            for word in keywordz:
                newUrl = copy.copy(url)
                newUrl += "query=" + word + "&"
                for item in optionz:
                    if(item == "minPrice" and optionz[item] != None):
                        newUrl += "minAsk=" + str(optionz[item]) + "&"
                        
                    if(item == "maxPrice" and optionz[item] != None):
                        newUrl += "maxAsk=" + str(optionz[item]) + "&"
                        
                    if(item == "image" and optionz[item] != 0):
                        newUrl += "hasPic=" + str(optionz[item]) + "&"
                        
                    if(item == "search"):
                        if(optionz[item] == 1):
                            opt = "A"
                        else:
                            opt = "T"
                        newUrl += "srchType=" + opt + "&"
                results.append(newUrl)
                
        else:
            newUrl = copy.copy(url)
            for item in optionz:
                if(item == "minPrice" and optionz[item] != None):
                    newUrl += "minAsk=" + str(optionz[item]) + "&"
                    
                if(item == "maxPrice" and optionz[item] != None):
                    newUrl += "maxAsk=" + str(optionz[item]) + "&"
                    
                if(item == "image" and optionz[item] != 0):
                    newUrl += "hasPic=" + str(optionz[item]) + "&"
                    
                if(item == "search"):
                    if(optionz[item] == 1):
                        opt = "A"
                    else:
                        opt = "T"
                    newUrl += "srchType=" + opt + "&"
            results.append(newUrl)
                
    return results

#Scrapes the contents of a list of provided urls
def gatherer(urlz):


    i = 0
    for url in urlz:
        data = urllib.urlopen(url)
        html = data.readlines()
        data.close()

        again = False
        
        for line in html:
            
            rowStart = re.compile('<p class="row">')
            rowEnd = re.compile('</p>')
            spanFinder = re.compile('<span class="ih" id=')
             
            if again != True:
                if rowStart.search(line):
                    #print "FIRST", line
                    i += 1
                    print i, "-------------------------------------"
                    again = True
            else:
                if not spanFinder.search(line) and not rowEnd.search(line):
                    print "LAST", line
                    line = line.strip()
                    lineContents = line.split('<a href="')
                    print lineContents
                    
                
                if rowEnd.search(line):
                    print "-------------------------------------\n"
                    again = False





                    
def main():
    urls = ["http://charleston.craigslist.org/search/cta?", "http://columbia.craigslist.org/search/cta?"]
    options = dict(minPrice = 50, maxPrice = 1000, image = 1, search = 1)
    words = ["Red", "red Camaro", "hate"]

    print options
    print urls

    for item in options:
        print item + ":", options[item]
        
    results = scraper(urls, options, words)

    gatherer(results)


  

main()
