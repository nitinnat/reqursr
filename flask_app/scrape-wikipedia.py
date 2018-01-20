# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 00:07:25 2018

@author: Nitin
"""

from bs4 import BeautifulSoup
import requests
import json
from collections import defaultdict

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


##Test
    
#a = scrape_wiki_link(base_link +link)[1]

def BFS(query):
    start_link = json.loads(requests.get(wiki_api_link + query).content)[3][0]
    print(start_link)
    count = 0
    queue = []
    
    link_dic = defaultdict(dict)
    titles = []
    s = (query.lower(), start_link)
    print(s)
    
    existing_ents = set()
    links = [] #source-target pair
    nodes = {} #name - group pair
    group_num = 0
    nodes[query.lower()] = 0
    queue.append(s)
    existing_ents.add(query.lower())
    
    
    while queue and count <= 2:
        s = queue.pop(0)
        
        if s[1] != None and '#' not in s[1]:
            print("Scraping: " +str(s[0]))
            
            title, text= scrape_wiki_link(s[1])
            
            #Add this entity to the nodes list if it doesn't exist
            if not s[0].lower() in nodes.keys():
                group_num += 1
                nodes[s[0]] = group_num
                existing_ents.add(s[0].lower())
                
            
            #Find entities
            entities = google_nlp(text)
            titles.append(title)
            print("Title: " + str(title))            
            link_dic[count]['text'] = text
            link_dic[count]['entities'] = entities
            print(entities)
            ##Add to the parent_Child_Rel dictionary
            print("Adding parent %s and its children to the relationship dictionary"%title)

            if entities:
                for ent in [e for e in entities if not e in existing_ents]:
                    try:
                        temp_link = json.loads(requests.get(wiki_api_link + ent).content)[3][0]
                        queue.append((ent,temp_link))

                        #Add to nodes
                        if not ent in nodes.keys():
                            group_num += 1
                            nodes[ent] = group_num
                            existing_ents.add(ent)
                            print("Added %s as %d"%(ent,group_num))
                            
                        #Add to links
                        links.append({"source" : nodes[s[0]], "target": group_num})
                        
                    except IndexError:
                        continue
                count += 1
            
    return queue,link_dic,nodes,links

def get_graph_data(query):
    a,b,node_dic,links = BFS(query.lower())
    nodes = []
    for n in node_dic.keys():
        nodes.append({"name":n,"group":node_dic[n]})
    my_json = {"nodes": nodes, "links": links}
    with open('graph.json', 'w') as fp:
        json.dump(my_json, fp)
    return my_json
    
        