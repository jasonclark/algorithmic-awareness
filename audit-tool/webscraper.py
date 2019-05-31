import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import io
import codecs 
import os.path
import sys

special_char_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd) 

def getPageInfo(url):
    r = requests.get(url)
    current = BeautifulSoup(r.content, 'html.parser')

    currentT = current.find('h1', attrs={'class': 'watch-title-container'})
    if currentT is None:
        print("Not a video")
        print()
    else:
        currentTi = currentT.find('span', attrs={'class': 'watch-title'}).text
        if currentTi is None:
            print("Not a video")
            print()
        else:
            currentTie = str(currentTi.translate(special_char_map))  #, 'utf-16').decode('utf-16', errors='replace'))
            currentTitl = currentTie[5:]
            currentTitle = currentTitl[:-3]
            print(currentTitle)
    
            currentVw = current.find('div', attrs={'class': 'watch-view-count'}) #span
            if currentVw is None:
                print("No views")
                currentViews = '0'
            else:
                currentView = currentVw.text
                currentViews = currentView[:-6]
                print(currentViews)
                
            currentCr = current.find('div', attrs={'class': 'yt-user-info'})
            if currentCr is None:
                print("No creator")
                currentCreator = 'None'
            else:
                currentCreate = currentCr.text
                currentCreator = currentCreate.strip()
                print(currentCreator)

            currentVerify = current.find('span', attrs={'class': 'yt-channel-title-icon-verified yt-uix-tooltip yt-sprite'})
            if currentVerify is None:
                print('Not verified?')
                isVerified = 'Not Verified'
            else:
                isVerified = currentVerify['aria-label']
                print('This channel is', isVerified)

            currentL = current.find('button', attrs={'class': 'yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target yt-uix-tooltip'})
            if currentL is None:
                print("No likes")
                currentLikes = '0'
            else:
                currentLikes = currentL.find('span', attrs={'class': 'yt-uix-button-content'}).text
                print(currentLikes)

            currentD = current.find('button', attrs={'class': 'yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target yt-uix-tooltip'})
            if currentD is None:
                print("No dislikes")
                currentDislikes = '0'
            else:
                currentDislikes = currentD.find('span', attrs={'class': 'yt-uix-button-content'}).text
                print(currentDislikes)

            currentDes = current.find('p', attrs={'id': 'eow-description'})
            if currentDes is None:
                print('No description')
                currentDescription = 'None'
            else:
                currentDescrip = currentDes.text
                currentDescription = str(currentDescrip.translate(special_char_map)) #, 'utf-16').decode('utf-16', errors='replace'))
                print(currentDescription)
        
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

            currentC = current.find_all('a', attrs={'class': 'yt-uix-sessionlink spf-link'})
            if currentC is None:
                print("No category")
                currentCategory = 'None'
            else:
                currentCat = currentC[-1]
                currentCategory = currentCat.text
                print(currentCategory)

            currentFam = current.find('meta', attrs={'itemprop': 'isFamilyFriendly'})
            if currentFam is None:
                print('Not family friendly?')
                statusF = 'False'
            else:
                statusF = str(currentFam['content'])
                print('Family Friendly =', statusF)

            currentPub = current.find('meta', attrs={'itemprop': 'datePublished'})
            if currentPub is None:
                print('No publish date')
                datePublished = '0000000'
            else:
                datePublished = str(currentPub['content'])
                print('Published =', datePublished)

            currentLen = current.find('span', attrs={'class': 'accessible-description'})
            if currentLen is None:
                print("No length")
                currentLength = '0'
            else:
                currentLeng = currentLen.text
                currentLengt = currentLeng[18:]
                currentLength = currentLengt[:-4]
                timeList = currentLength.split(":")
                if len(timeList) == 1:
                    currentLengthSec = int(timeList[0])
                elif len(timeList) == 2:
                    currentMin = int(timeList[0]) * 60
                    currentLengthSec = currentMin + int(timeList[1])
                elif len(timeList) == 3:
                    currentHour = int(timeList[0]) * 3600
                    currentMin = int(timeList[1]) * 60
                    currentLengthSec = currentHour + currentMin + int(timeList[2])
                print(currentLengthSec, "sec")

            videoL = current.find_all('a', attrs={'class': 'content-link spf-link yt-uix-sessionlink spf-link'})
            rec_titles=[]
            rec_urls = []
            for l in videoL:
                tmp = l['title']
                tmp1 = str(bytes(tmp, 'utf-16').decode('utf-16', errors='delete'))
                tmp2 ='https://www.youtube.com' +  l['href']
                rec_titles.append(tmp1.translate(special_char_map))
                rec_urls.append(tmp2)
            print(rec_titles)
            print()
            csvRow = [currentTitle, currentViews, currentCreator, isVerified, currentLikes, currentDislikes, currentDescription, currentSubscribers, currentCategory, statusF, datePublished, currentLengthSec, rec_titles, rec_urls]
            return csvRow

start = "https://www.youtube.com/results?search_query="
search = []
with open('input.txt') as fp:
    for line in fp:
        search.append(line.rstrip("\n"))
for s in search:
    page = requests.get(start+s)
    if(page.status_code != 200):
        print("Error! Page could not be reached.")
        exit()

    soup = BeautifulSoup(page.content, 'html.parser') 

    videoList = soup.find_all('a', attrs={'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})

    titles=[]
    urls = []
    for v in videoList:
        tmp1 = v['title']
        tmp2 ='https://www.youtube.com' +  v['href']
        titles.append(tmp1)
        urls.append(tmp2)

    savePath = 'C:/Users/Marielle/Desktop/algorithmic-awareness/search/output/'
    csvf = savePath+s+'.csv'
    csvR = ['Title', 'Views', 'Creator', 'Verified_Creator', 'Likes', 'Dislikes', 'Description', 'Subs', 'Category', 'Family_Friendly', 'Publish_Date', 'Length', 'Recommended_List_Titles', 'Recommended_List_URLs']
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
            recommended = csvRows[13]
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
    
