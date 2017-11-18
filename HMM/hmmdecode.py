import sys
from decimal import Decimal, getcontext

getcontext().prec = 400

fileModelInput = open('hmmmodel.txt', 'r')
fileModelOutput = open('hmmoutput.txt', 'w')
fileTestInput = open(sys.argv[1], 'r')
#fileTestInput = open("E:/NaturalLanguageProcessing/Homework5/hw5-data-corpus/catalan_corpus_dev_raw.txt", 'r')
lineCount = 0

def tagData(lines):
    global lineCount
    for line in lines:
        lineCount += 1
        previousTag = "qiSTART"
        previousProbability = 0
        line = line.split(" ")
        for word in line:
            if "\n" in word:
                addendChar = "\n"
                word = word.rstrip("\n")
            else:
                addendChar = " "
            wordToBeTagged = word.lower()
            tagProbability = []
            tagName = []
            for element in transition[previousTag]:
                nextTag = element
                wordWithTag = wordToBeTagged + "/" + nextTag.lower()
                if wordWithTag in emission:
                    probability = previousProbability + transition[previousTag][nextTag] + emission[wordWithTag]
                else:
                    probability = previousProbability + transition[previousTag][nextTag] - 50
                tagName.append(nextTag)
                tagProbability.append(probability)
            besttag = tagName[tagProbability.index(max(tagProbability))]
            highestProbability = max(tagProbability)
            previousTag = besttag
            previousProbability = highestProbability
            fileModelOutput.write(word + "/" + besttag + addendChar)

with fileModelInput as dataFile:
    tagCountName = dataFile.readline()
    tagsCount = dataFile.readline()
    tagCount = eval(tagsCount)

    transName = dataFile.readline()
    transData = dataFile.readline()
    transition = eval(transData)

    emissionName = dataFile.readline()
    emissionData = dataFile.readline()
    emission = eval(emissionData)

with fileTestInput as inputFile:
    lines = inputFile.readlines()
    tagData(lines)
