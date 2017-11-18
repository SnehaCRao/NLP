import re
import math
import sys
from decimal import Decimal, getcontext

getcontext().prec = 400

#fileInput = open("E:/NaturalLanguageProcessing/Homework5/hw5-data-corpus/catalan_corpus_train_tagged.txt", 'r')
fileModelOutput = open('hmmmodel.txt', 'w')
fileInput = open(sys.argv[1],'r')

lineCount = 0
tags = ["qiSTART"]
emissionDict = {}
transitionDict = {}
tagCount = {}

def getTags(lines):
    global lineCount
    for line in lines:
        lineCount += 1
        previousTag = "qiSTART"
        line = line.rstrip("\n").split(" ")
        for wordWithTag in line:
            wordTag = wordWithTag.lower()
            value = 1
            if wordTag not in emissionDict:
                 emissionDict[wordTag] = value
            else:
                 emissionDict[wordTag] += 1
            word = wordWithTag.split("/")
            if len(word) > 2:
                tag = word[-1]
            else:
                tag = word[1]
            addToWords(previousTag, tag)
            if re.search('^[A-Z][A-Z0]$', tag):
               wordTag = tag
               if tag not in tags:
                  tags.append(tag)
                  tagCount[wordTag] = 1
               else:
                  tagCount[wordTag] += 1
            previousTag = tag
    print lineCount
    return tags


def addToWords(previousTag, posttag):
    preTag = previousTag
    value = 1
    elementUpdated = False
    if preTag not in transitionDict:
        transitionDict.setdefault(preTag, {})
        transitionDict[preTag][posttag] = value
    else:
        for element in transitionDict[preTag]:
            if posttag == element:
                elementUpdated = True
                transitionDict[preTag][posttag] += 1
                break
        if not elementUpdated:
            transitionDict[preTag][posttag] = value


def writeToModel(tagName, data):
    fileModelOutput.write(tagName + "\n")
    fileModelOutput.write(str(data) + "\n")

with fileInput as f:
    lines = f.readlines()
    tags = getTags(lines)
    tagCount["qiSTART"] = lineCount

with fileModelOutput as modelFile:
    writeToModel("tagsCount", tagCount)
    for tagVal in transitionDict:
        total = 0
        for element in transitionDict[tagVal]:
            total += Decimal(transitionDict[tagVal][element])
        for element in tagCount.keys():
            if element in transitionDict[tagVal]:
                transitionDict[tagVal][element] = (math.log((Decimal(transitionDict[tagVal][element]) + 1) /
                                                            (total + len(tagCount.keys()))))
            else:
                transitionDict[tagVal][element] = (math.log(1. / len(tagCount.keys())))

    writeToModel("transition", transitionDict)

    for wordTag in emissionDict:
        startTag = wordTag[-2:].upper()
        emissionDict[wordTag] = (math.log(Decimal(emissionDict[wordTag]) / Decimal(tagCount[startTag])))
    writeToModel("emission", emissionDict)

    # outputDict["tagsCount"] = tagCount
    # outputDict["transition"] = transitionDict
    # outputDict["emission"] = emissionDict
    #
    # print outputDict
    # pickle.dump(outputDict, modelFile)

