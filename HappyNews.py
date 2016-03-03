#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:33:51 2016

@author: prassanna
"""

import requests
import argparse

def find_happiest_article(results):
    maxV = 0
    maxI = 0
    for result in results:
        sentiment_score = result['source']['enriched']['url']['docSentiment']['score']
        if(maxV<sentiment_score):
            maxV = sentiment_score
            maxI = results.index(result)            
    return results[maxI]['source']['enriched']['url']

def find_saddest_article(results):
    minV = 10
    minI = 0
    for result in results:
        sentiment_score = result['source']['enriched']['url']['docSentiment']['score']
        if(minV>sentiment_score):
            minV= sentiment_score
            minI = results.index(result)            
    return results[minI]['source']['enriched']['url']

parser = argparse.ArgumentParser(description='Happy News')
parser.add_argument('Keyword',  type=str, nargs='?', help='keyword to search',default="Google")
parser.add_argument('--sad', const=find_saddest_article, default=find_happiest_article, nargs='?')
#url = 'http://gateway-a.watsonplatform.net/calls/data/GetNews?apikey=2aa9eb057b743ba8eb9f9be88ce140ea82521844&outputMode=json&start=now-1d&end=now&count=100&q.enriched.url.enrichedTitle.relations.relation=|action.verb.text=acquire,object.entities.entity.type=Company|&return=enriched.url'
args = parser.parse_args()
keyword = args.Keyword

#sys.exit()

API_KEY = open('API-KEY','r').readline().replace('\n','')
url = 'https://gateway-a.watsonplatform.net/calls/data/GetNews?outputMode=json&start=now-30d&end=now&count=5&q.enriched.url.enrichedTitle.keywords.keyword.text='+keyword+'&return=enriched.url.url,enriched.url.title,enriched.url.docSentiment&apikey='+API_KEY
response = requests.get(url)
data = response.json()
ok_flag = str(data['result']['status']) == 'OK'
results  =data['result']['docs']





best_result = args.sad(results)

title = str(best_result['title'])
link = str(best_result['url'])
print (title)
print (link)
#sentiments = best_result['docSentiment']
#sentiment_score = sentiments['score']
#sentiment_positive = str(sentiments['type']) == 'positive'
