# coding=utf-8
################################imports########################################
import json
from elasticsearch import Elasticsearch
###############################################################################

#funcion que nos permite cargar un fichero de palabras vacias para ignorarlas
#en la búsqueda
def loadStop():
    result=open('./stop.txt','r').read().splitlines()
    file.close
    return result

#función que buscará palabras relacionadas con posibles factores comórbidos relativos a la ideación suicida,
#comprobará que no se encuentran dentro del fichero de StopWords y que tampoco son números aislados,
#e imprimirá por pantalla las palabras resultantes
def ejercicio4_suicide():
    es = Elasticsearch();
    stopW = loadStop(); #se carga el fichero StopWords
    result = []; #lista de palabras resultantes
    comorbido = []; #lista de palabras comórbidas
    results = es.search(
        index="reddit-mentalhealth",
        body = {
          "size": 0,
            "query": {
                "multi_match": {
                    "query": "suicide OR suicidal OR kill myself OR killing myself OR end my life",
                    "fields": ["title", "selftext", "subreddit"]
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

    for i in results["aggregations"]["texto"]["buckets"]:
            if(i["key"] not in stopW and not (i["key"].isdigit()) ):
                result.append(str(i["key"].encode("utf8")));

    for j in result:
        if(esFactorComorbido(j, "suicideGS.json")):
            comorbido.append(j)

    print("--- Found Comorbids ---")
    for word in comorbido:
        print(word);


def esFactorComorbido(palabra , archivo):
    with open(archivo,"r") as aux:
        info = json.load(aux)
        if palabra.decode("utf8") in info:
            return True
        return False

ejercicio4_suicide();
