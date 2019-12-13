################################imports########################################
import json # Para poder trabajar con objetos JSON
from elasticsearch import helpers as help
from elasticsearch import Elasticsearch
###############################################################################

#funcion que nos permite cargar un fichero de palabras vacias para ignorarlas
#en a búsqueda
def loadStop():
    result=open('./stop.txt','r').read().splitlines()
    file.close
    return result

#main para 5 terminos
def main5terms():
    stopW=loadStop()
    #realizamos la consulta
    es = Elasticsearch()
    aux = es.search(
        index="reddit-mentalhealth",
        body = {
                "size": 20,
                "query": {
                    "match": {
                        "selftext":"alcoholism"
                    }
                }
         }
    )

    info=[]

    for i in aux['hits']['hits']:
        info.append(i['_source']['selftext'].encode("utf8"))

    aux = help.scan(es,
        index="reddit-mentalhealth",
        query={
            "query": {
                "more_like_this" : {
                        "fields" : ["selftext"],
                        "like" : [{
                            "_index" : "reddit-mentalhealth",
                            "_type" : "post",
                            "doc" :{
                            "selftext":info
                            }
                        }],
                        "min_term_freq" : 1,
                        "max_query_terms" : 5,
                        "stop_words":stopW
                    }
            }
        }
    )

    data={}
    data['entries'] = []
    for i in aux:
        data['entries'].append({'author': i["_source"]["author"].encode("utf8"),
            'created_utc': i["_source"]["created_utc"],
            'selftext': i["_source"]["selftext"].encode("utf8")})

    with open('tarea2_5Terms.json', 'w') as output:
        json.dump(data, output,indent=True)

#main para 10 terminos
def main10terms():
    stopW=loadStop()
    #realizamos la consulta
    es = Elasticsearch()
    aux = es.search(
        index="reddit-mentalhealth",
        body = {
                "size": 20,
                "query": {
                    "match": {
                        "selftext":"alcoholism"
                    }
                }
         }
    )

    info=[]

    for i in aux['hits']['hits']:
        info.append(i['_source']['selftext'].encode("utf8"))

    aux = help.scan(es,
        index="reddit-mentalhealth",
        query={
            "query": {
                "more_like_this" : {
                        "fields" : ["selftext"],
                        "like" : [{
                            "_index" : "reddit-mentalhealth",
                            "_type" : "post",
                            "doc" :{
                            "selftext":info
                            }
                        }],
                        "min_term_freq" : 1,
                        "max_query_terms" : 10,
                        "stop_words":stopW
                    }
            }
        }
    )

    data={}
    data['entries'] = []
    for i in aux:
        data['entries'].append({'author': i["_source"]["author"].encode("utf8"),
            'created_utc': i["_source"]["created_utc"],
            'selftext': i["_source"]["selftext"].encode("utf8")})

    with open('tarea2_10Terms.json', 'w') as output:
        json.dump(data, output,indent=True)

#ejecutamos los mains
main5terms()
main10terms()
