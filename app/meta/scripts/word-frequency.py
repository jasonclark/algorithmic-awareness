#!/usr/bin/python
from string import punctuation
from collections import defaultdict

N = 100
words = {}

print "Top %d terms in text file" % N

words_gen = (word.strip(punctuation).lower() for line in open("search-log.txt")
for word in line.split())

words = defaultdict(int)
for word in words_gen:
  words[word] +=1

top_words = sorted(words.iteritems(),
  key=lambda(word, count): (-count, word))[:N]

for word, frequency in top_words:
  print "%s: %d" % (word, frequency)
