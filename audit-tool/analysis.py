import pandas as pd
import csv
import os
import numpy as np
import sys
import glob
import collections
import matplotlib.pyplot as plt

special_char_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
delCol = ['Recommended_List_URLs']
intCol = ['Views', 'Likes', 'Dislikes', 'Likes (%)', 'Dislikes (%)', 'Links', 'Capitals', 'Capitals (%)', 'Subs', 'Length']
search = []

def fileAnalysis(currentPath):
    tags = []
    flatList = []
    for currentFile in os.listdir(currentPath):
        file = currentPath+currentFile
        df = pd.read_csv(file)
        df = df.drop(delCol, axis=1)
        tag = df.Tags.values
        for x in tag:
            x = str(x.translate(special_char_map))
            flatList += x.split(',')
        df.Publish_Date = pd.to_datetime(df['Publish_Date'])
        df[intCol] = df[intCol].replace(np.nan,0)
        df[intCol] = df[intCol].applymap(np.int64)
        outputFile = outputPath+currentFile
        data = df.describe()
        print(data)
        data.to_csv(outputFile, sep=',')
    ListTag = collections.Counter(flatList)
    with open(outputPath+'/TagData.csv','a', encoding='utf-8') as csvfile:
        writer=csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #writer.writerow(ListTag)
        for key, value in ListTag.items():
            writer.writerow([key, value])
            
if (os.path.exists("data") == False): 
    os.mkdir("data")

if (os.path.exists("output") == False):
    print("Error no data available.")
    print("Please run the webscraper to collect data.")
else:
    search = next(os.walk("output"))[1]
    for s in search:
        currentPath = 'output/'+s+'/'
        outputPath = 'data/'+s+'/'
        if (os.path.exists(outputPath) == False):
            os.mkdir(outputPath)
        all_files = glob.glob(os.path.join(currentPath, "*.csv"))
        fileAnalysis(currentPath)
    
