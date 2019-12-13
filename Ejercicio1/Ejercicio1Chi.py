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

#funcion main
def main5terms():
    #definicion de una variable que usaremos para las herramientas de elastic
    elasticS = Elasticsearch()
    #cargamos en una variable auxiliar las palabras que deseamos ignorar
    stopW = loadStop()
    aux = elasticS.search(index="reddit-mentalhealth",
        body = {
                  "size": 0,
                  "query": {
                    "match": {
                      "selftext": "alcoholism"
                    }
                  },
                  "aggs": {
                    "info": {
                      "significant_terms": {
                        "field": "selftext",
                        "size": 5,
                        "chi_square": {}
                      }
                    }
                  }
                }
    )

    #filtramos las consultas con las palabras que han de ser ignoradas
    #añadiendolas a un set adicional
    keyW=set()
    for i in aux["aggregations"]["info"]["buckets"]:
            if(i["key"] not in stopW):
                keyW.add(str(i["key"]))

    #empleamos los helpers de elasticsearch
    query=""
    for i in keyW:
       query += i + " "

    aux = help.scan(elasticS, index="reddit-mentalhealth",
        query={
            "query": {
                "query_string": {
                    "query": query
                }
            },
        }
    )

    #para cada entrada obtenida la añadimos a nuestros datos de salida
    data={}
    data['entries'] = []
    for i in aux:
        data['entries'].append({'author': i["_source"]["author"].encode("utf8"),
            'created_utc': i["_source"]["created_utc"],
            'selftext': i["_source"]["selftext"].encode("utf8")})

    #volcamos los datos en un fichero de salida JSON
    with open('tarea1_chi_5Terms.json', 'w') as output:
        json.dump(data, output,indent=True)

#funcion main
def main10terms():
    #definicion de una variable que usaremos para las herramientas de elastic
    elasticS = Elasticsearch()
    #cargamos en una variable auxiliar las palabras que deseamos ignorar
    stopW = loadStopWords()
    aux = elasticS.search(index="reddit-mentalhealth",
        body = {
                  "size": 0,
                  "query": {
                    "match": {
                      "selftext": "alcoholism"
                    }
                  },
                  "aggs": {
                    "info": {
                      "significant_terms": {
                        "field": "selftext",
                        "size": 10,
                        "chi_square": {}
                      }
                    }
                  }
                }
    )

    #filtramos las consultas con las palabras que han de ser ignoradas
    #añadiendolas a un set adicional
    keyW=set()
    for i in aux["aggregations"]["info"]["buckets"]:
            if(i["key"] not in stopW):
                keyW.add(str(i["key"]))

    #empleamos los helpers de elasticsearch
    query=""
    for i in keyW:
       query += i + " "

    aux = help.scan(elasticS, index="reddit-mentalhealth",
        query={
            "query": {
                "query_string": {
                    "query": query
                }
            },
        }
    )

    #para cada entrada obtenida la añadimos a nuestros datos de salida
    data={}
    data['entries'] = []
    for i in aux:
        data['entries'].append({'author': i["_source"]["author"].encode("utf8"),
            'created_utc': i["_source"]["created_utc"],
            'selftext': i["_source"]["selftext"].encode("utf8")})

    #volcamos los datos en un fichero de salida JSON
    with open('tarea1_chi_10Terms.json', 'w') as output:
        json.dump(data, output,indent=True)


#llamamos a los mains para ejecutar las funciones
main5terms()
main10terms()