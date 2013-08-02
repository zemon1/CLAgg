#Jeff Haak
#Craigslist Scraper

import mechanize as mech
import lxml.html as lx
import urllib2, urlparse, sys

def getSites():
     sites = "http://www.craigslist.org/about/sites"
     data = urllib2.urlopen(sites)
     html = data.readlines()
     data.close()
     
     options = []

     pastEnd = False
     curState = ""
     stateCount = -1
     count = 1

     for line in html:
         line = line.strip()
         if "<h4>" in line or "<li>" in line:
             if "FORMAT" in line:
                 pastEnd = True
             if pastEnd == False:
                 if "<h4>" in line:
                     if not stateCount == -1:
                         options[stateCount][3] = count - 1 
                     count = 1
                     stateCount = stateCount + 1

                     state = line.split("<h4>")[1].split("</h4>")[0]
                     curState = state
                     options.append([stateCount, state, {}, -1])

                 if "<li>" in line:
                     info = ['', '']
                     info[1] = line.split('<li><a href="')[1].split('">')[0]
                     info[0] = line.split('">')[1].split('</a>')[0].title()
                     options[stateCount][2][count] = info
                     count = count + 1
         if pastEnd == True and options[stateCount][3] == -1:
             options[stateCount][3] = count - 1
    
     #for item in options:
     #    print item, "\n"
    


     return options

def prettyPrint(optionz):
     count = 1
     print optionz[0], "-", optionz[1]
     while count <= optionz[3]:
         print "\t", str(optionz[0]) + "-" + str(count), ":",  optionz[2][count][0]
         print "\t\t", optionz[2][count][1]
         count += 1

     

def printOptions(optionz):
     retry = True 
     us = 1
     while retry == True:
         try:
              us = raw_input("Just the US?(0-No / 1-Yes): ")
              us = int(us)
              
              if not us == 0 and not us == 1:
                  raise ValueError

              retry = False
         except ValueError:
              print "Bro, I said 1 or 0 it's not hard."
              retry = True

     if int(us) == 1:
          for option in optionz:
              if option[0] <= 50:
                  prettyPrint(option)
     else:
          for option in optionz:
               prettyPrint(option)

def getOptions(optionz):
     choices = []
     print "To choose options type all of the numbers you want.  When you are done type done."
     print "To pick a whole region type only the region's number."
     print "To pick a specfic area in a region type number-number."
     print "Example 1 for Massachusetts type 21<Enter>"
     print "Example 2 for Boston Massachusetts type 21-1<Enter>"

     done = False

     while not done:
         entered = raw_input("Type an option number or done:")
         if entered == "done" or entered == "Done" or entered == "DONE":
             done = True
         else:
             entered = entered.split("-")
             if len(entered) == 2:
                 #print entered[0]
                 #print entered[1]
                 
                 choices.append(optionz[int(entered[0])][2][int(entered[1])])
             elif len(entered) == 1:
                 count = 1
                 opMax = int(optionz[int(entered[0])][3])
                 option = optionz[int(entered[0])][2]
                 while count <= opMax: 
                     #print count
                     #print optionz[int(entered[0])][2][count][1]
                     choices.append(optionz[int(entered[0])][2][count])
                     count += 1
             else:
                 print "Don't mess with me, I don't need this right now... Do it right..."
    
     for ele in choices:
         print ele

     return choices

def aggregator(urlz, appends):
     result = []
     
     for item in urlz:
         
         for app in appends:
             result.append([item[1] + app, item[0]])         

     return result


def getResults(urlz):
     results = []
     for url in urlz:
         try:
             data = urllib2.urlopen(url[0])
             html = data.readlines()
             data.close()
             
             count = 0


             for line in html:
                 line = line.strip()
                 #try:
                 if '<h4 class="ban ' in line or '<p class="row"' in line:
                     line = line.split('<p class="row"')
                     for ele in line:
                         price = ""
                         if not 'craigslist.org' in ele:
                             ele = '<p class="row"' + ele
                             #print url[0]
                             count += 1
                             item = lx.fromstring(ele)

                             #Grabs the link to the ad
                             if len(item.cssselect('a')) > 2:
                                 #print lx.tostring(item.cssselect('a')[1])
                                 link = item.cssselect('a')[1].text
                                 linkToAd = url[0].split("/search")[0] + item.cssselect('a')[1].get('href')
                                 
                                 if not "low price" in item.cssselect('a')[1].text:
                                     #Grabs the price
                                     if len(item.cssselect('.price')) > 0:
                                         #print item.cssselect('.price')[0].text
                                         price = item.cssselect('.price')[0].text
                         
                                     results.append([url[1], url[0], linkToAd, link, price, 1])
                                 else:
                                     results.append([None, None, None, None, None, 0])

                             #print "\n" 
                                 

                 #except:
                 #    print "Well that happened..."
                 #    traceback.print_tb()
         except urllib2.URLError:
             print "Couldn't find that URL"

     return results

if __name__ == "__main__":
     allowedUrls = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    
     lists = []
     #lists.append("/search/mca?zoomToPosting=&query=ducati&srchType=A&minAsk=1000&maxAsk=7000")
     #lists.append("/search/mca?zoomToPosting=&query=triumph&srchType=A&minAsk=1000&maxAsk=7000")
     #lists.append("/search/mca?zoomToPosting=&query=norton&srchType=A&minAsk=1000&maxAsk=3000")
     #lists.append("/search/mca?zoomToPosting=&query=cbr&srchType=A&minAsk=1000&maxAsk=3000")
     #lists.append("/search/mca?zoomToPosting=&query=gxsr&srchType=A&minAsk=1000&maxAsk=3000")
     lists.append("/search/mca?zoomToPosting=&query=Kawasaki&srchType=A&minAsk=1000&maxAsk=5000")
    
     choices = getSites() 
     printOptions(choices)
     areas = getOptions(choices)
     theUrls = aggregator(areas, lists)
     theUrls.sort()
     
     results = getResults(theUrls)

     for ele in results:
         if ele[5] == 1:
             print ele[0]
             print ele[1]
             print ele[2]
             print ele[3]
             print ele[4]
             print "\n"


     


























