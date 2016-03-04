#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:33:51 2016

@author: prassanna
"""

import requests
import argparse
from colorama import Fore, Back, Style
#from __future__ import print_function
import sys
import random

def find_happiest_article(results):
    happyresults = happy_articles(results)
    if(len(happyresults)==1):
        idx=0
    elif(len(happyresults)==0):
        bla = dict()
        bla['title']= "Can't find anything positive"
        bla['url'] = "http://127.0.0.1"
        return bla            
    else:
        idx=random.randint(0,len(happyresults)-1)
        
    return happyresults[idx]['source']['enriched']['url']

def find_saddest_article(results):
    sadresults = sad_articles(results)  
    if(len(sadresults)==1):
        idx=0
    elif(len(sadresults)==0):
        bla = dict()
        bla['title']= "Can't find anything negative"
        bla['url'] = "http://127.0.0.1"
        return bla
    else:
        idx=random.randint(0,len(sadresults)-1)
    return sadresults[idx]['source']['enriched']['url']
    
def happy_articles(results):
    articles =[]
    for result in results:
        if(result['source']['enriched']['url']['docSentiment']['score']>=0):
            articles.append(result)
    return articles

def sad_articles(results):
    articles =[]
    for result in results:
        if(result['source']['enriched']['url']['docSentiment']['score']<=0):
            articles.append(result)
    return articles        

parser = argparse.ArgumentParser(description='Happy News')
parser.add_argument('--keyword',  type=str, nargs='?', help='keyword to search',default="Google")
parser.add_argument('--sad', const=find_saddest_article, default=find_happiest_article, nargs='?')
#url = 'http://gateway-a.watsonplatform.net/calls/data/GetNews?apikey=2aa9eb057b743ba8eb9f9be88ce140ea82521844&outputMode=json&start=now-1d&end=now&count=100&q.enriched.url.enrichedTitle.relations.relation=|action.verb.text=acquire,object.entities.entity.type=Company|&return=enriched.url'
args = parser.parse_args()
keyword = args.keyword

#sys.exit()

API_KEY = open('API-KEY','r').readline().replace('\n','')
if(sys.version_info<= (3,0)):
    url = 'http://gateway-a.watsonplatform.net/calls/data/GetNews?outputMode=json&start=now-30d&end=now&count=5&q.enriched.url.enrichedTitle.keywords.keyword.text='+keyword+'&return=enriched.url.url,enriched.url.title,enriched.url.docSentiment&apikey='+API_KEY
else:
    url = 'https://gateway-a.watsonplatform.net/calls/data/GetNews?outputMode=json&start=now-30d&end=now&count=5&q.enriched.url.enrichedTitle.keywords.keyword.text='+keyword+'&return=enriched.url.url,enriched.url.title,enriched.url.docSentiment&apikey='+API_KEY    
response = requests.get(url)
data = response.json()
ok_flag = str(data['result']['status']) == 'OK'
results  =data['result']['docs']



best_result = args.sad(results)

title = str(best_result['title'])
link = str(best_result['url'])
print (Fore.RED, title)
print (Fore.BLUE, link)
print (Fore.RESET, "")
#sentiments = best_result['docSentiment']
#sentiment_score = sentiments['score']
#sentiment_positive = str(sentiments['type']) == 'positive'
