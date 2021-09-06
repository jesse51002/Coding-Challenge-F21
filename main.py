"""
Author:  Jesse Musa
Project: Sentiment Analysis
Date: 09/04/2021

References:
    #Basic explaination
    “A Quick Guide To Sentiment Analysis | Sentiment Analysis In Python Using Textblob | Edureka.”
    Youtube, uploaded by edureka!, 8 Aug. 2018,
    www.youtube.com/watch?v=O_B7XLfx0ic.

    #Indepth explaination
    “Lecture 5 – Sentiment Analysis 1 | Stanford CS224U: Natural Language Understanding | Spring 2019.”
    Youtube, uploaded by stanfordonline, 18 July 2019,
    www.youtube.com/watch?v=O1Xh3H1uEYY.

    #Stopwords
    https://www.ranks.nl/stopwords

    #Sentiment Dictionary
    Theresa Wilson, Janyce Wiebe, and Paul Hoffmann (2005). Recognizing Contextual Polarity in Phrase-Level Sentiment Analysis. Proc. of HLT-EMNLP-2005.
    http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/

    # Negation Words
    https://www.grammarly.com/blog/negatives/
"""

import re

# Reciving input
txtFile = open("input.txt", "r")
txtStringRaw = txtFile.read()

# Removing symbols(cleaning)
txtStringClean = re.sub("[\n]+", " ", txtStringRaw)
txtStringClean = re.sub("[.]+", " .", txtStringClean)  # Keeping period in order to group sentences
txtStringClean = re.sub("[^a-zA-Z. ]+", "", txtStringClean)

# Making an array of words
wordsArr = txtStringClean.split(" ")

# Inputting StopWords
stopWords = []
stopWordsFile = open("stopWords.txt", "r")
for word in stopWordsFile:
    stopWords.append(re.sub("[^a-zA-Z ]", "", word))

# Removing stop words
for i in range(0, len(wordsArr)):
    if i >= len(wordsArr):
        break
    word = wordsArr[i]
    for sWord in stopWords:

        if word.lower() == sWord.lower():
            wordsArr.pop(i)
            i = i - 1
            break

# Inputting Sentiment Dictionary

sentimentDic = {}

sentDicFile = open('subjclueslen1-HLTEMNLP05.tff')

for sentWrdLine in sentDicFile:
    sentWrdSpl = sentWrdLine.split(" ")

    curWord = sentWrdSpl[2].split("=")[1]

    polarityWrd = re.sub("[^a-zA-Z ]+", "", sentWrdSpl[5].split("=")[1])

    polarityVal = 0
    if polarityWrd == 'negative':
        polarityVal = -1
    if polarityWrd == 'positive':
        polarityVal = 1

    sentimentDic[curWord] = polarityVal

# Inputting Negation words
negationWords = []
negWordsFile = open("negationWords.txt", "r")
for word in negWordsFile:
    negationWords.append(re.sub("[^a-zA-Z]", "", word.lower()))

# Finding the sentiment value of the input

totalSentWords = 0
totalSentimentVal = 0

sentenceValues = []
sentenceNegation = False
sentence = ""


# Will evaluate every sentence separately for negation


def newSentence():
    global sentenceValues
    global sentenceNegation
    global totalSentimentVal
    global totalSentWords
    global sentence

    multiplier = 1
    if sentenceNegation:
        multiplier = -1

    for x in sentenceValues:
        totalSentimentVal += x * multiplier

    totalSentWords += len(sentenceValues)
    sentenceValues = []
    sentenceNegation = False
    sentence = ""


for i in range(0, len(wordsArr)):
    word = wordsArr[i]

    if word == ".":
        newSentence()
        continue

    sentence += word + " "

    if wordsArr[i].lower() in negationWords:
        sentenceNegation = True

    if word.lower() in sentimentDic:
        sentVal = sentimentDic[word.lower()]
        sentenceValues.append(sentVal)

newSentence()

avgSentVal = totalSentimentVal / totalSentWords
print("Sentiment value is from range [-1,1] where 1 is extermely positive, 0 is neutral and -1 is negative")
print("Sentiment Value:", avgSentVal)

