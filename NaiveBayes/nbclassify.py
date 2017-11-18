import json
import string
import sys

truthResult = 0.0
deceptiveResult = 0.0
positiveResult = 0.0
negativeResult = 0.0

# inFileName = 'train-text.txt'
inFileName = sys.argv[1]
outputFileName = 'nboutput.txt'
modelFileName = 'nbmodel.txt'


outputFile = open(outputFileName, 'w')

with open(modelFileName) as data_file:
    data = json.load(data_file)
# truthResult = data["priorTruthful"]
# deceptiveResult = data["priorDeceptive"]
# positiveResult = data["priorPositive"]
# negativeResult = data["priorNegative"]

#inputData = open(inFileName, 'r').read()
for line in open(inFileName):
    #to retrieve the alphanumeric key
    keyValue = line.split(None, 1)[0]
    # to retrieve the rest of the text
    stringText = line.split(' ', 1)[1]
    stringText = stringText.translate(string.maketrans("", ""), string.punctuation)
    stringText = stringText.lower().strip()
    terms = stringText.split()
    truthResult = data["priorTruthful"]
    deceptiveResult = data["priorDeceptive"]
    positiveResult = data["priorPositive"]
    negativeResult = data["priorNegative"]
    for dataText in terms:
        if dataText in data["wordTruthfulClass"]:
            truthResult += data["wordTruthfulClass"][dataText]
        if dataText in data["wordDeceptiveClass"]:
            deceptiveResult += data["wordDeceptiveClass"][dataText]
        if dataText in data["wordPositiveClass"]:
            positiveResult += data["wordPositiveClass"][dataText]
        if dataText in data["wordNegativeClass"]:
            negativeResult += data["wordDeceptiveClass"][dataText]

    outputFile.write(keyValue+" ")
    if truthResult >= deceptiveResult:
        outputFile.write("truthful ")
    else:
        outputFile.write("deceptive ")
    if positiveResult >= negativeResult:
        outputFile.write("positive\n")
    else:
        outputFile.write("negative\n")
