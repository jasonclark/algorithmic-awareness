#prototype script for listing Google Autosuggest phrases
#inspired by https://importsem.com/query-google-suggestions-api-with-python/
#TODO:
#add headers to identify crawler
#create output as structured data file

import sys
import requests
import json
from fake_useragent import UserAgent

#Keyword to search, can be passed to script -> python audit-google-suugestions.py "ADD-KEYWORDS-HERE"
keyword = sys.argv[1] if len(sys.argv) > 1 else 'man is'
#keyword = "man is"
keyword.replace(" ", "+")

#client or output = What client to mask as (Firefox, Chrome, Toolbar). Determines the format of response. toolbar = XML. Firefox or Chrome = JSON.
#hl = Country to use (us, uk , fr…)
#gl = Language to use (en, es, fr…)
#q = Your query
#2 working API URLS = https://www.google.com/complete/search?client=toolbar&hl=en&gl=en&q= OR https://suggestqueries.google.com/complete/search?output=chrome&hl=en&gl=en&q=

#set suggestions API URL - note: using HTTP not HTTPS
#url = "https://suggestqueries.google.com/complete/search?output=firefox&q=" + keyword
url = "http://www.google.com/complete/search?client=chrome&hl=en&gl=en&q=" + keyword

#create user agent
ua = UserAgent()
headers = {"user-agent": ua.chrome}

#make request with user agent
response = requests.get(url, headers=headers, verify=False)

#data request without user agent
#response = requests.get(url, verify=True)

#store data returned from API request
data = json.loads(response.text)

#set up array to hold each suggestion returned
suggestions = []
for word in data[1]:
  suggestions.append(word)

#collate and print out list of suggestions
keywords = json.dumps(suggestions)
print(keywords)

