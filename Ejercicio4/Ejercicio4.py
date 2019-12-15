################################imports########################################
import json
from elasticsearch import Elasticsearch
###############################################################################

#funcion que nos permite cargar un fichero de palabras vacias para ignorarlas
#en a busqueda
def loadStop():
    result=open('./stop.txt','r').read().splitlines()
    file.close
    return result

def ejercicio4_suicide():
    es = Elasticsearch()
    stopW = loadStop();
    results = es.search(
            index="reddit-mentalhealth",
            body = {
              "size": 0,
              "query": {
                "bool": {
                  "should": [
                    {
                      "match_phrase": {
                        "title": "self harm"
                      }
                    },
                    {
                      "match_phrase": {
                        "selftext": "self harm"
                      }
                    },
                    {
                      "match_phrase": {
                        "subreddit": "self harm"
                      }
                    }
                  ]
                }
              },
              "aggs": {
                "texto": {
                  "significant_terms": {
                    "field": "selftext",
                    "size": 350,
                    "gnd": {}
                  }
                }
              }
            }
        )

    result=[]
    for i in results["aggregations"]["texto"]["buckets"]:
            if(i["key"] not in stopW):
                result.append(str(i["key"].encode("utf8")))

    comorbido=[]
    for i in result:
        if(isComorbid(i, "selfharm.json")):
            comorbido.append(i)

    print("--- Found Comorbids ---")
    for word in comorbido:
        print("\t",word)


def ejercicio4_selfharm():
    es = Elasticsearch();
    stopW = loadStop();
    results = es.search(
            index="reddit-mentalhealth",
            body = {
              "size": 0,
              "query": {
                "bool": {
                  "should": [
                    {
                      "match_phrase": {
                        "title": "suicide"
                      }
                    },
                    {
                      "match_phrase": {
                        "selftext": "suicide"
                      }
                    },
                    {
                      "match_phrase": {
                        "subreddit": "suicide"
                      }
                    },
                    {
                      "match_phrase": {
                        "title": "suicidal"
                      }
                    },
                    {
                      "match_phrase": {
                        "selftext": "suicidal"
                      }
                    },
                    {
                      "match_phrase": {
                        "subreddit": "suicidal"
                      }
                    },
                    {
                      "match_phrase": {
                        "title": "kill myself"
                      }
                    },
                    {
                      "match_phrase": {
                        "selftext": "kill myself"
                      }
                    },
                    {
                      "match_phrase": {
                        "subreddit": "kill myself"
                      }
                    }
                  ]
                }
              },
              "aggs": {
                "texto": {
                  "significant_terms": {
                    "field": "selftext",
                    "size": 350,
                    "gnd": {}
                  }
                }
              }
            }
        )

    result=[]
    for i in results["aggregations"]["texto"]["buckets"]:
        if(i["key"] not in stopW):
            result.append(str(i["key"].encode("utf8")))

    comorbido=[];
    for i in result:
        if(isComorbid(i, "selfharm.json")):
            comorbido.append(i);

    print("--- Found Comorbids ---")
    for word in comorbido:
        print("\t",word)

def isComorbid(palabra , archivo):
    with open(archivo,"r") as file:
        data=json.load(file)
        if palabra.decode("utf8") in data:
            return True
        return False

ejercicio4_suicide();
ejercicio4_selfharm();