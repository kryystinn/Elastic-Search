# Para poder usar la función print e imprimir sin saltos de línea
from __future__ import print_function

import json # Exportamos en archivos JSON
import pprint
import sys
from elasticsearch import helpers
from elasticsearch import Elasticsearch

def main():
    elasticS = Elasticsearch()
    pp = pprint.PrettyPrinter(indent=2)
    stopW = loadStopWords()
    aux = elasticS.search(
        index="reddit-mentalhealth",
        body = {
                "size": 0,
                "query": {
                    "match": {
                        "selftext":"alcoholism"
                    }
                },
                "aggs": {
                    "texto": {
                      "significant_terms": {
                        "field": "selftext",
                        "size":10,
                        "chi_square": {
	 }
                        }
                    }
                }
         }
    )

    keyW=set()
    for i in aux["aggregations"]["texto"]["buckets"]:
            if(i["key"] not in stopW):
                keyW.add(str(i["key"]))

    query=""
    for i in keyW:
       query += i + " "

    aux = helpers.scan(elasticS,
        index="reddit-mentalhealth",
        query={
            "query": {
                "query_string": {
                    "query": query
                }
            },
        }
    )

    data={}
    data['entradas'] = []
    for i in aux:
        data['entradas'].append({'author': i["_source"]["author"].encode("utf8"),
            'created_utc': i["_source"]["created_utc"],
            'selftext': i["_source"]["selftext"].encode("utf8")})

    with open('ejercicio1-chi-10terminos.json', 'w') as outfile:
        json.dump(data, outfile,indent=True)

def loadStopWords():
    file=open('./stop.txt','r')
    result=file.read().splitlines()
    file.close
    return result


if __name__ == '__main__':
    main()