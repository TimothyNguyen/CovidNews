import csv, json, sys, math
import numpy as np
import pandas as pd


def normalize(data):
    temp = {'title': '', 'body': '', 'name': '', 'link': '', 'home_page_url': '', 'domain': '', 'summary': [],
            'locations': [], 'language': '', 'published_at': np.nan, 'words_count': np.nan, 'facebook': [], 
            'linkedin': [], 'reddit': [], 'google_plus': []}
    for key, value in data.items():
        if(isinstance(value, dict)):
            #print("Key {}".format(key))
            for k, v in value.items():
                #print("{}: {}".format(k, v))
                if(k == 'name'):
                    temp['name'] = v
                elif(k == 'permalink'):
                    temp['link'] = v
                elif(k == 'home_page_url'):
                    temp['home_page_url'] = v
                elif(k == 'domain'):
                    temp['domain'] = v
                elif(k == 'sentences'):
                    temp['summary'] = v
                elif(k == 'locations'):
                    temp['locations'] = v
                elif(k == 'facebook'):
                    temp['facebook'] = v
                elif(k == 'linkedin'):
                    temp['linkedin'] = v
                elif(k == 'google_plus'):
                    temp['google_plus'] = v
                elif(k == 'reddit'):
                    temp['reddit'] = v
            #print("\n")
        else:
            #print("{}: {}\n".format(key, value))
            if(key == 'body'):
                temp['body'] = value
            elif(key == 'hashtags'):
                temp['hashtags'] = value
            elif(key == 'language'):
                temp['language'] = value
            elif(key == 'published_at'):
                temp['published_at'] = value
            elif(key == 'title'):
                temp['title'] = value
            elif(key == 'words_count'):
                temp['words_count'] = value
    return temp

def testParams(params, data):
    for k in params.keys():
        if params[k]["comparator"](data[k]):
            if params[k]["subparams"] != None:
                testParams(params[k]["subparams"],data)
            else:
                if params[k]["quantity"] > len(params[k]["list"]):
                    params[k]["list"].append(data)
def paramFulfilled(params):
    for v in params.values():
        if v["subparams"] == None:
            if len(v["list"]) < v["quantity"]:
                return False
        elif paramFulfilled(v["subparams"]) == False:
                return False
    return True
def queryDB(params, maxqueryNum = math.inf):
    clearParams(params)
    with open("aylien-covid-news.jsonl", 'r', encoding='utf-8') as f:
        for i,line in enumerate(f):
            if i == maxqueryNum or paramFulfilled(params):
                break
            data = normalize(json.loads(line))
            testParams(params,data)
    return params
def clearParams(p):
    if p == None:
        return
    for v in p.values():
        v["list"] = []
        if v["subparams"] != None:
            clearParams(v["subparams"])
def parseResult(p):
    if p == None:
        return []
    acc = []
    for v in p.values():
        acc += v["list"]
        acc += parseResult(v["subparams"])
    return acc

def addCondition(query, attr, quant, f):
    query[attr] = {"quantity":quant, "comparator":f, "subparams":None, "list": []}
    return query[attr]

def addSubCondition(query, attr, quant, f):
    if query["subparams"] == None:
        query["subparams"] = {}
    return addCondition(query["subparams"], attr, quant, f)

def getParsedDF(p):
    return pd.DataFrame(parseResult(p))
