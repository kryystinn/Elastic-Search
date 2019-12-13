# Para poder usar la función print e imprimir sin saltos de línea
from __future__ import print_function

import json # Para poder trabajar con objetos JSON
import pprint # Para poder hacer uso de PrettyPrinter
import sys # Para poder usar exit
import requests

from elasticsearch import Elasticsearch

# Queremos imprimir bonito
pp = pprint.PrettyPrinter(indent=2)

def main():

    # Nos conectamos por defecto a localhost:9200
    es = Elasticsearch()

    # En ocasiones las consultas tienen que formalizarse en JSON
    results = es.search(
        index="reddit-mentalhealth",
            body = {
                "size": 0,
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match_phrase": {
                                    "selftext": "I was taking"
                                }
                            },
                            {
                                "multi_match": {
                                    "query": "mg",
                                    "fields": ["selftext", "title"]
                                }
                            },
                            {
                                "match_phrase": {
                                    "selftext": "I was on"
                                }
                            },
                            {
                                "match": {
                                    "selftext": "dose"
                                }
                            },
                            {
                                "match": {
                                    "selftext": "prescribed"
                                }
                            }


                        ]
                    }
                },
                "aggs": {
                    "posibles medicamentos": {
                        "significant_terms": {
                            "field": "title",
                            "gnd": {}
                        }
                    }
                }
            }


    )

    for bucket in results['aggregations']['posibles medicamentos']['buckets']:
        medicamento = bucket['key']
        if (es_medicamento(medicamento)):
            print(medicamento)

def es_medicamento(candidato):

    url = 'https://query.wikidata.org/sparql'
    query = """
            SELECT ?item WHERE {
              ?item rdfs:label ?nombre.
              ?item wdt:P31 ?tipo.
              VALUES ?tipo {wd:Q28885102 wd:Q12140}
              FILTER(LCASE(?nombre) = "%s"@en)
            }
            """ % (candidato)
    r = requests.get(url, params = {'format': 'json', 'query': query})
    data = r.json()

    return len(data['results']['bindings']) > 0

if __name__ == '__main__':
    main()
