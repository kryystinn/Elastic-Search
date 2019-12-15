###############################imports##########################################
from elasticsearch import Elasticsearch
import json
from SPARQLWrapper import SPARQLWrapper, JSON
###############################imports##########################################

def ejercicio3():

    #instancia de elasticsearch
    es = Elasticsearch()
    #url de wikidata para la consulta de datos
    url = "https://query.wikidata.org/sparql"

    #consulta que contrastamos con wikidata
    consulta ="""SELECT DISTINCT ?itemLabel
    WHERE {
        ?item rdfs:label ?nombre.?item wdt:P31 ?tipo.VALUES ?tipo {wd:Q28885102 wd:Q12140}
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }"""

    #ejecutamos la consulta
    aux = SPARQLWrapper(url)
    aux.setQuery(consulta)
    aux.setReturnFormat(JSON)
    json=  aux.query().convert()["results"]["bindings"]

    #parseamos los valores obtenidos en una lista
    lista_meds = []
    for e in json:
        for value in e.values():
            lista_meds.append(value['value'])

    #lanzamos la busqueda en elasticsearch
    data = es.search(index="reddit-mentalhealth",
    body = {
        "size": 0,
        "query": {
            "query_string": {
                "query": "using OR prescribed OR dose OR mg -water",
                "allow_leading_wildcard": "true"
            }
        },
          "aggs": {
            "Title": {
              "significant_terms": {
                "field": "title",
                "size": 1000,
				"gnd":{}
              }
            },
            "Text": {
              "significant_terms": {
                "field": "selftext",
                "size": 1000,
				"gnd":{}
              }
            }
          }
    })

    #parseamos los datos obtenidos
    meds = []
    for j in ["Text", "Title"]:
        for i in data["aggregations"][j]["buckets"]:
            if (i["key"] not in meds and i["key"] in lista_meds):
                meds.append(i["key"])

    #imprimimos por pantalla el resultado
    print("--- Resultado ---")
    for med in meds:
        print(med)

ejercicio3()