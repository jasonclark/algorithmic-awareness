import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import io
import codecs 
import os
import numpy as np
import sys
import glob

special_char_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
delCol = ['Recommended_List_URLs']
intCol = ['Views', 'Likes', 'Dislikes', 'Likes (%)', 'Dislikes (%)', 'Links', 'Capitals', 'Capitals (%)', 'Subs', 'Length']
search = []

def fileAnalysis(currentPath):
    for currentFile in os.listdir(currentPath):
        file = currentPath+currentFile
        df = pd.read_csv(file)
        df = df.drop(delCol, axis=1)
        df.Publish_Date = pd.to_datetime(df['Publish_Date'])
        df[intCol] = df[intCol].replace(np.nan,0)
        df[intCol] = df[intCol].applymap(np.int64)
        outputFile = outputPath+currentFile
        data = df.describe()
        print(data)
        data.to_csv(outputFile, sep=',')
    
with open('input.txt') as fp:
    for line in fp:
        search.append(line.rstrip("\n"))
for s in search:
    currentPath = 'output/'+s+'/'
    outputPath = 'data/'+s+'/'
    os.mkdir(outputPath)
    all_files = glob.glob(os.path.join(currentPath, "*.csv"))
    fileAnalysis(currentPath)
