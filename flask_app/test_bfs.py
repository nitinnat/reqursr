# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 21:28:07 2018

@author: Nitin
"""
from bs4 import BeautifulSoup
import requests
import json
from collections import defaultdict
import os

base_link = "https://en.wikipedia.org"
link = "/wiki/Computer_vision"
wiki_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=opensearch&search="
wiki_title_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="
def google_nlp(text):
    base = "https://language.googleapis.com"
    doc = {"type": "PLAIN_TEXT", "content": text}
    request_data = {"document": doc, "encodingType": "UTF8"}
    
    entities_endpoint = "/v1/documents:analyzeEntities"
    entities_url = base + entities_endpoint + "?key=AIzaSyAGy5__54Qd0u5wEUC5uOIFCVBYc1hleQc"
    
    response = requests.post(entities_url, data=json.dumps(request_data))
    entities = json.loads(response.text)
    return [entities["entities"][i]['name'] for i in range(len(entities["entities"])) if 
          entities["entities"][i]['type'] == 'OTHER']
def scrape_extract(title):
    my_bytes_value = requests.get(wiki_api_link + title).content
    return scrape_wiki_link(json.loads(my_bytes_value)[3][0])

def get_first_link(query):
    return json.loads(requests.get(wiki_api_link + query).content)

def scrape_wiki_link(link):
    temppage = requests.get(link)
    tempsoup = BeautifulSoup(temppage.content, 'html.parser')
    
    #print(tempsoup.get_text())
    p =  tempsoup.find_all('p')
    title = tempsoup.find_all('title')
    text = ''
    
    for wrapper in p[0:3]:
        
        """
        children = wrapper.find_all('a')        
        for c in children:
            if ((not "#cite_note" in c['href']) and
                 (not "Wikipedia:Citation_needed" in c["href"])): 
                child_info.append((c['href'],c.string))
        """
        text = text +' ' + wrapper.get_text()
    
    
    return title,text


def BFS(query):
    query = query.lower()
    start_link = json.loads(requests.get(wiki_api_link + query).content)[3][0]
    count = 0
    queue = []
    titles = []
    links = [] 
    nodes = {} #name - group pair
    s = (query.lower(), start_link)
    group_num = 0
    nodes[unicode(query.lower())] = group_num
    queue.append(s)
    print(nodes)

    
    
    while queue and count <= 2:
        
        s = queue.pop(0)
        print("Scraping " + str(s))
        if s[1] != None and '#' not in s[1]:            
            title, text= scrape_wiki_link(s[1])
            
            #Add this entity to the nodes list if it doesn't exist
            if not s[0].lower() in nodes.keys():
                print("Adding again")
                group_num += 1
                nodes[s[0].lower()] = group_num
            
            
                
            
            #Find entities
            entities = google_nlp(text)
            
            #Remove duplicates and convert to lowercase
            entities = list(set(ent.lower() for ent in entities))
            print(entities)
            
            #If entities exist, then append to queue
            if entities:
                for ent in [e for e in entities if not e in nodes.keys()]:
                    try:
                        temp_link = json.loads(requests.get(wiki_api_link + ent).content)[3][0]
                        queue.append((ent,temp_link))
                        print("Appending " + str((ent,temp_link)))
                        #Add to nodes
                        if not ent in nodes.keys():
                            group_num += 1
                            nodes[ent.lower()] = group_num
                            #print("Added %s as %d"%(ent,group_num))
                            #Add to links
                        temp_link = {"source" : nodes[s[0].lower()], "target": group_num,"value": 1}
                        if not temp_link in links:
                            links.append(temp_link)
                    except IndexError:
                        continue
                print(nodes, links)
                count += 1
            
    return queue,nodes,links
    

BFS("machine learning")