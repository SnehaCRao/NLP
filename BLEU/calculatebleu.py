import sys
import os
import math
import collections

candidate_sentences = collections.OrderedDict()
size = 0
refSize = 0
referenceSentences = []


def cand_fetch_data(filename):
    global candidate_sentences, size
    with open(filename, "r") as f:
        for line in f:
            sentence = line.strip()
            words = sentence.split()
            candidate_sentences[sentence] = words
            size += len(words)


def ref_fetch_data(filename):
    global refSize
    referenceSentence = collections.OrderedDict()
    with open(filename, "r") as f:
        for line in f:
            sentence = line.strip()
            words = sentence.split()
            referenceSentence[sentence] = words
            refSize += len(words)
    return referenceSentence


def sentence_size(sentence):
    words = sentence.split()
    sent_size = len(words)
    return sent_size


def ngram_length(candidate_sentence, n):
    return sum(ngram(candidate_sentence, n).values())


def ngram(sentence, n):
    # if(val == True):
    words = candidate_sentences[sentence]
    # else:
    #     words = referenceSentences[sentence]
    return collections.Counter(zip(*[words[i:] for i in range(n)]))


def ngram_ref(words, n, val):
    return collections.Counter(zip(*[words[i:] for i in range(n)]))


def max_match(c_ngram, r_ngrams):
    return max(map(lambda r: r[c_ngram], r_ngrams))


def counts(candidate_sentence, reference, n):
    c_ngrams = ngram(candidate_sentence, n)
    r_ngrams = []
    for key, value in reference.iteritems():
        r_ngrams.append(ngram_ref(value, n, False))
    print r_ngrams
    count = 0
    for c_ngram, c_count in c_ngrams.iteritems():
        count += min(c_count, max_match(c_ngram, r_ngrams))
    return count


def reference_count(candidate_sentence, count, n):
    reference_key = map(lambda r: r.keys()[count], referenceSentences)
    i = 0
    reference = {}
    for key in reference_key:
        word = referenceSentences[i][key]
        reference[key] = word
        i += 1
    print reference
    return counts(candidate_sentence, reference, n)


def precision(n):
    numerator = 0
    denominator = 0
    count = 0
    for k, v in candidate_sentences.items():
        candidate_sentence = k
        numerator += reference_count(candidate_sentence, count, n)
        denominator += ngram_length(candidate_sentence, n)
        count += 1
    return float(numerator) / float(denominator)


def min_reference_size(candidate, count):
    reference_key = map(lambda r: r.keys()[count], referenceSentences)
    i = 0
    reference = []
    reference_sentence = {}
    for key in reference_key:
        word = referenceSentences[i][key]
        reference.append(word)
        reference_sentence[key] = word
        i += 1
    print reference
    size_diff = map(lambda r: abs(len(candidate_sentences[candidate]) - len(r)), reference)
    print size_diff
    min_reference_sentence = reference[size_diff.index(min(size_diff))]
    return min_reference_sentence


def brevity_penality():
    len_c = 0
    len_r = 0
    count = 0
    for k, v in candidate_sentences.items():
        candidate_sentence = k
        min_reference_sentence = min_reference_size(candidate_sentence, count)
        len_c += sentence_size(candidate_sentence)
        len_r += len(min_reference_sentence)
        count += 1
    if len_c > len_r:
        return 1
    else:
        return math.exp(1 - (len_r / len_c))


def get_bleu_score():
    precision_val = 0.0
    weight = 0.25
    for i in range(4):
        precision_val += weight * math.log(precision(i + 1))
    return brevity_penality() * math.exp(precision_val)


candidate_file = sys.argv[1]
reference_file = sys.argv[2]
cand_fetch_data(candidate_file)
if os.path.isdir(reference_file):
    for dirpath, dirs, files in os.walk(reference_file):
        for file in files:
            referenceSentences.append(ref_fetch_data(os.path.join(dirpath, file)))
else:
    referenceSentences.append(ref_fetch_data(reference_file))

with open("bleu_out.txt", "w") as fout:
    bleu_score = get_bleu_score()
    print bleu_score
    fout.write(str(bleu_score))
