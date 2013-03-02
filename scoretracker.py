#!/usr/bin/python
"""A dirty hack to fetch scores from Barcelona matches and notify on a new goal
Will work on all Unix flavored systems with libnotify (available by default in all linux flavors)"""
from BeautifulSoup import BeautifulSoup
import requests
import time
import os
import sys
score = ('0','0')
local = ['']
visitor = ['']
while True:
    page = requests.get('http://www.fcbarcelona.com/')
    soup = BeautifulSoup(page.content, convertEntities=BeautifulSoup.HTML_ENTITIES).find("div",\
        attrs={'class':"match-stats"})
    refreshedscore = (soup.find("span",attrs={'class':"score-box js-data-bind-gameSummary15965-result_local"}).text, \
        soup.find("span",attrs={'class':"score-box js-data-bind-gameSummary15965-result_visitor"}).text)
    
    if refreshedscore != score:
        score = refreshedscore
        scoreboard = soup.findAll('span')
        local[0] = scoreboard[0].text
        for element in scoreboard:
            if element.attrMap != None and element.has_key('class') and \
              element.attrMap['class'] == 'score-box js-data-bind-gameSummary15965-result_visitor':
                refreshedlocal = scoreboard[:scoreboard.index(element)]
                refreshedvisitor = scoreboard[scoreboard.index(element):]
                visitor[0] = scoreboard[scoreboard.index(element)+1].text
        
        for element in xrange(0,len(refreshedlocal)):
            if refreshedlocal[element].attrMap.get('class', None) == 'minute':
                scorer = (refreshedlocal[element].text, refreshedlocal[element+1].text)
                if scorer not in local:
                    local.append(scorer)
                    string = 'notify-send '+' \"Goal by '+scorer[1]+' at '+scorer[0]+'\" '+\
                        '\"Score: '+local[0]+' - '+score[0]+' : '+visitor[0]+' - '+score[1]+'\"' \
                        ' --icon=dialog-information'
                    os.system(string)
        
        for element in xrange(0,len(refreshedvisitor)):
            if (refreshedvisitor[element].attrMap != None and \
                refreshedvisitor[element].attrMap.get('class', None) == 'minute') or \
              refreshedvisitor[element].text.find("'") != -1:
                scorer = (refreshedvisitor[element].text, refreshedvisitor[element+1].text)
                if scorer not in visitor:
                    visitor.append(scorer)
                    string = 'notify-send '+' \"Goal by '+scorer[1]+' at '+scorer[0]+'\" '+\
                        '\"Score: '+local[0]+' - '+score[0]+' : '+visitor[0]+' - '+score[1]+'\"' \
                        ' --icon=dialog-information'
                    os.system(string)
    
    if soup.find('p', attrs={'class':"date-time phase js-data-bind-gameSummary15965-status"}).text.find('Finished') != 1:
        string = 'notify-send '+ '\'Game Finished\' '+\
            '\"Final Score: '+local[0]+' - '+score[0]+' : '+visitor[0]+' - '+score[1]+'\"' \
            ' --icon=dialog-information'
        os.system(string)
        break

    time.sleep(60)