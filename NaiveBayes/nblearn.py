import sys
import json
import math
import string

NEGATIVE = "negative"

DECEPTIVE = "deceptive"

TRUTHFUL = "truthful"

POSITIVE = "positive"

# trainFile = 'train-text.txt'
trainFile = sys.argv[1]
# labelFile = 'train-labels.txt'
labelFile = sys.argv[2]
modelName = 'nbmodel.txt'
class1Dictionary = {}
class2Dictionary = {}
reviewTextDictionary = {}
trainingVocabulary = {}
deceptiveDictionary = {}
positiveDictionary = {}
truthfulDictionary = {}
negativeDictionary = {}
mapTrainData = {}
truthCount = 0
deceptiveCount = 0
positiveCount = 0
negativeCount = 0

STOP_WORDS = ['a', 'as', 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after',
              'afterwards', 'again', 'against', 'aint', 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'already',
              'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any', 'anybody',
              'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'appear', 'appreciate',
              'appropriate', 'are', 'arent', 'around', 'as', 'aside', 'ask', 'asking', 'associated', 'at', 'available',
              'away', 'awfully', 'b', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before',
              'beforehand', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'best', 'better', 'between',
              'beyond', 'both', 'brief', 'but', 'by', 'c', 'cmon', 'cs', 'came', 'can', 'cant', 'cannot', 'cant',
              'cause', 'causes', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes',
              'concerning', 'consequently', 'consider', 'considering', 'contain', 'containing', 'contains',
              'corresponding', 'could', 'couldnt', 'course', 'currently', 'd', 'definitely', 'described', 'despite',
              'did', 'didnt', 'different', 'do', 'does', 'doesnt', 'doing', 'dont', 'done', 'down', 'downwards',
              'during', 'e', 'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'enough', 'entirely',
              'especially', 'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere',
              'ex', 'exactly', 'example', 'except', 'f', 'far', 'few', 'fifth', 'first', 'five', 'followed',
              'following', 'follows', 'for', 'former', 'formerly', 'forth', 'four', 'from', 'further', 'furthermore',
              'g', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten',
              'greetings', 'h', 'had', 'hadnt', 'happens', 'hardly', 'has', 'hasnt', 'have', 'havent', 'having', 'he',
              'hes', 'hello', 'help', 'hence', 'her', 'here', 'heres', 'hereafter', 'hereby', 'herein', 'hereupon',
              'hers', 'herself', 'hi', 'him', 'himself', 'his', 'hither', 'hopefully', 'how', 'howbeit', 'however', 'i',
              'id', 'ill', 'im', 'ive', 'ie', 'if', 'ignored', 'immediate', 'in', 'inasmuch', 'inc', 'indeed',
              'indicate', 'indicated', 'indicates', 'inner', 'insofar', 'instead', 'into', 'inward', 'is', 'isnt', 'it',
              'itd', 'itll', 'its', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'knows',
              'known', 'l', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets',
              'like', 'liked', 'likely', 'little', 'look', 'looking', 'looks', 'ltd', 'm', 'mainly', 'many', 'may',
              'maybe', 'me', 'mean', 'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much',
              'must', 'my', 'myself', 'n', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs',
              'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor',
              'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'o', 'obviously', 'of', 'off', 'often', 'oh',
              'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'otherwise',
              'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own', 'p', 'particular',
              'particularly', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible', 'presumably', 'probably',
              'provides', 'q', 'que', 'quite', 'qv', 'r', 'rather', 'rd', 're', 'really', 'reasonably', 'regarding',
              'regardless', 'regards', 'relatively', 'respectively', 'right', 's', 'said', 'same', 'saw', 'say',
              'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen',
              'self', 'selves', 'sensible', 'sent', 'serious', 'seriously', 'seven', 'several', 'shall', 'she',
              'should', 'shouldnt', 'since', 'six', 'so', 'some', 'somebody', 'somehow', 'someone', 'something',
              'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specified', 'specify', 'specifying',
              'still', 'sub', 'such', 'sup', 'sure', 't', 'ts', 'take', 'taken', 'tell', 'tends', 'th', 'than', 'thank',
              'thanks', 'thanx', 'that', 'thats', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then',
              'thence', 'there', 'theres', 'thereafter', 'thereby', 'therefore', 'therein', 'theres', 'thereupon',
              'these', 'they', 'theyd', 'theyll', 'theyre', 'theyve', 'think', 'third', 'this', 'thorough',
              'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together',
              'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'twice', 'two', 'u', 'un',
              'under', 'unfortunately', 'unless', 'unlikely', 'until', 'unto', 'up', 'upon', 'us', 'use', 'used',
              'useful', 'uses', 'using', 'usually', 'uucp', 'v', 'value', 'various', 'very', 'via', 'viz', 'vs', 'w',
              'want', 'wants', 'was', 'wasnt', 'way', 'we', 'wed', 'well', 'were', 'weve', 'welcome', 'well', 'went',
              'were', 'werent', 'what', 'whats', 'whatever', 'when', 'whence', 'whenever', 'where', 'wheres',
              'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while',
              'whither', 'who', 'whos', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'willing', 'wish', 'with',
              'within', 'without', 'wont', 'wonder', 'would', 'would', 'wouldnt', 'x', 'y', 'yes', 'yet', 'you', 'youd',
              'youll', 'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves', 'z', 'zero']

for line in open(labelFile):
        # split the alphanumeric,truthful/deceptive and positive/negative reviews
        alphaNumValue, class1, class2 = line.split(' ')
        # count the number of occurences of truthful/deceptive in myDictionaryClass1
        #print class1, class2
        class1 = class1.strip()
        class2 = class2.strip()
        if class1.lower() == TRUTHFUL:
            truthCount += 1
        elif class1.lower() == DECEPTIVE:
            deceptiveCount += 1

        if class2.lower() == POSITIVE:
            positiveCount += 1
        elif class2.lower() == NEGATIVE:
            negativeCount += 1
        # add the truthful/deceptive review to the myDictionaryClass1
        class1Dictionary.setdefault(alphaNumValue, class1)
        # add the positive/negative review to the myDictionaryClass2
        class2Dictionary.setdefault(alphaNumValue, class2)

for line in open(trainFile):
    #to retrieve the alphanumeric key
    keyValue = line.split(None, 1)[0]
    # to retrieve the rest of the text
    stringText = line.split(' ', 1)[1]
    stringText = stringText.translate(string.maketrans("", ""), string.punctuation)
    stringText = stringText.lower().strip()
    # tokens = stringText.split(' ')
    # terms = filter(None, tokens)
    terms = stringText.split()
    for currentWord in terms:
        if currentWord in STOP_WORDS:
            continue
        # reviewTextDictionary.setdefault(keyValue, []).append(current_word)
        if currentWord not in trainingVocabulary:
            trainingVocabulary[currentWord] = 1
        else:
            trainingVocabulary[currentWord] += 1
        if TRUTHFUL == class1Dictionary.get(keyValue):
            if currentWord not in truthfulDictionary:
                truthfulDictionary[currentWord] = 1
            else:
                truthfulDictionary[currentWord] += 1
        if DECEPTIVE == class1Dictionary.get(keyValue):
            if currentWord not in deceptiveDictionary:
                deceptiveDictionary[currentWord] = 1
            else:
                deceptiveDictionary[currentWord] += 1
        if POSITIVE == class2Dictionary.get(keyValue):
            if currentWord not in positiveDictionary:
                positiveDictionary[currentWord] = 1
            else:
                positiveDictionary[currentWord] += 1
        if NEGATIVE == class2Dictionary.get(keyValue):
            if currentWord not in negativeDictionary:
                negativeDictionary[currentWord] = 1
            else:
                negativeDictionary[currentWord] += 1
# Probabilities of the word in a given class - truthful/ deceptive ; positive/negative
truthfulProb = {}
deceptiveProb = {}
positiveProb = {}
negativeProb = {}

# total number of words in positiveClass, negativeClass, truthfulClass, deceptiveClass
positiveTotal = 0
negativeTotal = 0
truthTotal = 0
deceptiveTotal = 0

for key, value in positiveDictionary.iteritems():
    positiveTotal += value
for key, value in negativeDictionary.iteritems():
    negativeTotal += value
for key, value in truthfulDictionary.iteritems():
    truthTotal += value
for key, value in deceptiveDictionary.iteritems():
    deceptiveTotal += value

lenUniquePN = len(trainingVocabulary)

for x in trainingVocabulary.keys():
    if x in positiveDictionary:
        positiveProb[x] = math.log10((positiveDictionary[x] + 1) / float(positiveTotal + lenUniquePN))
    else:
        positiveProb[x] = math.log10(1 / float(positiveTotal + lenUniquePN))

for x in trainingVocabulary.keys():
    if x in negativeDictionary:
        negativeProb[x] = math.log10((negativeDictionary[x] + 1) / float(negativeTotal + lenUniquePN))
    else:
        negativeProb[x] = math.log10(1 / float(negativeTotal + lenUniquePN))

for x in trainingVocabulary.keys():
    if x in truthfulDictionary:
        truthfulProb[x] = math.log10((truthfulDictionary[x] + 1) / float(truthTotal + lenUniquePN))
    else:
        truthfulProb[x] = math.log10(1 / float(truthTotal + lenUniquePN))

for x in trainingVocabulary.keys():
    if x in deceptiveDictionary:
        deceptiveProb[x] = math.log10((deceptiveDictionary[x] + 1) / float(deceptiveTotal + lenUniquePN))
    else:
        deceptiveProb[x] = math.log10(1 / float(deceptiveTotal + lenUniquePN))

# store the prior probability and the probability of each word in each class to a map - mapTrainData
mapTrainData["priorTruthful"] = math.log10(truthCount/float(len(class1Dictionary)))
mapTrainData["priorDeceptive"] = math.log10(deceptiveCount/float(len(class1Dictionary)))
mapTrainData["priorPositive"] = math.log10(positiveCount/float(len(class2Dictionary)))
mapTrainData["priorNegative"] = math.log10(negativeCount/float(len(class2Dictionary)))

mapTrainData["wordTruthfulClass"] = truthfulProb
mapTrainData["wordDeceptiveClass"] = deceptiveProb
mapTrainData["wordPositiveClass"] = positiveProb
mapTrainData["wordNegativeClass"] = negativeProb

# print mapTrainData

# write the mapTrainData content to nbmodel.txt in json format
with open(modelName, 'w') as handle:
    json.dump(mapTrainData, handle, indent=True)
