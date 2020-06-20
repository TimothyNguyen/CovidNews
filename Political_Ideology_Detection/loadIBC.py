from __future__ import division
import pickle
from random import randint
import math
import Political_Ideology_Detection.naiveBayesOnlySentence as naiveBayesOnlySentence
import Political_Ideology_Detection.logRegOnlySentence
import Political_Ideology_Detection.logRegw2v
import Political_Ideology_Detection.mostCommon
import Political_Ideology_Detection.logRegSentenceAndPhrase
import Political_Ideology_Detection.logRegOnlyPhrase
import Political_Ideology_Detection.naiveBayesSentenceAndPhrase
import Political_Ideology_Detection.run_w2vec
from sklearn.model_selection import KFold
from numpy import array, mean, median
from random import shuffle
import Political_Ideology_Detection.getStats

TRAIN_TEST_SPLIT = 0.9

def test_random(test_data):
    count = 0
    for each_ob in test_data:
        gen = randint(0, 1)
        if (gen == each_ob["label"]):
            count += 1
        print("Random Classifier:", count / len(test_data))

# def train_test_split(lib, con):
#     total_data = []
#     for lib_sent in lib:
#        total_data.append({"sentence": lib_sent.get_words(), "label": 0})
#     for con_sent in con:
#       total_data.append({"sentence": con_sent.get_words(), "label": 1})
#     lim = int(math.floor(TRAIN_TEST_SPLIT * len(total_data)))
#     shuffle(total_data)
#     train_data = total_data[:lim]
#     test_data = total_data[lim:]
#
#     return total_data, train_data, test_data

def lr2(model, total_data):
    lim = int(math.floor(TRAIN_TEST_SPLIT * len(total_data)))
    train = total_data[:lim]
    test = total_data[lim:]
    results = {"accuracy":[], "fpr":[], "tpr":[]}

    accuracy, fpr, tpr = model.run(train, test)
    results["accuracy"].append(accuracy)
    results["fpr"].append(fpr)
    results["tpr"].append(tpr)

    print("Average Accuracy: ", mean(results["accuracy"]))
    model.generate_plot(accuracy, fpr, tpr)

def lrw2v(model, total_data):
    lim = int(math.floor(TRAIN_TEST_SPLIT * len(total_data)))
    train = total_data[:lim]
    test = total_data[lim:]

    print(len(train))

    f_vecs_train = pass_data_to_w2vec(train)
    f_vecs_test = pass_sent_to_w2vec(test)

    results = {"accuracy": [], "fpr": [], "tpr": []}

    accuracy, fpr, tpr = model.run(f_vecs_train, f_vecs_test)
    results["accuracy"].append(accuracy)
    results["fpr"].append(fpr)
    results["tpr"].append(tpr)

    print("Average Accuracy: ", mean(results["accuracy"]))
    model.generate_plot(accuracy, fpr, tpr)