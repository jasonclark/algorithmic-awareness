import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import io
import os
import sys
import re 

special_char_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd) #set of characters

def getTitle(current): #retrieve title from the Youtube video
    currentT = current.find('h1', attrs={'class': 'watch-title-container'})
    if currentT is None:
        return currentT
    else:
        currentTi = currentT.find('span', attrs={'class': 'watch-title'}).text
        if currentTi is None:
            return currentTi
        else:
            currentTie = str(currentTi.translate(special_char_map))
            currentTitl = currentTie[5:]
            currentTitle = currentTitl[:-3]
            print(currentTitle)
            return currentTitle
        
def getViews(current): #retrieve number of views from the Youtube video 
    currentV = current.find('div', attrs={'class': 'watch-view-count'})
    if currentV is None:
        print("No views")
        currentViews = '0'
    else:
        currentVw = currentV.text
        currentView = currentVw[:-6]
        currentViews = currentView.replace(",","")
        print("Views: ", currentViews)
    return currentViews

def getCreator(current): #retrieve name of video creator from the Youtube video 
    currentCr = current.find('div', attrs={'class': 'yt-user-info'})
    if currentCr is None:
        print("No creator")
        currentCreator = 'None'
    else:
        currentCreate = currentCr.text
        currentCreator = currentCreate.strip()
        print("Creator:", currentCreator)
    return currentCreator 
    
def getVerify(current): #retrieve if creator is verified from the Youtube video 
    currentVerify = current.find('span', attrs={'class': 'yt-channel-title-icon-verified yt-uix-tooltip yt-sprite'})
    if currentVerify is None:
        print('Not verified?')
        isVerified = 'Not Verified'
    else:
        isVerified = currentVerify['aria-label']
        print('This channel is', isVerified)
    return isVerified 
    
def getLikes(current): #retrieve number of likes from the Youtube video
    currentL = current.find('button', attrs={'class': 'yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target yt-uix-tooltip'})
    if currentL is None:
        print("No likes")
        currentLikes = '0'
    else:
        currentLike = currentL.find('span', attrs={'class': 'yt-uix-button-content'}).text
        currentLikes = currentLike.replace(",","")
        print("Likes: ", currentLikes)
    return currentLikes
    
def getDislikes(current): #retrieve number of dislikes from the Youtube video 
    currentD = current.find('button', attrs={'class': 'yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target yt-uix-tooltip'})
    if currentD is None:
        print("No dislikes")
        currentDislikes = '0'
    else:
        currentDislike = currentD.find('span', attrs={'class': 'yt-uix-button-content'}).text
        currentDislikes = currentDislike.replace(",","")
        print("Dislikes: ", currentDislikes)
    return currentDislikes

def getPercentLike(currentLikes, currentDislikes): #calculate the percentage of likes
    total = int(currentLikes,10) + int(currentDislikes,10)
    if total != 0:
        currentPercentLike = (int(currentLikes,10)/total)*100
        print("Likes (%): ", currentPercentLike)
        return currentPercentLike

def getPercentDislike(currentLikes, currentDislikes): #calculate the percentage of dislikes
    total = int(currentLikes,10) + int(currentDislikes,10)
    if total != 0:
        currentPercentDislike = (int(currentDislikes,10)/total)*100
        print("Dislikes (%): ", currentPercentDislike)
        return currentPercentDislike

def getDescription(current): #retrieve the video discription from the Youtube video
    currentDes = current.find('p', attrs={'id': 'eow-description'})
    if currentDes is None:
        print('No description')
        currentDescription = 'None'
    else:
        currentDescrip = currentDes.text
        currentDescription = str(currentDescrip.translate(special_char_map)) 
        print(currentDescription)
    return currentDescription

def getLinks(currentDescription): # determine the number of links in the description
    link = "http"
    currentLinks = currentDescription.count(link)
    print("Links: ", currentLinks)
    return currentLinks

def getCapitalization(currentDescription): #determine the number of capitalized words in the description
    currentCapitals = len(re.findall(r'[A-Z]', currentDescription))
    print("Capitals: ", currentCapitals)
    return currentCapitals

def getPercentCapital(currentCapitals, currentDescription): #determine the percentage of capital letters in description
    Dtotal = len(currentDescription)
    if Dtotal != 0:
        currentPercentCapital = (currentCapitals/Dtotal)*100
        print("Capitals (%): ", currentPercentCapital)
        return currentPercentCapital

def getSubscribers(current): #retrieve the number of subscribers from the Youtube video
    currentSub = current.find('span', attrs={'class': 'yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count'})
    if currentSub is None:
        print("No subs")
        currentSubscribers = '0'
    else:
        currentSubs = currentSub.text
        if 'K' in currentSubs:
            currentSubscribe = currentSubs[:-1]
            currentSubscriber = float(currentSubscribe)
            currentSubscriber = currentSubscriber*1000
        elif 'M' in currentSubs:
            currentSubscribe = currentSubs[:-1]
            currentSubscriber = float(currentSubscribe)
            currentSubscriber = currentSubscriber*1000000
        else:
            currentSubscriber = currentSubs
        currentSubscribers = int(currentSubscriber)
        print(currentSubscribers)
    return currentSubscribers 

def getCategory(current): #retrieve the category of the Youtube video
    currentC = current.find_all('a', attrs={'class': 'yt-uix-sessionlink spf-link'})
    if currentC is None:
        print("No category")
        currentCategory = 'None'
    else:
        currentCat = currentC[-1]
        currentCategory = currentCat.text
        print(currentCategory)
    return currentCategory

def getFamily(current): #retrieve if the video is considered Family Friendly from the Youtube video
    currentFam = current.find('meta', attrs={'itemprop': 'isFamilyFriendly'})
    if currentFam is None:
        print('Not family friendly?')
        statusF = 'False'
    else:
        statusF = str(currentFam['content'])
        print('Family Friendly =', statusF)
    return statusF
    
def getPublished(current): #retrieve the publishing date of the Youtube video
    currentPub = current.find('meta', attrs={'itemprop': 'datePublished'})
    if currentPub is None:
        print('No publish date')
        datePublished = '0000000'
    else:
        datePublished = str(currentPub['content'])
        print('Published =', datePublished)
    return datePublished
    
def getLength(current): #retrieve the length of the Youtube video (in seconds)
    currentLen = current.find('span', attrs={'class': 'accessible-description'})
    if currentLen is None:
        print("No length")
        currentLengthSec = '0'
    else:
        currentLeng = currentLen.text
        currentLengt = currentLeng[18:]
        currentLength = currentLengt[:-4]
        timeList = currentLength.split(":")
        if len(timeList) == 1:
            if timeList[0] == '':
                currentLengthSec = 0
            else:
                currentLengthSec = int(timeList[0])
        elif len(timeList) == 2:
            currentMin = int(timeList[0]) * 60
            currentLengthSec = currentMin + int(timeList[1])
        elif len(timeList) == 3:
            currentHour = int(timeList[0]) * 3600
            currentMin = int(timeList[1]) * 60
            currentLengthSec = currentHour + currentMin + int(timeList[2])
        print(currentLengthSec, "sec")
    return currentLengthSec

def getTags(current): #retrieve the tags of the Youtube video
    currentTags = current.find_all('meta', attrs={'property': 'og:video:tag'})
    tags = []
    for t in currentTags:
        tmp = t['content']
        tmp1 = str(bytes(tmp, 'utf-16').decode('utf-16', errors='delete'))
        tags.append(tmp1.translate(special_char_map))
    print('Tags: ',tags)
    return tags

def getRecommendedT(current): #retrieve an array of all recommended video titles for the Youtube video 
    videoL = current.find_all('a', attrs={'class': 'content-link spf-link yt-uix-sessionlink spf-link'})
    rec_titles=[]
    for l in videoL:
        tmp = l['title']
        tmp1 = str(bytes(tmp, 'utf-16').decode('utf-16', errors='delete'))
        rec_titles.append(tmp1.translate(special_char_map))
    print()
    return rec_titles

def getRecommendedURL(current): #retrieve an array of all recommended video urls for the Youtube video 
    videoL = current.find_all('a', attrs={'class': 'content-link spf-link yt-uix-sessionlink spf-link'})
    rec_urls = [] 
    for l in videoL:
        tmp2 ='https://www.youtube.com' +  l['href']
        rec_urls.append(tmp2)
    return rec_urls 

def getPageInfo(url): #gets all information of youtube video
    r = requests.get(url,timeout = 10)
    current = BeautifulSoup(r.content, 'html.parser')
    currentTitle = getTitle(current)
    if currentTitle is None:
        print("Not a video")
    else:
        currentViews = getViews(current) 
        currentCreator = getCreator(current)
        currentVerified = getVerify(current)
        currentLikes = getLikes(current)
        currentDislikes = getDislikes(current)
        currentPercentLike = getPercentLike(currentLikes, currentDislikes)
        currentPercentDislike = getPercentDislike(currentLikes, currentDislikes)
        currentDescription = getDescription(current)
        currentLinks = getLinks(currentDescription)
        currentCapitals = getCapitalization(currentDescription)
        currentPercentCapital = getPercentCapital(currentCapitals, currentDescription) 
        currentSubscribers = getSubscribers(current)
        currentCategory = getCategory(current)
        currentFF = getFamily(current)
        currentPublished = getPublished(current)
        currentLengthSec = getLength(current)
        currentTags = getTags(current)
        rec_urls = [] 
        rec_titles = getRecommendedT(current)
        rec_urls = getRecommendedURL(current)

        csvRow = [currentTitle, currentViews, currentCreator, currentVerified, currentLikes, currentDislikes, currentPercentLike, currentPercentDislike, currentDescription, currentLinks, currentCapitals, currentPercentCapital, currentSubscribers, currentCategory, currentFF, currentPublished, currentLengthSec, currentTags, rec_titles, rec_urls]
        return csvRow

if (os.path.exists("output") == False):
    os.mkdir("output")

start = "https://www.youtube.com/results?search_query="
search = []
inputString = input("Enter a list of search terms separated by comma (no space between words): ")
search = inputString.split(",")
for s in search:
    if " " in s:
        s.replace(" ", "+")
    try:
        page = requests.get(start+s,timeout=10)
    except requests.exceptions.Timeout:
        print("Timeout occured")
        
    soup = BeautifulSoup(page.content, 'html.parser')

    videoList = soup.find_all('a', attrs={'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})

    titles=[]
    urls = []
    for v in videoList:
        tmp1 = v['title']
        tmp2 ='https://www.youtube.com' +  v['href']
        titles.append(tmp1)
        urls.append(tmp2)

    savePath = 'output/'+s+'/'
    os.mkdir(savePath)
    csvf = savePath+s+'.csv'
    csvR = ['Title', 'Views', 'Creator', 'Verified_Creator', 'Likes', 'Dislikes', 'Likes (%)', 'Dislikes (%)', 'Description', 'Links', 'Capitals', 'Capitals (%)', 'Subs', 'Category', 'Family_Friendly', 'Publish_Date', 'Length', 'Tags', 'Recommended_List_Titles', 'Recommended_List_URLs']
    with io.open(csvf, 'a', encoding='utf-8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(csvR)

    num = 0
    for i in urls:
        num += 1
        csvRows = getPageInfo(i)
        if csvRows is None:
            print('Not a video')
        else:
            with io.open(csvf, 'a', encoding='utf-8') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(csvRows) 
            recommended = csvRows[19]
            holdT = s+"_%d" %num
            xmlTitle = savePath+holdT+'.csv'
            with io.open(xmlTitle, 'a', encoding='utf-8') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(csvR)
            for r in recommended:
                ignore = getPageInfo(r)
                if ignore is None:
                    print('Not a video')
                else:
                    with io.open(xmlTitle, 'a', encoding='utf-8') as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        filewriter.writerow(ignore)
    
